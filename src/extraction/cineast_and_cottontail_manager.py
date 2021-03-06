from src.extraction.cineast_manager import CineastManager
from src.extraction.cottontail_manager import CottontailManager
from src.utils.file_setup_util import create_directories_if_not_exists, delete_contents_with_exceptions_in_directory


class CineastAndCottontailManager:
    """
    This class provides an interface, with which the main_flask_app module can communicate with cineast and cottontail
    Class Responsibilities:
        1. Setup up necessary directories to store extracted content
        2. Initialize Cineast and Cottontail Manager classes
        3. Start extraction process, when content has been uploaded
    """

    def __init__(self, server_config_data):
        self._setup_directories(server_config_data)
        self.__cottontailManager = CottontailManager(server_config_data)

        self.__cineastManager = CineastManager(server_config_data)

    def _setup_directories(self, server_config_data):
        create_directories_if_not_exists(server_config_data.server_content_base_path_str)
        create_directories_if_not_exists(server_config_data.thumbnails_base_path_str)

    def start_extraction(self, new_content_to_extract_path_str, num_of_elements_to_extract, setup=False):
        num_of_elem_before = self.get_table_count()
        exception_occurred = self.__cineastManager.extract_content_to_database(new_content_to_extract_path_str, setup)
        num_of_elem_after = self.get_table_count()
        assert (num_of_elem_before + num_of_elements_to_extract == num_of_elem_after)
        return exception_occurred

    def get_table_count(self):
        table_name = "cineast_multimediaobject"
        return self.__cottontailManager.count_elements_in_table(table_name)

    def get_object_feature_information(self, object_id):
        return self.__cottontailManager.get_all_aesthetic_attributes_of_object(object_id)

    @staticmethod
    def get_active_predictors_address(server_config_data):
        return CineastManager.get_active_predictors_address(server_config_data)
