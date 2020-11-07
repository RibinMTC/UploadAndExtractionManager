from src.extraction.base_subprocess_manager import SubprocessManager
import src.utils.json_writer as json_manager


class CineastManager(SubprocessManager):

    def __init__(self, server_config_data):
        self.__cineast_job_file_str = server_config_data.cineast_job_abs_path
        self._setup_config(server_config_data)
        cineast_start_cmd = "java -jar cineast-api-3.0.1-full.jar " + server_config_data.cineast_config_abs_path
        super().__init__(server_config_data.cineast_base_path_str, cineast_start_cmd)

    def _setup_config(self, server_config_data):
        cineast_config_dict = json_manager.get_dict_from_json(server_config_data.cineast_config_abs_path)

        if server_config_data.thumbnails_base_path_str != "" and server_config_data.server_content_base_path_str != "":
            cineast_config_dict['api']['thumbnailLocation'] = server_config_data.thumbnails_base_path_str
            cineast_config_dict['api']['objectLocation'] = server_config_data.server_content_base_path_str
        else:
            print("!!! Thumbnails or Content base location is empty in the main config file !!!")
            raise ValueError

        json_manager.store_dict_to_json(server_config_data.cineast_config_abs_path, cineast_config_dict)

        cineast_job_dict = json_manager.get_dict_from_json(server_config_data.cineast_job_abs_path)

        cineast_job_dict['exporters'][0]['properties']['destination'] = server_config_data.thumbnails_base_path_str

        json_manager.store_dict_to_json(server_config_data.cineast_job_abs_path, cineast_job_dict)

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
            if exception_occurred:
                print("Finished extraction with errors!")
            else:
                print("Finished extraction successfully")
