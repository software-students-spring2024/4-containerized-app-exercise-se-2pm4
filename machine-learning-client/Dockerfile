# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-buster

# installation of libgl1-mesa-glx for deepface
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install\
    libgl1\
    libgl1-mesa-glx \ 
    libglib2.0-0 -y && \
    rm -rf /var/lib/apt/lists/* \
    pkg-config \
    libhdf5-dev \
    gcc
#install curl
RUN apt-get update && apt-get install -y curl
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Install pip requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /root/.deepface/weights 
RUN curl -L https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5 -o /root/.deepface/weights/facial_expression_model_weights.h5 && \
    curl -L https://github.com/serengil/deepface_models/releases/download/v1.0/age_model_weights.h5 -o /root/.deepface/weights/age_model_weights.h5 && \
    curl -L https://github.com/serengil/deepface_models/releases/download/v1.0/gender_model_weights.h5 -o /root/.deepface/weights/gender_model_weights.h5 && \
    curl -L https://github.com/serengil/deepface_models/releases/download/v1.0/race_model_single_batch.h5 -o /root/.deepface/weights/race_model_single_batch.h5
    

COPY . /app
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "mlc_deepface.py"]
