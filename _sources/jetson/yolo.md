# YOLO

You Only Look Once object detection

## Pre-reading

- [How computers learn to recognize objects instantly](https://youtu.be/Cgxsv1riJhI)

### Objectives

- Run YOLO on the Jetson

## Howto

This is the YOLOv8 model architecture... it's really complex!

![YOLOv8 model architecture](https://blog.roboflow.com/content/images/2023/01/image-16.png)

So, let's be honest, there's a lot going on there that we don't understand.
*Fortunately*, [Ultralytics, who sponsors YOLOv8](https://docs.ultralytics.com/)
builds a Docker image: [ultralytics | Docker Hub](https://hub.docker.com/r/ultralytics/ultralytics)

### Steps

First, plug in a USB web cam.

Next, pull the image

```bash
docker pull ultralytics/ultralytics:latest-jetson
```

`cd` into a dedicated directory

Run the container

```bash
docker run -it --rm --runtime nvidia -v ./yolov5:/yolov5 --device /dev/video0:/dev/video0:mrw -e DISPLAY=:0 -v /tmp/.X11-unix/:/tmp/.X11-unix ultralytics/ultralytics:latest-jetson /bin/bash
```

Inside the container:

```bash
cd /yolov5/standard
```

Run the object detection. Source `0` refers to your webcam, which the OS is calling `video0` (hopefully).
Conf `0.5` sets confidence threshold to 0.5; you can raise or lower it depending on your needs.

This will take a while to load.
Then it will print detections to the screen.

Exit with `Ctrl+C` and wait for the video to save into the volume you provided.

```bash
python3 detect.py --source 0 --conf 0.5
```

How could you improve upon this?
