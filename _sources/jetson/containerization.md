# Containerization

## Pre-reading

- [Docker overview](https://docs.docker.com/get-started/overview/)

### Objectives

- Describe the difficulties with dependency management
- Explain what a container is and how it is different from a virtual machine
- Demonstrate how to build an image from `Dockerfile` and run the image as a container.

## The Lesson

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

### What is containerization?

Virtual machines run **a complete operating system–including its own kernel–** on top of a hypervisor.

![Virtual machine architecture](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/media/virtual-machine-diagram.svg)

In contrast, **containers build on top of the host operating system's kernel.**

![Container architecture](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/media/container-diagram.svg)

Both offer benefits with isolation and portability, however there are [some key differences](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/containers-vs-vm#containers-vs-virtual-machines-1).

### Docker

Docker has *completely revolutionized* the way the world operates software applications.

- **Docker Inc.** is an American company that offers products such as Docker Hub and Docker Desktop.
- **[Docker Hub](https://hub.docker.com/)** is a *container registry* (`docker.io`). There are thousands of community and officially sponsored images; you can also upload your own images.
- **[NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com)** is a container registry (`nvcr.io`) for GPU accelerated containers.
- **Docker Engine](https://docs.docker.com/engine/)** is an open source project for running containers. It is part of the [Moby Project](https://github.com/moby/moby), which is an open source upstream of Docker Enterprise Edition.

![docker future](https://thinkr.fr/wp-content/uploads/2019/07/back-to-the-future-docker.jpg)

#### Docker Engine

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

```{note}
[Podman](https://podman.io/) is a Docker alternative that is sponsored by Red Hat. It is part of the Open Container Initiative (OCI).

Podman has several advantages over Docker, including a fork-exec model
instead of a daemon and the ability to run rootless.

It is also available in the default Debian 11 (Ubuntu 22.04) and later **apt** repositories.

You can effectively `alias docker=podman`.

Together with [buildah](https://buildah.io/) and [skopeo](https://github.com/containers/skopeo) you can do everything Docker can and more.

Overall, I like podman better... but that's not the way the industry is leaning ☹️
```

### Build Dockerfile

What if you want to customize your container?

Remember **containers are supposed to be immutable** so
you shouldn't modify them while running.

Instead, you can build your own custom container!

Create a file named `Dockerfile`, such as the example below
and then build image and run the container.

```dockerfile
# Example to add a package and change the default command
# Build with `docker build -t alpine-pubip .`
# Run with `docker run --rm alpine-pubip` to display host public IP address
# Run with `docker run --rm -it alpine-pubip /bin/sh` to launch shell
FROM alpine:3

RUN apk add curl

CMD ["/usr/bin/curl", "-s", "ifconfig.me"]

```

The `-t` flag specifies the flag with which you wish to name your new image.

```{tip}
By default, `build` looks at all the files in a directory.
To minimize file size, put your Dockerfile in a directory that only has what you need.
```

After building the image you can push it to a container registry.
Then you can pull it to somewhere else!

## Tensorflow on Jetson

NVIDIA builds and publishes ML containers optimized for GPU acceleration.
They can be found at [NVIDIA NCG Catalog](https://catalog.ngc.nvidia.com/containers).

Here is a Hello World for GPU acceleration on the Jetson Orin Nano:

#### Hello World

Browse to [Tensorflow Container for Jetson and Jetpack](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow).
Read the page and check to make sure version match up.

Pull the image... it's several GB...

```bash
sudo docker pull nvcr.io/nvidia/l4t-tensorflow:r35.3.1-tf2.11-py3
```

Run the container and start an interactive session.

```bash
sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-tensorflow:r35.3.1-tf2.11-py3
```

Now, inside the container, we'll run an excerpt from the Hello Colab script.

The script is hosted [as a gist](https://gist.github.com/byarbrough/442209e580349fd55f839e4d23e8794d).

```bash
# Will download the script into the container
curl -LO https://gist.githubusercontent.com/byarbrough/442209e580349fd55f839e4d23e8794d/raw/b10c21f10996732929b690e464e8ab468067059a/tf_gpu_hello.py
# Verify it, because we don't blindly trust things
less tf_gpu_hello.py
# Run it
python3 tf_gpu_hello.py
```

Or copy and paste from the gist.
