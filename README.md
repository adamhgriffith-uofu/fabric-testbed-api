# FABRIC Python API

## Configure FABlib Application

Copy-paste `./fabric_config/fabric_rc.tmpl` to `./fabric_config/fabric_rc` and fill in the placeholder values. Finally, load the variables into the current Bash session:

```shell
source ./fabric_config/fabric_rc.py
```

## Bastion Key

Download your Bastion SSH key from the [Fabric Portal](https://portal.fabric-testbed.net/experiments#sshKeys) to `./fabric_config/fabric-bastion-key` and execute the following:

```shell
chmod 600 ${FABRIC_BASTION_KEY_LOCATION}
```

## Set SLICE Key Pair

```shell
ssh-keygen -t rsa -b 3072 -f ${FABRIC_SLICE_PRIVATE_KEY_FILE} -q -N ""
```