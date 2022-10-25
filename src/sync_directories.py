"""
This file contains class with multiple methods that is used in directories synchronization.

Author : Sushma Bhandari
"""

import filecmp
import os
import shutil
import logging
import time
import argparse


class Synchronization:

    def __init__(self, source_path, replica_path, sync_interval=5, log_file_path="synclog.log", time_out=0):
        self.source = source_path
        self.replica = replica_path
        self.interval = sync_interval
        self.logpath = log_file_path
        self.timeout = time_out
        self.timing = time.time() + 60 * self.timeout

        # logging
        self.logs = logging.getLogger(__name__)
        self.logs.setLevel(logging.DEBUG)

        # logging into a log file
        file = logging.FileHandler(os.path.abspath(self.logpath))
        # file.setLevel(logging.INFO)
        file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file.setFormatter(file_format)
        self.logs.addHandler(file)

        # logging to a console output
        stream = logging.StreamHandler()
        # stream.setLevel(logging.INFO)
        stream_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream.setFormatter(stream_format)
        self.logs.addHandler(stream)




        self.logs.info(f"The logs are saved in '{os.path.abspath(self.logpath)}'. ")

    # the source directory is replicated into a replica directory, if there are any existing data, those will be
    # deleted before making the replica. This method should be used only for replicating a directory for the first time
    def replicate_dir(self):
        try:
            self.logs.info("\t------ INITIAL SYNCHRONIZATION IS RUNNING------\n")
            self.logs.info(f"Trying to replicate the contents of '{self.source}' into '{self.replica}'. ")
            self.logs.info(f"If the directory'{self.replica}' does not exist, a new directory will be created. ")
            self.logs.info(f"----If '{self.replica}' exist and has any existing data, those will be deleted before making the replica of '{self.source}'.")
            if os.path.isdir(self.replica):
                # if the replica directory is not empty, delete the directory and create a new one
                files_dirs = os.listdir(self.replica)
                if len(files_dirs) != 0:
                    shutil.rmtree(self.replica)
                    self.logs.warning(f"'{self.replica}' is not empty. So, deleted the existing content..")

            # copy the source directory to replica directory,
            # if replica directory is not available, new replica directory will be created
            shutil.copytree(self.source, self.replica)
            self.logs.info(f"Synchronized the content of '{self.source}' to '{self.replica}' directory.")
        except FileNotFoundError as fnf_error:
            self.logs.error(fnf_error)
        except Exception as ex:
            self.logs.error(ex)

    # compare two directories and their underlying subdirectories and make one way synchronization (source -> replica)
    def sync_dir(self, dir_original, dir_copy):
        try:
            comparisons = filecmp.dircmp(dir_original, dir_copy)
            # files and directories only available in source
            if comparisons.left_only:
                for source_file in comparisons.left_only:
                    source_file_path = os.path.join(dir_original, os.path.basename(source_file))
                    if os.path.isdir(source_file_path):
                        shutil.copytree(source_file_path, os.path.join(dir_copy, os.path.basename(source_file)))
                        self.logs.info(f"Copied '{source_file}' directory to '{dir_copy}'.")
                    else:
                        shutil.copyfile(source_file_path, os.path.join(dir_copy, os.path.basename(source_file)))
                        self.logs.info(f"Copied '{source_file}' file to '{dir_copy}'.")

            # If files are only available in the replica folder but has been deleted from source folder, delete them from
            # replica folder as well
            if comparisons.right_only:
                for replica_file in comparisons.right_only:
                    replica_file_path = os.path.join(dir_copy, os.path.basename(replica_file))
                    if os.path.isdir(replica_file_path):
                        shutil.rmtree(replica_file_path)
                        self.logs.info(f"Removed '{replica_file_path}' directory.")
                    else:
                        os.remove(replica_file_path)
                        self.logs.info(f"Removed '{replica_file_path}' file.")

            # if the content of the sub-folders in source is changed
            if comparisons.common_dirs:
                for directory in comparisons.common_dirs:
                    self.sync_dir(os.path.join(dir_original, directory), os.path.join(dir_copy, directory))

            # if the content of the files within the folder or sub-folder is changed
            if comparisons.diff_files:
                for diffFiles in comparisons.diff_files:
                    source_file_path = os.path.join(dir_original, os.path.basename(diffFiles))
                    shutil.copyfile(source_file_path, os.path.join(dir_copy, os.path.basename(diffFiles)))
                    self.logs.info(f"Synchronize '{diffFiles}' file in '{dir_copy}' folder as in '{dir_original}' folder.")

        except FileNotFoundError as fnf_error:
            self.logs.error(fnf_error)
        except Exception as ex:
            self.logs.error(ex)

    # periodic synchronization
    def periodic_sync(self):
        self.logs.info("\t------ PERIODIC SYNCHRONIZATION IS RUNNING------\n")
        self.logs.info(f"Synchronization of '{self.source}' to '{self.replica}' is done periodically in every {self.interval} seconds.")
        if self.timeout != 0:
            self.logs.info(f"The synchronization will end after {self.timeout} minutes")
        else:
            self.logs.info(f"Press 'ctr+c' to end the periodic synchronization")

        while True:
            if self.timeout != 0 and time.time() > self.timing:
                break
            self.sync_dir(self.source, self.replica)
            time.sleep(self.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronize two directories. "
                                                 "\n It is a one direction synchronization source -> replica ")
    parser.add_argument("source_path", type=str, help="Full path of the original directory.")
    parser.add_argument("replica_path", type=str, help="Full path of replica directory.")
    parser.add_argument("-i", "--interval", type=int, default=5, dest="sync_interval",
                        help="unit : seconds. After every <interval>seconds synchronization is performed.")
    parser.add_argument("-l", "--logfile", type=str, default="synclog.log", dest="log_file_path",
                        help="Full path of the logfile.")
    parser.add_argument("-t", "--timeout", type=int, default=0, dest="time_out",
                        help="unit : minute. Use only to end the synchronization after certain time.")

    args = parser.parse_args()
    sync_folders = Synchronization(args.source_path, args.replica_path, args.sync_interval, args.log_file_path,
                                   args.time_out)
    sync_folders.replicate_dir()
    sync_folders.periodic_sync()
