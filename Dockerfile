FROM ubuntu:18.04

MAINTAINER ribin chalumattu <cribin@inf.ethz.ch>

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt -y install python3 python3-pip \
    && apt-get install -y wget

# install java
RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install \
      default-jre-headless \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip

# set work directory
WORKDIR /uploadAndExtractionManager

# copy requirements.txt
COPY ./requirements.txt /uploadAndExtractionManager/requirements.txt

# install project requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

##get cineast jar and config files from git repo(forker cineast repo by ribin)
#RUN wget https://github.com/RibinMTC/cineast/blob/primitive-extraction-support/cineast-api/build/libs/cineast-api-3.0.1-full.jar -O /uploadAndExtractionManager/cineast/cineast-api-3.0.1-full.jar
#RUN wget https://github.com/RibinMTC/cineast/blob/primitive-extraction-support/cineast_deploy.json -O /uploadAndExtractionManager/cineast/cineast_deploy.json

# set app port
EXPOSE 5003 4567 4568 1865

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "src.upload.flask_file_uploader:app"]