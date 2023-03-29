FROM "mcr.microsoft.com/devcontainers/python:0-3.11"
# Install the xz-utils package
RUN apt-get update && apt-get install -y xz-utils

## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip
# Install production dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt