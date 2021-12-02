# syntax=docker/dockerfile:1
FROM python:3.9.9-buster

# Docker image arguments:
ARG jupytertheme=monokai
ARG username

# Docker container environmental variables:
ENV FABRIC_API_USER=${username}
ENV FABRIC_ENV=prod
ENV HISTFILE=/work/.bash_history_docker
ENV JUPYTER_THEME=${jupytertheme}

# Install remaining packages:
COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt
RUN python -m bash_kernel.install

# Prepare entrypoint:
COPY ./docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

# Create the docker directory:
RUN mkdir /docker

# Add the SLATE API envs:
COPY ./envs ./docker/envs

# Add the scripts:
COPY ./scripts ./docker/scripts
RUN chmod +x ./docker/scripts/yml.sh

# Change working directory:
WORKDIR /root

# Set the SSH keys:
COPY ./secrets/ssh ./.ssh/
RUN chmod 600 -R ./.ssh/

# Set the work directory:
RUN mkdir /work

# Volumes
VOLUME [ "/work" ]

# Ports:
EXPOSE 8888/tcp

# Run once the container has started:
ENTRYPOINT [ "/docker-entrypoint.sh" ]
