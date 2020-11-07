import json


class ServerConfigData:

    def __init__(self, base_path):
        base_path_str = str(base_path.absolute())
        config_file_path = base_path / 'vitrivr_paths_config_new.json'
        with config_file_path.open() as json_paths_file:
            data = json.load(json_paths_file)
            self.shared_volume_base_path_str = data['shared_volume_base']
            self.server_content_base_path_str = self.__join_paths(self.shared_volume_base_path_str, data[
                'content_base'])  # self.shared_volume_base_path_str + '/' + data['content_base']
            self.thumbnails_base_path_str = self.__join_paths(self.shared_volume_base_path_str, data[
                'thumbnails_base'])  # self.shared_volume_base_path_str + '/' + data['thumbnails_base']
            self.cineast_base_path_str = self.__join_paths(base_path_str, data[
                'cineast_base'])  # base_path_str + '/' + data['cineast_base']
            self.cineast_shared_config_path_str = self.__join_paths(self.shared_volume_base_path_str,
                                                                    data['cineast_shared_config'])
            self.cineast_job_abs_path = self.__join_paths(self.cineast_shared_config_path_str, data[
                'cineast_job_file'])  # self.cineast_base_path_str + '/' + data['cineast_job_file']
            self.cineast_config_abs_path = self.__join_paths(self.cineast_shared_config_path_str, data[
                'cineast_config_json'])  # self.cineast_base_path_str + '/' + data['cineast_config_json']
            self.cottontail_base_path_str = self.__join_paths(base_path_str, data[
                'cottontail_base'])  # base_path_str + '/' + data['cottontail_base']
            self.cottontail_shared_config_path_str = self.__join_paths(self.shared_volume_base_path_str,
                                                                       data['cottontail_shared_config'])
            self.cottontail_config_abs_path = self.__join_paths(self.cottontail_shared_config_path_str, data[
                'cottontail_config_json'])  # self.cottontail_base_path_str + '/' + data['cottontail_config_json']

    def __join_paths(self, path1, path2):
        return path1 + '/' + path2
