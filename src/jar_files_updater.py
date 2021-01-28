import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from pathlib import Path

from src.utils.file_setup_util import download_file_from_url
from src.utils.server_config_data import ServerConfigData


if __name__ == '__main__':
    if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
        config_file_path = "vitrivr_pipeline_config.json"
    else:
        config_file_path = "vitrivr_pipeline_config_local.json"

    base_path = Path(__file__).parent.parent
    serverConfigData = ServerConfigData(base_path, config_file_path)

    cineast_api_jar_path = "cineast/cineast-api.jar"
    cineast_jar_file_path = serverConfigData.base_path / cineast_api_jar_path
    download_file_from_url(serverConfigData.cineast_jar_url, cineast_jar_file_path, over_write=True)

    cottontail_db_jar_path = "cottontail/cottontaildb-1.0-SNAPSHOT-all.jar"
    cottontail_db_jar_file_path = serverConfigData.base_path / cottontail_db_jar_path
    download_file_from_url(serverConfigData.cottontail_jar_url, cottontail_db_jar_file_path, over_write=True)
