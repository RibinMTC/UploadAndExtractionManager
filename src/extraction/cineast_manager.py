from src.extraction.base_subprocess_manager import SubprocessManager
import src.utils.json_writer as json_manager
from src.utils.file_setup_util import download_file_from_url


class CineastManager(SubprocessManager):
    """
    This class handles the setup and interaction with cineast retrieval engine via the subprocess module
    """

    def __init__(self, server_config_data):
        self.__cineast_job_file_str = server_config_data.cineast_job_abs_path
        self.__cineast_api_jar_name = "cineast-api.jar"
        self._setup_config(server_config_data)
        cineast_start_cmd = "java -jar " + self.__cineast_api_jar_name + " " + server_config_data.cineast_config_abs_path
        super().__init__(server_config_data.cineast_base_path_str, cineast_start_cmd)

    def _setup_config(self, server_config_data):
        if server_config_data.update_cineast_jar_file:
            self._update_cineast_jar_file(server_config_data)

        cineast_config_dict = json_manager.get_dict_from_json(server_config_data.cineast_config_abs_path)

        if server_config_data.thumbnails_base_path_str != "" and server_config_data.server_content_base_path_str != "":
            cineast_config_dict['api']['thumbnailLocation'] = server_config_data.thumbnails_base_path_str
            if server_config_data.custom_content_import:
                cineast_config_dict['api']['objectLocation'] = server_config_data.shared_volume_base_path_str
            else:
                cineast_config_dict['api']['objectLocation'] = server_config_data.server_content_base_path_str
        else:
            print("!!! Thumbnails or Content base location is empty in the main config file !!!")
            raise ValueError

        all_predictors_address = [predictor['apiAddress'].rsplit('/', 1)[0] for predictor in
                                  cineast_config_dict['aestheticPredictorsConfig']]
        active_predictors_index = cineast_config_dict['activePredictors']
        self.active_predictors_address = [all_predictors_address[active_predictor_index - 1] + '/is_model_ready' for active_predictor_index
                                          in active_predictors_index]

        json_manager.store_dict_to_json(server_config_data.cineast_config_abs_path, cineast_config_dict)

        cineast_job_dict = json_manager.get_dict_from_json(server_config_data.cineast_job_abs_path)

        cineast_job_dict['exporters'][0]['properties']['destination'] = server_config_data.thumbnails_base_path_str

        json_manager.store_dict_to_json(server_config_data.cineast_job_abs_path, cineast_job_dict)

    def _update_cineast_jar_file(self, server_config_data):
        cineast_jar_file_path = server_config_data.base_path / ('cineast/' + self.__cineast_api_jar_name)
        download_file_from_url(server_config_data.cineast_jar_url, cineast_jar_file_path, over_write=True)

    def __update_job_file(self, content_to_extract_path):
        json_dict = json_manager.get_dict_from_json(self.__cineast_job_file_str)

        json_dict['input']['path'] = content_to_extract_path

        json_manager.store_dict_to_json(self.__cineast_job_file_str, json_dict)

    def __extract_from_cineast(self, setup):
        if setup:
            super()._run_command_on_process("setup --extraction " + self.__cineast_job_file_str)
        super()._run_command_on_process("extract --extraction " + self.__cineast_job_file_str)

    def extract_content_to_database(self, content_to_extract_path, setup):
        exception_occurred = False
        try:
            self.__update_job_file(content_to_extract_path)
            self.__extract_from_cineast(setup)

            super()._communicate_with_process()

            super()._start_process()
        except Exception as e:
            exception_occurred = True
            print(str(e))
        finally:
            if exception_occurred or self.__has_error_occurred_during_extraction():
                print("Finished extraction with errors. See cineast log file for more information!")
            else:
                print("Finished extraction successfully")
            return exception_occurred

    def __has_error_occurred_during_extraction(self):
        with open(self.process_log_file_path_str, 'r') as cineast_log_file_to_read:
            string_to_search = "EXTRACTION-ERROR for table"
            cineast_log_file_to_read = reversed(list(cineast_log_file_to_read))
            for line in cineast_log_file_to_read:
                if string_to_search in line:
                    return True
            return False

    def get_active_predictors_address(self):
        return self.active_predictors_address
