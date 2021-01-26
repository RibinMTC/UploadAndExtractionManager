#!/bin/sh

python3 src/predictors_ready_checker.py
gunicorn --config gunicorn_config.py src.main_flask_app:app