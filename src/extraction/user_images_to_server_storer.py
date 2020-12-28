"""
Module Responsibility: On each new upload, create a new folder and copy contents to said folder
Utilized by main_flask_app module
"""

import os
import shutil
from pathlib import Path
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def __get_new_import_folder_number(content_base_path_str):
    sorted_subdir = [subdir for subdir in os.listdir(content_base_path_str)
                     if os.path.isdir(os.path.join(content_base_path_str, subdir))]
    sorted_subdir.sort(key=natural_keys)

    if len(sorted_subdir) == 0:
        return 1

    get_last_import_number = int(sorted_subdir[-1].split('_')[1])

    return get_last_import_number + 1


def get_new_import_folder_path_str(content_base_path):
    content_base_path_str = str(content_base_path)
    if not content_base_path.exists():
        print("Aborting upload: The given path " + content_base_path_str + "does not exist.")
        return

    _new_import_number = __get_new_import_folder_number(content_base_path_str)

    new_import_folder_path_str = content_base_path_str + "/import_" + str(_new_import_number)
    new_import_folder_path = Path(new_import_folder_path_str)
    if new_import_folder_path.exists():
        print("Aborting upload: The folder: " + new_import_folder_path_str + " already exists.")
        return

    new_import_folder_path.mkdir()

    return new_import_folder_path_str


def __copy_user_content_to_server_folder(user_content_folder_path, server_import_folder_path):
    for content in user_content_folder_path.iterdir():
        shutil.copy(content, server_import_folder_path.absolute())
    print("Upload to Server successful")


def store_user_content_to_server(user_content_folder_path, server_content_base_path):
    if user_content_folder_path is not None:
        new_import_folder_path = get_new_import_folder_path_str(server_content_base_path)
        __copy_user_content_to_server_folder(user_content_folder_path, new_import_folder_path)
        return new_import_folder_path
