"""
Main flask module.
Module Responsibilities:
    1.  Provide an upload web interface( html template: templates/index_dropzone.html), onto which users can upload
        images to be extracted by cineast
    2.  Start cineast extraction upon image upload and upload content to virtual server, if desired.
    3.  Provide details(predicted aesthetic features) for a given segment(image or video segment) from the vitrivr-web-interface
"""
import imghdr
import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from src.extraction.cineast_and_cottontail_manager import CineastAndCottontailManager
from src.extraction.user_images_to_server_storer import get_new_import_folder_path_str
from src.utils.file_setup_util import get_num_of_files_in_directory
from src.utils.server_config_data import ServerConfigData

if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
    config_file_path = "vitrivr_pipeline_config.json"
    print("Using global config")
else:
    config_file_path = "vitrivr_pipeline_config_local.json"
    print("Using local config")

base_path = Path(__file__).parent.parent
serverConfigData = ServerConfigData(base_path, config_file_path)
server_content_base_path = Path(serverConfigData.server_content_base_path_str)

template_dir = base_path / 'templates'
app = Flask(__name__, template_folder=template_dir)

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE=','.join(serverConfigData.supported_content_types),
    DROPZONE_MAX_FILE_SIZE=50,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_PARALLEL_UPLOADS=200,
    DROPZONE_INVALID_FILE_TYPE="This file type is not supported.",
    DROPZONE_FILE_TOO_BIG="File is too big {{filesize}}. Max filesize: {{maxFilesize}}MB."
)

dropzone = Dropzone(app)


# def validate_image(stream):
#     header = stream.read(512)
#     stream.seek(0)
#     format = imghdr.what(None, header)
#     if not format:
#         return None
#     return '.' + (format if format != 'jpeg' else 'jpg')


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


def secure_file_upload(uploaded_file, server_upload_path_str):
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        # file_ext = os.path.splitext(filename)[1]
        # if file_ext not in serverConfigData.supported_content_types:
        #     return 'File type: ' + file_ext + ' is not supported', 400
        uploaded_file.save(server_upload_path_str + '/' + filename)
    return True


@app.route('/aesthetic_details/<object_id>', methods=['POST', 'GET'])
def get_aesthetic_details(object_id):
    test = cineast_and_cottontail_manager.get_object_feature_information(object_id)
    if not bool(test):
        return "No features could be found for this object"
    response = jsonify(test)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  # print_items(test)


def print_items(dict_to_print, indent=0):
    p = ['<ul>\n']
    for k, v in dict_to_print.items():
        if isinstance(v, dict):
            p.append('<li>' + k + ':')
            p.append(print_items(v))
            p.append('</li>')
        else:
            p.append('<li>' + k + ':')
            attributes_str = ','.join(v)
            p.append(attributes_str)
            p.append('</li>')
    p.append('</ul>\n')
    return '\n'.join(p)


@app.route('/', methods=['POST', 'GET'])
def upload():
    if serverConfigData.custom_content_import:
        return 'Upload is not available when importing custom content. Please set custom_content_import to false in the config file!', 400
    if request.method == 'POST':
        new_import_folder_path_str = get_new_import_folder_path_str(server_content_base_path)
        num_of_files_to_extract = 0
        for key, f in request.files.items():
            if key.startswith('file'):
                if secure_file_upload(f, new_import_folder_path_str):
                    num_of_files_to_extract += 1
        if num_of_files_to_extract > 0:
            cineast_and_cottontail_manager.start_extraction(new_import_folder_path_str,
                                                            num_of_files_to_extract, True)
    return render_template('index_dropzone.html')


cineast_and_cottontail_manager = CineastAndCottontailManager(serverConfigData)
cineast_and_cottontail_manager.setup_directories(serverConfigData)

if __name__ == '__main__':
    app.run(debug=False, threaded=False, port=5003, host='0.0.0.0')
