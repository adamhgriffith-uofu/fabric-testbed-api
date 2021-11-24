# syntax=docker/dockerfile:1
FROM python:3.9.9-buster

# Docker image arguments:
ARG username=fabric

# Install remaining packages:
COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt
RUN python -m bash_kernel.install

# Set the SSH private key:
COPY ./ssh/id_rsa ./.ssh/id_rsa_fabric
RUN chown ${username}:${username} ./.ssh/id_rsa_fabric

# Set the user:
RUN useradd -ms /bin/bash ${username}
WORKDIR /home/${username}

# Switch to SLATE API user:
USER ${username}

# Configuring git:
RUN git config --global user.email "horkle@snorkle.com" && \
    git config --global user.name "Horkle Snorkle Porkchop"

# Volumes:
VOLUME /access
VOLUME /work

# Ports:
EXPOSE 8888/tcp

# Run once the container has started:
COPY ./entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]