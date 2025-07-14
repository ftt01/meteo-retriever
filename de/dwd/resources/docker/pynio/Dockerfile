#
#   ref https://github.com/tebeka/pythonwise/blob/master/docker-miniconda/Dockerfile
#
#   miniconda vers: http://repo.continuum.io/miniconda
#   sample variations:
#     Miniconda3-latest-Linux-armv7l.sh
#     Miniconda3-latest-Linux-x86_64.sh
#     Miniconda3-py38_4.10.3-Linux-x86_64.sh
#     Miniconda3-py37_4.10.3-Linux-x86_64.sh
#
#   py vers: https://anaconda.org/anaconda/python/files
#   tf vers: https://anaconda.org/anaconda/tensorflow/files
#   tf-mkl vers: https://anaconda.org/anaconda/tensorflow-mkl/files
#

ARG UBUNTU_VER=18.04
ARG CONDA_VER=latest
ARG OS_TYPE=x86_64
# ARG PY_VER=3.8.11
# ARG TF_VER=2.5.0

FROM ubuntu:${UBUNTU_VER}

# System packages 
RUN apt-get update && apt-get install -yq curl wget jq vim

# Use the above args during building https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG CONDA_VER
ARG OS_TYPE
# Install miniconda to /miniconda
RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh"
RUN bash Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -p /miniconda -b
RUN rm Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# ARG PY_VER
# ARG TF_VER
# Install packages from conda and downgrade py (optional).
# RUN conda install -c anaconda -y python=${PY_VER}
# RUN pip install pyyaml pandas
# RUN conda install -c anaconda -y \
    # tensorflow-mkl=${TF_VER} \
    # && pip install pyyaml pandas

RUN conda create --name pynio_env --channel conda-forge pynio
ENV PATH="/miniconda/envs/pynio_env/bin:$PATH"
RUN pip install xarray

COPY docker_extractor.py /home/pynio/docker_extractor.py
ENTRYPOINT ["python", "/home/pynio/docker_extractor.py"]

# TO RUN: docker run -it -v /home/daniele/documents/github/ftt01/phd/projects/hydrological_forecasting/:/home/hydrological_forecasting conda_test