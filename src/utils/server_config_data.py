import json


class ServerConfigData:

    def __init__(self, base_path):
        base_path_str = str(base_path.absolute())
        config_file_path = base_path / 'vitrivr_paths_config_new.json'
        with config_file_path.open() as json_paths_file:
            data = json.load(json_paths_file)
            self.shared_volume_base_path_str = data['shared_volume_base']
            self.server_content_base_path_str = self.shared_volume_base_path_str + '/' + data['content_base']
            self.thumbnails_base_path_str = self.shared_volume_base_path_str + '/' + data['thumbnails_base']
            self.cineast_base_path_str = base_path_str + '/' + data['cineast_base']
            self.cineast_job_abs_path = self.cineast_base_path_str + '/' + data['cineast_job_file']
            self.cineast_config_abs_path = self.cineast_base_path_str + '/' + data['cineast_config_json']
            self.cottontail_base_path_str = base_path_str + '/' + data['cottontail_base']
            self.cottontail_config_abs_path = self.cottontail_base_path_str + '/' + data['cottontail_config_json']
