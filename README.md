# Fabric Python API and Jupyter

> **_IMPORTANT:_** This repository requires a read-through of [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/) in order to make any sense.

Containerized Fabric Python API and Jupyter with SSH access.

## Requirements

### Dockerfile Arguments

The `Dockerfile` provides the following build arguments:

| Name       | Required | Description                                                  |
|------------|----------|--------------------------------------------------------------|
| `username` | Yes      | The Fabric API user name for Fabric and the Bastion servers. |

### SSH Key Files

> **_NOTE:_** All files added to `/<repo-location>/secrets/ssh` will be ignored by Git so don't worry :).

* During the build process Docker will copy relevant SSH keys into the image.
* Please copy all required keys below to `/<repo-location>/secrets/ssh` before building the images.

| Name                      | Required | Description                                                                                                                       |
|---------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| `id_rsa_fabric`           | Yes      | Counterpart to the public key for Fabric and the Bastion servers.                                                                 |
| `id_rsa_fabric_slice`     | No       | Counterpart to the public key used when the slice is defined and requested. If not specified a new private key will be generated. |
| `id_rsa_fabric_slice.pub` | No       | Counterpart to the private key used when the slice is defined and requested. If not specified a new public key will be generated. |

## Build and Run

### Production

Build the Docker image with production `build-arg`s:

```shell
docker build --file Dockerfile --build-arg username=<username> --tag fabric-api:prod .
```

Running the image will create a new tagged container and start up Jupyter.

```shell
[your@localmachine ~]$ docker run -it -p 8888:8888 -v /<repo-location>/work:/work fabric-api:prod
[I 19:58:14.368 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 19:58:14.632 NotebookApp] Serving notebooks from local directory: /work
[I 19:58:14.632 NotebookApp] Jupyter Notebook 6.4.6 is running at:
[I 19:58:14.632 NotebookApp] http://1234abc:8888/?token=asdfasdfasdf
[I 19:58:14.632 NotebookApp]  or http://127.0.0.1:8888/?token=asdfasdfasdf
[I 19:58:14.632 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 19:58:14.637 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-30-open.html
    Or copy and paste one of these URLs:
        http://1234abc:8888/?token=asdfasdfasdf
     or http://127.0.0.1:8888/?token=asdfasdfasdf
```
