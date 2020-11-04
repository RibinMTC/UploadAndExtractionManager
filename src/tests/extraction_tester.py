import os
from pathlib import Path
from progressbar import ProgressBar

from src.extraction.cineast_and_cottontail_manager import CineastAndCottontailManager
from src.utils.server_config_data import ServerConfigData

base_path = Path(__file__).parent.parent.parent

serverConfigData = ServerConfigData(base_path)
cineast_and_cottontail_manager = CineastAndCottontailManager(serverConfigData)

test_import_folder_path = "/local/home/cribin/Documents/AestheticsBackup/Datasets/ava_large_dataset/extracted_images" \
                          "/images/"
num_files_to_extract = len([f for f in os.listdir(test_import_folder_path)
                            if os.path.isfile(os.path.join(test_import_folder_path, f))])

file_end_num = 51
pbar = ProgressBar()
for i in pbar(range(2, file_end_num)):
    file_name = test_import_folder_path + str(i) + "_1"
    num_files_to_extract = len([f for f in os.listdir(file_name)
                                if os.path.isfile(os.path.join(file_name, f))])
    print("Starting extraction for :" + file_name)
    cineast_and_cottontail_manager.start_extraction(file_name, num_files_to_extract, False)
