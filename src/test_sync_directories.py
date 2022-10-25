"""
This file is used for unit test.

Author : Sushma Bhandari
"""
import datetime
import os.path
import pytest
from sync_directories import *
from utils import *


# test if a replica of a directory is done when the replica directory does not exist
@pytest.mark.dependency()
def test_replicate_dir(create_source_dir):
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.replicate_dir()
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


# test if a replica of a directory is done when the replica directory already exist
@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_replicate_dir_replica_exist():
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.replicate_dir()
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


# test if default logfile is created
@pytest.mark.dependency()
def test_default_logfile():
    Synchronization("..\\SourceDir", "..\\ReplicaDir")
    assert os.path.isfile("synclog.log")


# test if synchronization works when a file is added at source
@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_sync_dir_file_added_on_source(create_new_file):
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.sync_dir("..\\SourceDir", "..\\ReplicaDir")
    assert os.path.isfile("..\\ReplicaDir\\salesfile.txt")
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_sync_dir_file_added_in_subfolder_source(create_new_file_in_subfolder):
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.sync_dir("..\\SourceDir", "..\\ReplicaDir")
    assert os.path.isfile("..\\ReplicaDir\\Folder2\\Folder2_file1.txt")
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


# test if synchronization works when a file is deleted at source
@pytest.mark.dependency(depends=['test_replicate_dir', 'test_sync_dir_file_added_on_source'])
def test_sync_dir_file_deleted_on_source(delete_file):
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.sync_dir("..\\SourceDir", "..\\ReplicaDir")
    assert not os.path.isfile("..\\ReplicaDir\\salesfile.txt")
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


# test if synchronization works when content within a file is changed
@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_sync_dir_file_content_changed(add_content_in_file):
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir")
    sync.sync_dir("..\\SourceDir", "..\\ReplicaDir")
    fopen = open('..\\ReplicaDir\\Folder1\\Folder1_file3.txt', mode='r+')
    fread = fopen.readlines()
    for text in fread:
        assert "This is added content" in text
    compare = filecmp.dircmp("..\\SourceDir", "..\\ReplicaDir")
    assert len(compare.diff_files) == 0


@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_sync_periodic_sync_timeinterval():
    time_now = get_current_datetime()
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir", sync_interval=5,
                           log_file_path="..\\SourceDir\\synclogfile.log", time_out=1)
    sync.periodic_sync()
    datetime_lastline = get_logfile_datetime(logfile="..\\SourceDir\\synclogfile.log", linenum=-1)
    datetime_secondlastline = get_logfile_datetime(logfile="..\\SourceDir\\synclogfile.log", linenum=-2)
    delta = datetime_lastline - datetime_secondlastline
    duration = delta.seconds
    assert duration == 5


@pytest.mark.dependency(depends=['test_replicate_dir'])
def test_sync_periodic_sync_timeout():
    time_now = get_current_datetime()
    sync = Synchronization("..\\SourceDir", "..\\ReplicaDir", sync_interval=5,
                           log_file_path="..\\SourceDir\\synclogfile.log", time_out=1)
    sync.periodic_sync()
    datetime_lastline = get_logfile_datetime(logfile="..\\SourceDir\\synclogfile.log", linenum=-1)
    delta = datetime_lastline - time_now
    duration = delta.seconds
    assert 55 <= duration <= 65
