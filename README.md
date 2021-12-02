# Fabric Python API and Jupyter

> **_IMPORTANT:_** This repository requires a read-through of [Install the FABRIC Python API](https://learn.fabric-testbed.net/knowledge-base/install-the-python-api/) in order to make any sense.

Containerized Fabric Python API with Jupyter and SSH.

## Requirements

### Dockerfile Arguments

The `Dockerfile` provides the following build arguments:

| Name           | Required | Description                                                                                                                                                                                     |
|----------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `jupytertheme` | No       | The theme for the Jupyter notebook environment. If not specified this will be set to `monokai`. See [jupyterthemes](https://github.com/dunovank/jupyter-themes) for a list of available themes. |
| `username`     | Yes      | The Fabric API user name for Fabric and the Bastion servers.                                                                                                                                    |

### SSH Key Files

> **_NOTE:_** All files added to `/<repo-location>/secrets/ssh` will be ignored by Git so don't worry :).

* During the build process Docker will copy relevant SSH keys into the image.
* Please copy all required keys below to `/<repo-location>/secrets/ssh` before building the images.

| Name                      | Required | Description                                                                                                                                  |
|---------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `id_rsa_fabric`           | Yes      | Counterpart to the public key for Fabric and the Bastion servers.                                                                            |
| `id_rsa_fabric_slice`     | No       | Counterpart to the public key used when the slice is defined and requested. If not specified a new private key will be generated on the fly. |
| `id_rsa_fabric_slice.pub` | No       | Counterpart to the private key used when the slice is defined and requested. If not specified a new public key will be generated on the fly. |

* **Optional:** Create your own persistent slice keys:

  ```shell
  ssh-keygen -b 2048 -t rsa -f "/<repo-location>/secrets/ssh/id_rsa_fabric_slice" -q -N ""
  ```

## Build and Run

### Production

Build the Docker image with production `build-arg`s:

```shell
docker build --file Dockerfile --build-arg username=<username> --tag fabric-api:prod .
```

Running the image will create a new tagged container and start up Jupyter.

```shell
[your@localmachine ~]$ docker run -it -p 8888:8888 -v /<repo-location>/work:/work fabric-api:prod
Existing Slice key not found.
Generating /root/.ssh/id_rsa_fabric_slice key pair on the fly...
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

## SSH Commands

The `username` and API SSH keys are already applied to `~/.ssh/config` in a standard way. The upshot is that lengthy commands like the following are no longer necessary.

```shell
ssh -i /path/to/key -J <username>@<bastion-hostname> -i /path/to/another/key <username>@<endpoint-hostname>
```

Instead, make use of the shorter command below using any of the predefined SSH hosts.

```shell
ssh <ssh-host>
```

| SSH Hosts             | Description                       |
|-----------------------|-----------------------------------|
| `fabric-bastion-host` | External Fabric SSH Bastion host. |

* Not all Bastion hosts allow direct login. This is expected behavior.

## Persistent Bash History

The `bash` history  is stored in `/work/.bash_history_docker`.
* If `/work` has been specified as a volume the history will persist between containers.

```shell
[root@123 ~]# history
    1  echo 'hello world'
    2  ls -al
    3  exit
    4  history
    5  exit
    6  history
```