FROM ubuntu:bionic

MAINTAINER Matthew Vaughn <opensource@tacc.cloud>

# Install base utils
RUN apt-get update && apt-get install -y \
    build-essential \
    locales \
    curl \
    git \
    vim \
    sudo \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install pipenv
RUN pip3 install --no-cache-dir pipenv

RUN mkdir -p /dc-cli
WORKDIR /dc-cli

COPY . /dc-cli
RUN pipenv install --system --deploy
