import time

from src.extraction.base_subprocess_manager import SubprocessManager
import src.utils.json_writer as json_manager


class CottontailManager(SubprocessManager):
    """
    This class handles the setup and interaction with cottontail db via the subprocess module
    """

    def __init__(self, server_config_data):
        self._setup_config(server_config_data)

        cottontail_start_cmd = "java -jar cottontaildb-1.0-SNAPSHOT-all.jar " + server_config_data.cottontail_config_abs_path
        super().__init__(server_config_data.cottontail_base_path_str, cottontail_start_cmd)

    def _setup_config(self, server_config_data):
        cottontail_config_dict = json_manager.get_dict_from_json(server_config_data.cottontail_config_abs_path)

        cottontail_config_dict['root'] = server_config_data.shared_volume_base_path_str + '/cottontaildb-data'

        json_manager.store_dict_to_json(server_config_data.cottontail_config_abs_path, cottontail_config_dict)

        try:
            self.__feature_table_names = []
            self.__feature_print_names = []
            cineast_config_dict = json_manager.get_dict_from_json(server_config_data.cineast_config_abs_path)
            for aesthetic_predictor_config in cineast_config_dict['aestheticPredictorsConfig']:
                table_name = aesthetic_predictor_config['tableName']
                print_name = table_name.replace('_', ' ').title()
                self.__feature_table_names.append(table_name)
                self.__feature_print_names.append(print_name)
        except Exception as e:
            print(str(e))

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

    def __get_object__features_from_log_file(self, key_name):
        with open(self.process_log_file_path_str, 'r') as cottontail_log_file_to_read:
            data_started = False
            start_string = "Printed"
            end_string = "["
            fail_string = "Command execution failed"
            separator_string = ":"
            key_string = "key"
            feature_string = "feature"
            dict_current_value = ""
            dict_feature_name_to_value = {}
            cottontail_log_file_to_read = reversed(list(cottontail_log_file_to_read))
            for line in cottontail_log_file_to_read:
                if fail_string in line:
                    break
                if not data_started:
                    data_started = start_string in line
                    continue
                if end_string in line:
                    break

                if separator_string in line:
                    str_split = line.split(separator_string)
                    if len(str_split) != 2:
                        continue
                    name, value = str_split
                    if key_string in name:
                        if feature_string in value:
                            value = key_name
                        if value in dict_feature_name_to_value:
                            dict_feature_name_to_value[value].append(dict_current_value)
                        else:
                            dict_feature_name_to_value[value] = [dict_current_value]
                    else:
                        dict_current_value = value

            return dict_feature_name_to_value

    def get_all_aesthetic_attributes_of_object(self, object_id):
        features_dict = {}
        for table_name, feature_print_name in zip(self.__feature_table_names, self.__feature_print_names):
            super()._run_command_on_process("find cineast " + table_name + " -c id -v " + object_id)
            time.sleep(0.1)
            features_dict.update(self.__get_object__features_from_log_file(feature_print_name))

        features_dict = {key.replace('"', '').strip().capitalize(): ','.join(value).replace('"', '').strip() for key, value in features_dict.items()}
        features_dict.pop('Id', None)
        return features_dict

    def count_elements_in_table(self, table_name):
        exception_occurred = False
        count = -1
        try:
            self.__count_elements_in_table(table_name)
            time.sleep(2)
            count = self.__get_count_from_log_file()
            if count is None or count == -1:
                count = 0
        except Exception as e:
            exception_occurred = True
            print(str(e))
        finally:
            if exception_occurred:
                print("Finished table element counting with errors!")
            else:
                print("Table " + table_name + " contains " + str(count) + " elements")

        return count
