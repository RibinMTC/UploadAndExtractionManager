import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import time
from pathlib import Path

import requests

from src.utils.file_setup_util import get_num_of_files_in_directory, delete_contents_with_exceptions_in_directory
from src.extraction.cineast_and_cottontail_manager import CineastAndCottontailManager
from src.utils.server_config_data import ServerConfigData


def check_if_predictor_is_ready(predictor_address):
    try:
        response = requests.get(predictor_address)
        if "Model not initialized" in str(response.content):
            return None
        return "Model initialized"
    except Exception as e:
        print(str(e))
        return None


def poll_until_active_predictors_ready():
    active_predictors_address = cineast_and_cottontail_manager.get_active_predictors_address()
    for active_predictor_address in active_predictors_address:
        print("Waiting for connection with: " + active_predictor_address + " ...")
        predictor_response = None
        while predictor_response is None:
            predictor_response = check_if_predictor_is_ready(active_predictor_address)
            if predictor_response is None:
                time.sleep(10)
            else:
                print("Connection established to predictor: " + active_predictor_address)


def execute_custom_content_upload():
    custom_content_path = serverConfigData.custom_content_folder_path

    if not os.path.exists(custom_content_path):
        print("The folder " + custom_content_path + " does not exist. Aborting custom import.")
        return

    num_of_files_to_extract = get_num_of_files_in_directory(custom_content_path)
    print("Uploading " + str(num_of_files_to_extract) + " custom content...")
    if num_of_files_to_extract > 0:
        cineast_and_cottontail_manager.start_extraction(custom_content_path,
                                                        num_of_files_to_extract, True)


if __name__ == '__main__':
    if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
        config_file_path = "vitrivr_pipeline_config.json"
        print("Using global config")
    else:
        config_file_path = "vitrivr_pipeline_config_local.json"
        print("Using local config")

    base_path = Path(__file__).parent.parent
    serverConfigData = ServerConfigData(base_path, config_file_path)
    if serverConfigData.execute_feature_extraction:
        cineast_and_cottontail_manager = CineastAndCottontailManager(serverConfigData)
        poll_until_active_predictors_ready()
        if serverConfigData.custom_content_import:
            delete_contents_with_exceptions_in_directory(serverConfigData.shared_volume_base_path_str,
                                                         serverConfigData.server_content_base_path_str)
            cineast_and_cottontail_manager.setup_directories(serverConfigData)
            execute_custom_content_upload()
