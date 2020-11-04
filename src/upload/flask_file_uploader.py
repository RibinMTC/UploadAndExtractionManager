import imghdr
import os
from pathlib import Path

from flask import Flask, render_template, request
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from src.extraction.cineast_and_cottontail_manager import CineastAndCottontailManager
from src.extraction.user_images_to_server_storer import get_new_import_folder_path_str
from src.utils.server_config_data import ServerConfigData

base_path = Path(__file__).parent.parent.parent

template_dir = base_path / 'templates'
app = Flask(__name__, template_folder=template_dir)

# Todo: Allow also upload of video input
app.config.update(
    UPLOAD_EXTENSIONS=['.jpg', '.png', '.gif'],
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_PARALLEL_UPLOADS=200
)

dropzone = Dropzone(app)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


def secure_file_upload(uploaded_file, server_upload_path_str):
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(server_upload_path_str + '/' + filename)
    return '', 204


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        new_import_folder_path_str = get_new_import_folder_path_str(server_content_base_path)
        num_of_files_to_extract = 0
        for key, f in request.files.items():
            if key.startswith('file'):
                secure_file_upload(f, new_import_folder_path_str)
                num_of_files_to_extract += 1
        cineast_and_cottontail_manager.start_extraction(new_import_folder_path_str, num_of_files_to_extract, True)
    return render_template('index_dropzone.html')


def create_directories_if_not_exists(directory_abs_path):
    if not os.path.exists(directory_abs_path):
        os.makedirs(directory_abs_path)
        print("Created folder: " + directory_abs_path)


serverConfigData = ServerConfigData(base_path)
server_content_base_path = Path(serverConfigData.server_content_base_path_str)
create_directories_if_not_exists(serverConfigData.server_content_base_path_str)
create_directories_if_not_exists(serverConfigData.thumbnails_base_path_str)
cineast_and_cottontail_manager = CineastAndCottontailManager(serverConfigData)

if __name__ == '__main__':
    app.run(debug=False, threaded=False, port=5003, host='0.0.0.0')
