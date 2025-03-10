FROM ubuntu:20.04
FROM python:3.10-slim-buster


ARG NB_USER="sagemaker-user"
ARG NB_UID="1000"
ARG NB_GID="100"

RUN apt-get update

RUN apt-get install curl -y

RUN apt-get install unzip -y

# Install the AWS CLI:
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip
RUN ./aws/install

RUN useradd --create-home --shell /bin/bash --gid "${NB_GID}" --uid ${NB_UID} ${NB_USER}


RUN pip install --upgrade pip

RUN python3 -m pip install --no-cache-dir \
    'jupyterlab>=4.0.0,<5.0.0' \
    urllib3 \
    jupyter-activity-monitor-extension \
    --ignore-installed

# Verify versions
RUN python3 --version && \
    jupyter lab --version

USER ${NB_UID}

CMD jupyter lab --ip 0.0.0.0 --port 8888 \
    --ServerApp.base_url="/jupyterlab/default" \
    --ServerApp.token='' \
    --ServerApp.allow_origin='*'