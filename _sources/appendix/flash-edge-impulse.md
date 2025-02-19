# Flash Edge Impulse Firmware to Arduino

On your **Raspberry Pi** we will install edge-impulse-cli and arduino-cli.

Before doing anything, let's update the installed software.

```bash
sudo apt update && sudo apt upgrade -y
```

#### Edge Impulse CLI

Now do the relevant portions from the [Linux installation docs](https://docs.edgeimpulse.com/docs/tools/edge-impulse-cli/cli-installation#installation-linux-ubuntu-macos-and-raspbian-os).

Specifically,

- Install node
- Verify node version and path
- Install `edge-impulse-cli`

After installing you need to `exit` that terminal and open a new one.

Then verify it installed:

```bash
edge-impulse-daemon --version
```

#### Arduino CLI

Install `arduino-cli` according to [the docs](https://arduino.github.io/arduino-cli/1.1/installation/)

First, ensure `~/.local/bin` is on your PATH.

The environment variable `$PATH` is a list of directories that the OS will search for executables, *in order.*

```bash
# This shows your home directory, which uses the ~ symbol for short
# We expect it to be /home/pi/ by default, but it can be whatever!
echo $HOME

# This will print your current path.
# We expect to see ~/.local/bin/ towards the end,
# but instead of ~ it will be the result from the previous command
echo $PATH
```

We want to install the Arduino CLI to somewhere on our path. If we do `~/.local/bin` we don't need `sudo`.

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh
```

Verify installation

```bash
arduino-cli version
```

#### Dialout Group

Lastly, we need to add your user to the Linux dialout group.

```{note}
It took Capt Yarbrough two entire afternoons to figure out that this needs to be done 🫠
```

The dialout group grants users permissions to access serial ports and modems.
Our Arduino board and daemon will connect to the serial port in such a way that we'll need this.

```bash
sudo usermod -aG dialout $USER
```

Then reboot.

```bash
sudo reboot
```

Once logged back in, user `pi` (or whoever you are) should be in dialout group.

```bash
grep dialout /etc/group
```

### Arduino Firmware

Follow the instructions to [connect edge impulse to the Arduino Nano 33 BLE Sense](https://docs.edgeimpulse.com/docs/edge-ai-hardware/mcu/arduino-nano-33-ble-sense#id-1.-connect-the-development-board-to-your-computer).

Specifically, you need to **connect the board** and **update firmware.**
You don't strictly need to do the "setting keys" part, but it might be helpful.

![RESET to launch bootloader](https://docs.edgeimpulse.com/~gitbook/image?url=https%3A%2F%2F3586622393-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FGEgcCk4PkS5Pa6uBabld%252Fuploads%252Fgit-blob-c47c9b3fde5e9a23528f23e997f35a51c1e3be3e%252Fb302301-out.gif%3Falt%3Dmedia&width=768&dpr=2&quality=100&sign=347037cf&sv=2)

If successful you should see a message like

> Flashed your Arduino Nano 33 BLE development board.

```{tip}
You *can* do all of this on Raspberry Pi or you *can* do all of this on Windows.
But I've found that:

1. Installing node and these things on Windows is a bad idea.
2. Folks like to be able to take their board and laptop out of the lab and still do work.
```
