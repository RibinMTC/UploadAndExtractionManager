import time

from src.extraction.base_subprocess_manager import SubprocessManager
import src.utils.json_writer as json_manager


class CottontailManager(SubprocessManager):

    def __init__(self, server_config_data):
        self._setup_config(server_config_data)
        cottontail_start_cmd = "java -jar cottontaildb-1.0-SNAPSHOT-all.jar " + server_config_data.cottontail_config_abs_path
        super().__init__(server_config_data.cottontail_base_path_str, cottontail_start_cmd)
        print(self.process_log_file_path_str)

    def _setup_config(self, server_config_data):
        cottontail_config_dict = json_manager.get_dict_from_json(server_config_data.cottontail_config_abs_path)

        cottontail_config_dict['root'] = server_config_data.shared_volume_base_path_str + '/cottontaildb-data'

        json_manager.store_dict_to_json(server_config_data.cottontail_config_abs_path, cottontail_config_dict)

    def __count_elements_in_table(self, table_name):
        super()._run_command_on_process("count cineast " + table_name)

    def __get_count_from_log_file(self):
        with open(self.process_log_file_path_str, 'r') as cottontail_log_file_to_read:
            string_to_search = "longData:"
            cottontail_log_file_to_read = reversed(list(cottontail_log_file_to_read))
            for line in cottontail_log_file_to_read:
                if string_to_search in line:
                    count = int(line.split(':')[1])
                    return count
            return -1

    def count_elements_in_table(self, table_name):
        exception_occurred = False
        count = -1
        try:
            self.__count_elements_in_table(table_name)
            time.sleep(2)
            count = self.__get_count_from_log_file()
            if count is None or count == -1:
                count = 0
        except:
            exception_occurred = True
        finally:
            if exception_occurred:
                print("Finished table element counting with errors!")
            else:
                print("Table " + table_name + " contains " + str(count) + " elements")

        return count
