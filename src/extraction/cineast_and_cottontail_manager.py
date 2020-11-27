from pathlib import Path

from src.extraction.cineast_manager import CineastManager
from src.extraction.cottontail_manager import CottontailManager


class CineastAndCottontailManager:

    def __init__(self, server_config_data):
        self.__cottontailManager = CottontailManager(server_config_data)

        self.__cineastManager = CineastManager(server_config_data)

    def start_extraction(self, new_content_to_extract_path_str, num_of_elements_to_extract, setup=False):
        num_of_elem_before = self.get_table_count()
        self.__cineastManager.extract_content_to_database(new_content_to_extract_path_str, setup)
        num_of_elem_after = self.get_table_count()
        assert (num_of_elem_before + num_of_elements_to_extract == num_of_elem_after)

    def get_table_count(self):
        table_name = "cineast_multimediaobject"
        return self.__cottontailManager.count_elements_in_table(table_name)

    def get_object_feature_information(self, object_id):
        table_name = "features_notexistant"
        return self.__cottontailManager.get_all_aesthetic_attributes_of_object(object_id)
