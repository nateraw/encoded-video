FROM debian:latest
LABEL maintainer="naterawdata@gmail.com"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    git \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    wget \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    lib32z1-dev \
    vim \
    python-dev \
    pkg-config \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev


# General dependencies
# RUN apt-get install -y python-dev pkg-config

# Library components
# RUN apt-get install -y \
#     libavformat-dev libavcodec-dev libavdevice-dev \
#     libavutil-dev libswscale-dev libswresample-dev libavfilter-dev

# Install conda
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV CONDA_INSTALLER="Miniconda3-4.5.11-Linux-x86_64.sh"

RUN wget --quiet --no-check-certificate https://repo.continuum.io/miniconda/${CONDA_INSTALLER} && \
    /bin/bash /${CONDA_INSTALLER} -f -b -p $CONDA_DIR && \
    rm ${CONDA_INSTALLER} && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh

# Make requirements accessible to container
COPY requirements.txt /tmp/

# Install specific python version and dependencies
ARG python_version=3.7
RUN conda install -y python=${python_version} && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Add a pythonpath - gives python context to workdir
ENV PYTHONPATH=/src/workspace

WORKDIR /src/workspace/

# Copy over entire source dir to workspace
COPY . /src/workspace/

# Install package
RUN python setup.py develop

CMD ["/bin/bash"]