"""
Module Responsibilities:
    1. Creation of directories and files, delete content from directories.
    2. Download of files from url.
"""

import os
from pathlib import Path
import shutil

import wget


def get_num_of_files_in_directory(directory_abs_path):
    return len([f for f in os.listdir(directory_abs_path) if os.path.isfile(os.path.join(directory_abs_path, f))])


def delete_contents_in_directory(directory_abs_path):
    try:
        shutil.rmtree(directory_abs_path)
    except OSError as e:
        print("Error: %s : %s" % (directory_abs_path, e.strerror))


def delete_contents_with_exceptions_in_directory(directory_abs_path, subdirs_to_exclude):
    try:
        for f in os.scandir(directory_abs_path):
            if f.is_dir() and f.path not in subdirs_to_exclude:
                shutil.rmtree(f.path)
    except OSError as e:
        print("Error: %s : %s" % (directory_abs_path, e.strerror))


def create_directories_if_not_exists(directory_abs_path):
    if not os.path.exists(directory_abs_path):
        os.makedirs(directory_abs_path)
        print("Created folder: " + directory_abs_path)


def copy_if_file_does_not_exist(file_path_dest_str, file_path_src_str):
    my_file = Path(file_path_dest_str)
    if not my_file.is_file():
        shutil.copyfile(file_path_src_str, file_path_dest_str)
        print("Copied : " + file_path_src_str + " to :" + file_path_dest_str)


def download_file_from_url(file_url, file_storage_path, over_write=False):
    file_storage_path_str = str(file_storage_path.absolute())
    if over_write and file_storage_path.exists():
        file_storage_path.unlink()

    wget.download(file_url, file_storage_path_str)
    print("Updated: " + file_storage_path_str)


def delete_all_in_dir(file_dir_str):
    try:
        if os.path.isdir(file_dir_str):
            shutil.rmtree(file_dir_str)
            print("Deleted everything in the directory: " + file_dir_str)
        else:
            print("The following is not a valid directory to delete: " + file_dir_str)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_dir_str, e))
