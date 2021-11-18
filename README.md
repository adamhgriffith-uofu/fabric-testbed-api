# Docker and the Fabric Testbed Jupyter Examples

> **_NOTE:_** This repository requires a readthrough of [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/) in order to make any sense.

## Environmental Variables

The ``Dockerfile`` provides the following environmental variables.

| Name | Description |
| ---  | ---         |
| BASTION_PRIVATE_KEY | The SSH private key related to the public key sent to the Fabric team for SSH Bastion access (see [Create Token](https://portal.fabric-testbed.net/experiments)). |
| CILOGON_REFRESH_TOKEN | Fabric's identity token is used to generate this refresh token with a much shorter lifespan (see [Create Token](https://portal.fabric-testbed.net/experiments)). |
| FABRIC_CREDMGR_HOST | See [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/#configure-the-environment). |
| FABRIC_TOKEN_LOCATION | See [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/#configure-the-environment). |
| FABRIC_ORCHESTRATOR_HOST | See [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/#configure-the-environment). |

## Setup

Build the Docker image.

```shell
docker build --file Dockerfile --tag fabric-jupyter:latest .
```

Mount the `/access` and `/work` directories in this repository to the container and publish the Jupyter notebook server port.

```shell
docker run -it -p 8888:8888 -v /<repo-location>/access:/access -v /<repo-location>/work:/work
```

Follow the prompts to complete the SSH key generation.

Finally Jupyter in your web browser by clicking one of the URLs indicated in the console, e.g. [http://127.0.0.1:8888/?token=horklesnorkle](http://127.0.0.1:8888/?token=horklesnorkle).

## Next Steps

* Most Jupyter example notebooks reference key pairs in `~/.ssh/`. Not being sure how those are generated goofy files were created with `entrypoint.sh`.

* How and where `CILOGON_REFRESH_TOKEN` is created is still a mystery (see [Create Token](https://portal.fabric-testbed.net/experiments)).