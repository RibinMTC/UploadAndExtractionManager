import json


class ServerConfigData:
    """
    This class stores the configuration data from the vitrivr_pipeline_config.json file.
    """

    def __init__(self, base_path, config_file_path):
        base_path_str = str(base_path.absolute())
        self.base_path = base_path
        config_file_path = base_path / config_file_path
        with config_file_path.open() as json_paths_file:
            data = json.load(json_paths_file)
            upload_import_volume_base_path_str = data['upload_import_volume_base']
            custom_import_volume_base_path_str = data['custom_import_volume_base']

            self.custom_content_import = data['custom_content_import']
            if self.custom_content_import:
                self.shared_volume_base_path_str = custom_import_volume_base_path_str
                self.custom_content_folder_path = self.__join_paths(self.shared_volume_base_path_str,
                                                                    data['content_base'])
            else:
                self.shared_volume_base_path_str = upload_import_volume_base_path_str

            self.server_content_base_path_str = self.__join_paths(self.shared_volume_base_path_str, data[
                'content_base'])
            self.thumbnails_base_path_str = self.__join_paths(self.shared_volume_base_path_str, data[
                'thumbnails_base'])

            self.cineast_base_path_str = self.__join_paths(base_path_str, data[
                'cineast_base'])
            self.cineast_job_abs_path = self.__join_paths(self.cineast_base_path_str, data[
                'cineast_job_file'])
            self.cineast_config_abs_path = self.__join_paths(self.cineast_base_path_str, data[
                'cineast_config_json'])

            self.cottontail_base_path_str = self.__join_paths(base_path_str, data[
                'cottontail_base'])
            self.cottontail_config_abs_path = self.__join_paths(self.cottontail_base_path_str, data[
                'cottontail_config_json'])

            self.update_cineast_jar_file = data['update_cineast_jar']
            self.cineast_jar_url = data['cineast_jar_url']
            self.cineast_job_url = data['cineast_job_file_url']

            self.cottontail_jar_url = data['cottontail_jar_url']

            self.supported_content_types = data['supported_content_types']

            self.execute_feature_extraction = data['execute_feature_extraction']




    def __join_paths(self, path1, path2):
        return path1 + '/' + path2
