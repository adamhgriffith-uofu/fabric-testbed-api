#!/bin/bash

# Enable strict mode:
set -euo pipefail

# Setting the hosts:
export FABRIC_CREDMGR_HOST=$(cat /access/hosts/FABRIC_CREDMGR_HOST)
export FABRIC_ORCHESTRATOR_HOST=$(cat /access/hosts/FABRIC_ORCHESTRATOR_HOST)

# Create key files?
ssh-keygen -t rsa -b 4096 -C "horkle@snorkle.com"

# Set up the Jupyter example notebooks:
if [ ! -d "/work/jupyter-examples" ]
then
  git clone https://github.com/fabric-testbed/jupyter-examples.git /work/jupyter-examples
  cd /work/jupyter-examples
else
  cd /work/jupyter-examples
  git stash
  git pull origin master
fi
jupyter notebook --no-browser --ip=0.0.0.0 --allow-root