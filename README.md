## UploadAndExtractionManager

UploadAndExtractionManager is a python tool which offers the following functionalities:

1. Provides an upload webinterface to upload images and videos using DropzoneJS. Supported formats are: *jpg, png, mp4*.
2. Predicts aesthetic features for the uploaded content using the [Vitrivr-Pipline](https://vitrivr.org/). Specifically, *Cineast* retrieval engine and *CottontailDb* are used. The features to predict can be defined in the *cineast/cineast.json* file.
3. Provides stored aesthetic features for a given image or video, upon request from the *Vitrivr-webinterface*

### Requirements

This project requires Python 3.

### Installation

Clone this repository and install the project requirements:

```bash
pip install -r requirements.txt
```
 

### Usage

As this project depends on the Aesthetic Predictors defined in the *cineast.json* config file, it is not intended for an isolated usage.
For running the code locally, run the following command from the project's root directory:

```bash
gunicorn --config gunicorn_config.py src.main_flask_app:app
```