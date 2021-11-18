# syntax=docker/dockerfile:1
FROM python:3.9.9-buster

# Global variables:
ENV FABRIC_CREDMGR_HOST=cm.fabric-testbed.net
ENV FABRIC_ORCHESTRATOR_HOST=orchestrator.fabric-testbed.net

# Access management variables:
ENV BASTION_PRIVATE_KEY=/access/keys/id_rsa
ENV FABRIC_TOKEN_LOCATION=/access/tokens/fabric-identity-token.json
ENV CILOGON_REFRESH_TOKEN=/access/tokens/fabric-refresh-token.json

# Install remaining packages:
COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt
RUN python -m bash_kernel.install

# git config
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