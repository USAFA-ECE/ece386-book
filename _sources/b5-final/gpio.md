# Final: GPIO Checkpoint

For this checkpoint, you must prove that you can trigger an action by driving a GPIO pin to digital HIGH.

## Board Selection

You may use *either* the Jetson or the Raspberry Pi.

- If you use the **Jetson** you are required to run Docker to leverage the CUDA GPU.
    But the Jetson's GPIO cannot directly connect to CUDA so you must use BASH to read them (see {ref}`jetson-gpio`) and then tirgger an action in Docker.
- If you use the **Pi** you can use [`gpiozero`](https://github.com/gpiozero/gpiozero) to easily listen for a button press!
    But there is no GPU so you need to host Whisper on the DFEC server as an API.

## Deliverables

1. Conduct a BLERP analysis for voice recording and transcription.
2. Select a board (either Jetson or Pi)
3. Prove that you can use the GPIO on that board to trigger something *simple* (like printing to a screen)
    - A BASH action if using the Jetson
        - ideally, this in-turn triggers something in a Docker container
    - A Python action in a virtual environment if using the Pi
