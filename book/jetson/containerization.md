# Containerization

## Pre-reading

- [Docker overview](https://docs.docker.com/get-started/overview/)

### Objectives

- Describe the difficulties with dependency management
- Explain what a container is and how it is different from a virtual machine
- Demonstrate how to build an image from `Dockerfile` and run the image as a container.

## Background

### Dependency Management

Managing dependencies is extremely challenging for complex projects.

The challenge is even greater when you have specific builds
trying to take advantage of hardware.

In Python a common approach is to use a [Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
# This will show system python
which python3

# Run the python venv module to create virtual environment
# Common names are env or .venv, but you can use anything
python3 -m venv env

# Tell terminal to use the venv. Should see a preceding (env) in terminal.
source env/bin/activate

# This will show venv python
which python3
```

We can then install python requirements specifically to this environment,
keeping them separate from other projects or from the system!

```{tip}
A `requirements.txt` file makes installing python libraries much easier.

`pip install -r requirements.txt`
```

But what if you have to build binaries?

And what about starting multiple processes?

And what about the the 15 things you had to do to get it working?

![ship your machine](https://pbs.twimg.com/media/FPKqqiFX0AMRBu4?format=png)

### Containerization?

Virtual machines run **a complete operating system–including its own kernel–** on top of a hypervisor.

![Virtual machine architecture](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/media/virtual-machine-diagram.svg)

In contrast, **containers build on top of the host operating system's kernel.**

![Container architecture](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/media/container-diagram.svg)

Both offer benefits with isolation and portability, however there are [some key differences](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/containers-vs-vm#containers-vs-virtual-machines-1).

## Docker

Docker has *completely revolutionized* the way the world operates software applications.

- **Docker Inc.** is an American company that offers products such as Docker Hub and Docker Desktop.
- [**Docker Hub**](https://hub.docker.com/) is a *container registry* (`docker.io`). There are thousands of community and officially sponsored images; you can also upload your own images.
- [**NVIDIA NGC Catalog**](https://catalog.ngc.nvidia.com) is a container registry (`nvcr.io`) for GPU accelerated containers.
- [**Docker Engine**](https://docs.docker.com/engine/)** is an open source project for running containers. It is part of the [Moby Project](https://github.com/moby/moby), which is an open source upstream of Docker Enterprise Edition.
- [**Podman**](https://podman.io/) is an Open Container Runtime that is a great alternative to Docker and is easily installed with apt, *but* doesn't have as good of GPU support.

![docker future](https://thinkr.fr/wp-content/uploads/2019/07/back-to-the-future-docker.jpg)

### Docker Engine

> Docker Engine is an open source containerization technology for building and containerizing your applications. Docker Engine acts as a client-server application with:
>
> - A server with a long-running daemon process `dockerd`.
> - APIs which specify interfaces that programs can use to talk to and instruct the Docker daemon.
> - A command line interface (CLI) client `docker`.
>
> The CLI uses Docker APIs to control or interact with the Docker daemon through scripting or direct CLI commands. Many other Docker applications use the underlying API and CLI. The daemon creates and manage Docker objects, such as images, containers, networks, and volumes.

You will largely interact with docker via the CLI.

See [Docker run reference](https://docs.docker.com/engine/reference/run/)

As an example, try

```bash
sudo docker run -it --rm alpine:latest
```

This will do a few things!

1. Pull the latest tag from [docker.io/alpine](https://hub.docker.com/_/alpine).
2. Save the image locally.
3. [Run](https://docs.docker.com/engine/reference/commandline/run/) the container (you need to familiarize yourself with the flags for this subcommand).
    - `-i` specifies interactive and keeps STDIN open
    - `-t` allocates a pseudo-TTY so you get things like autocompletion
    - `--rm` automatically removes the container when it exits
4. Enters you into the default process for the alpine container: `/bin/sh`.

Now, inside the alpine container, run

```bash
cat /etc/os/release
```

Next, open a new terminal and run

```bash
sudo docker ps
```

Type `exit` back in your alpine terminal and run `docker ps` again.
Now try `docker ps -a`.

## Container Lifecycle

A core benefit of containerization is that immutable images can be pre-built and then
distributed via container repositories. This means that complex installations just work!

```{figure} https://www.markbuckler.com/img/docker_high_level.png
The container lifecycle includes being built, pulled, pushed, run, and more.
```

### Container Repositories

A container repository just hosts built containers. The two we will use for this course are [DockerHub](https://hub.docker.com/) and [NVIDIA NCG Catalog](https://catalog.ngc.nvidia.com/containers).

You can **pull** an image:

```bash
sudo docker pull docker.io/python:latest
```

You can see what images you have locally:

```bash
sudo docker image ls
```

You can **push** an image as well:

```bash
docker image push docker.io/example/my-cool-container:latest
```

### Dockerfile Exercise

What if you want to customize your container?

Remember **containers are immutable and ephemeral**, so you generally don't modify them while running.

Instead, you can build your own custom container!

1. Make a new directory
2. In that directory create a file named `Dockerfile`\
3. Put this into the Dockerfile

```dockerfile
# Example to print your public IP address
FROM alpine:3

RUN apk add curl

ENTRYPOINT ["/usr/bin/curl", "-s", "ifconfig.me"]
```

4. Build the image

```bash
# -t specifies the name we want to give the tag
sudo docker buildx build -t mypub-ip .
```

```{tip}
By default, `build` looks at all the files in a directory
(that's why the `.` is important!)
To minimize file size, put your Dockerfile in a directory that only has what you need.
```

5. See that your image is now available

```bash
sudo docker image ls
```

6. Run the container

```bash
sudo docker run --rm mypub-ip
```

7. (Optional/hypothetical) Push your new image to Dockerhub

```bash
sudo docker push docker.io/your-username/mypub-ip:latest
```

8. (Optional/hypothetical) Pull your image to run as a container on a different computer!

```bash
# Notice that you don't need the Dockerfile anymore!
sudo docker pull docker.io/your-username/alpine-publicip:latest
```

## Ultralytics YOLO

```{note}
The instructor should demo this!
It's easy, but the image is large and takes time to pull.
```

Ultralytics publishes a Docker image that lets you run YOLO (You Only Look Once) object detection on your Jetson Orin Nano!

[Quick Start Guide: NVIDIA Jetson with Ultralytics YOLO11](https://docs.ultralytics.com/guides/nvidia-jetson/)

```bash
docker pull ultralytics/ultralytics:latest-jetson-jetpack6
```

Plug in a webcam, run this, and then click on the link it provides to open a browser!

```bash
docker run -it --rm --device=/dev/video0 --runtime=nvidia --ipc=host ultralytics/ultralytics:latest-jetson-jetpack6 yolo streamlist-predict
```
