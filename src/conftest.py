"""
This file is necessary to run the unit tests in test_sync_directories.py file
Do not delete this file.

Author : Sushma Bhandari

"""

import os.path
import time
import pytest
import shutil



# create a source directory. this is first step before starting a test
@pytest.fixture(scope="session")
def create_source_dir():
    # create a source directory
    cwd = os.getcwd()
    sourcedir = "SourceDir"
    parent_dir = os.path.dirname(cwd)
    source_dir_path = os.path.join(parent_dir, sourcedir)
    if os.path.exists(source_dir_path):
        shutil.rmtree(source_dir_path)
    if os.path.exists(os.path.join(parent_dir, "ReplicaDir")):
        shutil.rmtree(os.path.join(parent_dir, "ReplicaDir"))


    os.makedirs(source_dir_path)

    # create a directory (Folder1) within a source directory with 3 text files
    folder1_dir = os.path.join(source_dir_path, "Folder1")
    os.makedirs(folder1_dir)
    with open(os.path.join(folder1_dir, "Folder1_file1.txt"), 'w') as fp:
        fp.write('This is a new Folder1 -> file1.')
    with open(os.path.join(folder1_dir, "Folder1_file2.txt"), 'w') as fp:
        fp.write('This is a new Folder1 -> file2. \n This is a second file within Folder1.')
    with open(os.path.join(folder1_dir, "Folder1_file3.txt"), 'w') as fp:
        fp.write("")

    # create an empty directory (Folder2) within a source directory
    folder1_dir = os.path.join(source_dir_path, "Folder2")
    os.makedirs(folder1_dir)
    # comment out the following if you do not want to delete the source directory and replica directory created
    # during text execution


# create a file within source directory
@pytest.fixture
def create_new_file():
    with open(os.path.join("..\\SourceDir", "salesfile.txt"), 'w') as fp:
        fp.write('This is a new file.')
    print("File is created in source directory")


# create a file within subfolder of source directory
@pytest.fixture
def create_new_file_in_subfolder():
    with open(os.path.join("..\\SourceDir\\Folder2", "Folder2_file1.txt"), 'w') as fp:
        fp.write('This is a newly file within Folder2.')
    print("File is created in a subfolder with source directory")


# delete a file from source directory
@pytest.fixture()
def delete_file():
    if os.path.exists("..\\SourceDir\\salesfile.txt"):
        os.remove("..\\SourceDir\\salesfile.txt")
    else:
        print("The file you are trying to delete doesnot exit")


# add content within a file of sub-folder in source directory
@pytest.fixture()
def add_content_in_file():
    with open(os.path.join("..\\SourceDir\\Folder1", "Folder1_file3.txt"), 'a') as fp:
        fp.write("This is added content")
    print("Content added into a file.")
