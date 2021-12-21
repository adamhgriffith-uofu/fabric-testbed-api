#!/bin/bash

# Enable strict mode:
set -euo pipefail

# Create the bash history file if necessary:
if [ ! -f "$HISTFILE" ]
then
  touch /work/.bash_history_docker
fi

# Load environmental values:
source "/docker/scripts/yml.sh"
create_variables "/docker/envs/${FABRIC_ENV}.yml" "conf_"
export FABRIC_BASTION_HOST="${conf_fabric_bastion_hostname}"
export FABRIC_BASTION_HOST_PRIV_IPV4="${conf_fabric_bastion_private_ipv4}"
export FABRIC_BASTION_HOST_PRIV_IPV6="${conf_fabric_bastion_private_ipv6}"
export FABRIC_CREDMGR_HOST="${conf_fabric_credmgr_hostname}"
export FABRIC_ORCHESTRATOR_HOST="${conf_fabric_orchestrator_hostname}"

# Create the SSH configuration file:
cat > "$HOME/.ssh/config" <<EOF
### Global Settings
StrictHostKeyChecking no
UserKnownHostsFile /dev/null

### The External FABRIC Bastion host
Host fabric-bastion-host
  HostName ${conf_fabric_bastion_hostname}
  IdentitiesOnly yes
  IdentityFile /root/.ssh/id_rsa_fabric
  Port ${conf_fabric_bastion_port}
  User ${FABRIC_API_USER}
EOF

# Create Slice key files:
if [ ! -f "/root/.ssh/id_rsa_fabric_slice" ]
then
  echo "Existing Slice key not found."
  echo "Generating $HOME/.ssh/id_rsa_fabric_slice key pair on the fly..."
  ssh-keygen -b 2048 -t rsa -f "$HOME/.ssh/id_rsa_fabric_slice" -q -N ""
fi

# Set up the examples:
if [ -d "/work/examples" ]
then
  rm -rf "/work/examples"
fi
cp -rfp /docker/examples /work/examples

# Start up Jupyter:
if [ $JUPYTER_THEME != "none" ]
then
  jt -t $JUPYTER_THEME
fi
jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --notebook-dir=/work