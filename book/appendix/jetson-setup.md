# Jetson Setup

Instructions to setup the [**Jetson Orin Nano Super Developer Kit**](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/) 8GB DeveloperKit.

## Flash the Board

Flash the board using the SDK Manager on Ubuntu by following [these instructions](https://www.jetson-ai-lab.com/initial_setup_jon_sdkm.html)

Make sure to pay special attention to where the wire goes to launch into recovery mode
and to *uncheck* Jetson Runtime Components.

I also recommend changing OEM Configuration from Runtime to *Pre-Config* and setting a username and password.

## Software Update, Install, Configure

Once the board is flashed and you've disconnected the recovery mode jumper, run the following to:

1. Upgrade all installed apt packages
2. Install Docker with the [get docker convenience script](https://github.com/docker/docker-install)
3. Install and configure [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#configuring-docker)
4. Reboot

```bash
# Warning, this will execute a script from the Internet as sudo
sudo apt update && sudo apt upgrade -y && \
wget -qO- https://get.docker.com | sudo sh && \
sudo apt install nvidia-container-toolkit && \
sudo nvidia-ctk runtime configure --runtime=docker && reboot
```

## Get Started with GPU

To make sure your GPU is online and available on your Jetson, `nvidia-smi`
will tell you about your GPU and CUDA version.

```bash
nvidia-smi
```

A good test of docker is to run a [PyTorch container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch);
if the GPU is available to the container's Python environment it will output `True`; otherwise, `False`.

```bash
# Version compatible with Jetpack 6.2
sudo docker run -rm --runtime=nvidia --ipc=host nvcr.io/nvidia/pytorch:25.02-py3-igpu python -c "import torch; print(torch.cuda.is_available())"
```
