# Networks and Tooling

## Pre-reading

- [Cloudflare: How does the Internet work?](https://www.cloudflare.com/learning/network-layer/how-does-the-internet-work/)

### Objectives

## Internet Protocol

A **network** usually refers to a collection of devices connected via the Internet Protocol.
The Internet Protocol was originally defined in [RFC 791](https://datatracker.ietf.org/doc/html/rfc791),
published by DARPA in 1981.

The entire IP stack involves several layers, and Electrical and Computer Engineers are commonly
concerned with the physical layer or the *link layer*
(which includes Ethernet - [IEEE 802.3](https://en.wikipedia.org/wiki/IEEE_802.3)
and Wi-Fi - [IEEE 802.11](https://en.wikipedia.org/wiki/IEEE_802.11)).

In this course we will route traffic between devices on the same local area network (LAN),
as well as across the big Internet!

### Address

Every device on the internet has an IP address. Usually this address if IPv4 and looks like four numbers between 0-255, separated by dots.

For examples, `192.168.1.40` is my current private IP address. `104.16.133.229` is Cloudflare.com's current IP address.

#### Subnet

IP addresses belong to subnets. For this class, all you need to know is that when you are connected to a Wi-Fi router you are (typically) on the same subnet as the other devices.
This means you can talk to those other devices, as long as the router doesn't block that traffic (which is common on guest networks).

The following [Private IPv4 address] are reserved for private use, meaning you won't see them on the big Internet.

- `192.168.0.0` – `192.168.255.255` (most common for home LAN)
- `172.16.0.0` – `172.31.255.255` (Docker defaults to one of these)
- `10.0.0.0` – `10.255.255.255` (more common on enterprise networks)

There is also the reserved loopback subnet `127.0.0.0/8`; packets never leave the device. Yes, it's okay to talk to yourself.

![There's no place like `127.0.0.1`](https://i.redd.it/rcokvkzk62a01.jpg)

**Because of scarcity of IP addressed (there are only about 4 billion) we have to reuse some; hence, private vs. public IP.**

You can find your private IP address with the following commands.
You may have multiple IP addresses, if you have multiple interfaces, such as ethernet, Wi-Fi, and loopback!

```bash
# Linux
ip a
```

```powershell
# Windows
ipconfig
```

You can find your public IP by searching "what is my IP" in a web browser.
You can also visit or curl one of the many dedicated websites.

```bash
curl ipconfig.io
```

Notice your IP is tied to a fairly precise physical location!

#### Domain

While all Internet-connected devices have an IP address, these addresses may change. Plus, it's difficult to remember more than a few IP addresses; but it's easy to remember a domain name!

Examples of domain names include `google.com` or `usafa.edu`.

Domain names are resolved to an IP address via a Domain Name Server (DNS) query.

> A computer's IP address is like the physical address of a house. If someone calls a pizzeria to order a delivery, they need to provide their physical address. Without that address, the pizza delivery person will have no idea which house to deliver the pizza to. ~ [Cloudflare: What is my IP address?](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/)

```{figure} https://cf-assets.www.cloudflare.com/slt3lc6tev37/54NvR4ArYd9isJUmbz5wbW/5abc7d8ece3a915683f8ed71d47ea28e/ddos-dns.svg

---
url: https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/
---
The DNS process for requesting the IP address of a web server.
```

You can conduct a DNS query with `nslookup`.

```bash
nslookup google.com
```

This should show you the IP address of your DNS server as well as the IPv4 and IPv6 address of Google!

**DNS carries major security concerns.**
Cloudflare provides the free, fast, and private DNS server `1.1.1.1`.

Cloudflare also provide alternate DNS addresses via [1.1.1.1 for Families](https://blog.cloudflare.com/introducing-1-1-1-1-for-families/), which blocks lots of malware and adult content!

```{tip}
DNS is a thing that frequently goes wrong with networking.
When debugging connectivity, try and do an nslookup and then try and access a website with the raw IP: `curl 1.1.1.1`.
```

### Port

If an IP address is like a physical building address, the port is like the room number.

> A port is a virtual point where network connections start and end. Ports are software-based and managed by a computer's operating system. Each port is associated with a specific process or service. Ports allow computers to easily differentiate between different kinds of traffic: emails go to a different port than webpages, for instance, even though both reach a computer over the same Internet connection. ~ [Cloudflare: What is a computer port?](https://www.cloudflare.com/learning/network-layer/what-is-a-computer-port/)

Only one process may bind a port at a time.
**There are 65,535 possible port numbers.** The first 1024 require sudo permissions to bind.

Here are some common well-known ports:

- **Port 22**: Secure Shell (SSH). SSH is one of many tunneling protocols that create secure network connections.
- **Port 53**: Domain Name System (DNS). DNS is an essential process for the modern Internet; it matches human-readable domain names to machine-readable IP addresses, enabling users to load websites and applications without memorizing a long list of IP addresses.
- **Port 80**: Hypertext Transfer Protocol (HTTP). HTTP is the protocol that makes the World Wide Web possible.
- **Port 443**: HTTP Secure (HTTPS). HTTPS is the secure and encrypted version of HTTP. All HTTPS web traffic goes to port 443. Network services that use HTTPS for encryption, such as DNS over HTTPS, also connect at this port.

You can view listening ports with

```bash
ss -tunlp
```

## Talking to Other Devices

The following are for Linux.
In your terminal, use the `man` command to get more information about each.

### Ping

Exactly what it sounds like! Sends an ICMP packet to try and bounce off an IP address.
Be aware that sometimes network admins block this.

```bash
ping 1.1.1.1
```

### SSH

Secure Shell (SSH) is the most common method for interactively sending commands between computers.
It commonly uses **port 22**. You can do both username/password and encryption key authentication
(key is preferred to password, as it is more secure and less typing).

```bash
# Example, assuming you have a Raspberry Pi listening
ssh pi@192.168.0.34
```

See [CloudFlare: What is SSH?](https://www.cloudflare.com/learning/access-management/what-is-ssh/)
or [DigitalOcean: How To Use SSH to Connect to a Remote Server](https://www.digitalocean.com/community/tutorials/how-to-use-ssh-to-connect-to-a-remote-server).

#### SCP

Secure Copy (SCP) uses SSH to transfer files between devices.

```bash
# From me to them
scp my_file pi@192.168.0.37:/home/pi/their_new_file

# From them to me
scp pi@192.168.0.37:/home/pi/their_file my_new_file
```

```{note}
For large files (such as datasets) or for files where changes are copied (such as remote backups)
`rsync` is preferred. Basic `rysnc` usage is the same syntax as `scp`.
```

### HTTP Requests

You can make an HTTP request with `curl` or `wget`.
See `man curl` or `man wget` for more options (such as how to save output to a file).

## Python

In my opinion, Python is a terrible language and in a perfect world Julia would have overtaken Python &
people would build other things with Go, Rust, or Kotlin. *sigh*.
Alas, the reality is that the entire tech sector has jumped on the Python bandwagon and it is here to stay
as the language of data science and machine learning.

If you need to brush up on your Python, see the following from ECE 487 - Advanced Robotics:

- [Python Basics](https://stanbaek.github.io/ece487/PythonBasic.html)
- [Python Intermediate](https://stanbaek.github.io/ece487/PythonIntermediate.html)
- [NumPy](https://stanbaek.github.io/ece487/NumPy.html)

### Type Hints

It is an expectation in this course that **you will use type hints in function declarations and global variables**.

You should verify these hints are valid in VS Code via Pylance, which comes with Microsoft's official Python Extension [`ms-python.python`](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

Alternatively, you can use [PyRight](https://pypi.org/project/pyright/) directly.

**Global variables** are any variables declared outside of a function.

```python
# Example of a global variable with a type hint
age: int = 21
```

**Function declarations** may include parameters and return values.

```python
# Example of a function declaration with type hint for parameter and return
def stringify(num: int) -> str:
    '''Stringify casts an integer into a string'''
    return str(num)
```

```{tip}
Why don't we require type hints on all variables?

Python is a *dynamically typed* language, which adds flexibility and generally makes writing scripts quicker.
Some languages are statically typed - which comes with great benefits - but makes the code more rigid.

Adding type hints to every variable in Python (which the interpreter discards anyways!)
generally isn't worth the tradeoff for how long it takes to write the code and the decreased flexibility.

**Adding hints to just global variables and function declarations is an engineering compromise that
gets a lot of benefit for very little overhead.**
```

#### Type hints preventing errors

We use type hints to **bias toward build-time errors** *instead* of runtime errors.

```python
def type_error_demo_1(a, b):
    return a + b

def type_error_demo_2(a: int, b: int) -> int:
    return a + b

# This will cause a problem at *run*
my_runtime_error = type_error_demo_1(99, 'problems!')
# This will cause an error at type check
my_static_error = type_error_demo_2(0, 'problems.')
```

If you try to run this script, Python will give you this runtime error.
It's hard to debug and will crash your app at an unknown time.

```text
Traceback (most recent call last):
  File "/tmp/type.py", line 8, in <module>
    my_runtime_error = type_error_demo_1(99, 'problems')
  File "/tmp/type.py", line 2, in type_error_demo_1
    return a + b
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

*But* if you use Pyright *before* running the code you get the exact problem
(trying to pass "problems", which is a string instead of the expected int), and where it is.
Just notice that you **must** provide the type hints.

```text
/tmp/type.py:10:40 - error: Argument of type "Literal['problems.']" cannot be assigned to parameter "b" of type "int" in function "type_error_demo_2"
    "Literal['problems.']" is not assignable to "int" (reportArgumentType)
1 error, 0 warnings, 0 informations
```

#### Further reading

- [Python Types Intro (FastAPI)](https://fastapi.tiangolo.com/python-types/)
- [Type Hints Cheat Sheet (MyPy)](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)

### Format and Lint

Format really matters in Python for two reasons:

1. It is white space delimited (which is *dumb*, but here we are), so an error will cause a true error.
2. A standard format makes code easier to read and debug.

Most IDEs will help to some extent. You should always **lint** code you write.

> [Linting](https://code.visualstudio.com/docs/python/linting) helps to prevent errors by analyzing code for common syntactical, stylistic, and functional errors
> and unconventional programming practices. Although there is a little overlap between formatting and linting, the two capabilities are complementary.
> ~ [Formatting Python in VS Code](https://code.visualstudio.com/docs/python/formatting)

#### Format with Black

I recommend using [Black](https://black.readthedocs.io/en/stable/index.html) for format.

```python
# Black will standardize these to both use double quotes
print("Hey!")
print('How are you?')
```

According to the [docs](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter),
you can ensure VS Code formats Python files with black on save by [installing Microsoft's Black Formatter extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
and then adding using **View > Command Palette... and run Preferences: Open User Settings (JSON)** and adding the following between the `{ }`:

```json
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
```

#### Lint with Pylance

Microsoft's **Pylance** is included in the official [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and is a great linter!

```python
# Pylance will complain that y is not declared
x = y + 3
print(x)
```

## Tooling

### Jupyter Notebook

We will just [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html)
to run code in VS Code, Google Colab, and our department AI server.
These notebooks allow you to execute Python, save the results, commit with Git, and distribute them.

As you saw in the previous lesson, you can open many of the pages in this course directly into Google Colab
via the 🚀 button at the top of the page.

### GitHub

This is where you will backup all of your completed code.
Gradescope will also pull from your repos for assignment submission.

For a refresher, see [ECE 281: GitHub Real Fast](https://usafa-ece.github.io/ece281-book/appendix/github.html)

### GitHub and Jupyter

The next homework assignment will have you fork a copy of this repository.
You can then open your copy of this repo in whatever Jupyter instnace you are using.
After you make changes to a file you can then push those changes from Jupyter to GitHub!
This will then allow you to easily submit to Gradescope as well.

```{tip}
To push chnages from Google Colab to GitHub, you can simply hit **Ctrl+S**.
This will open a "Save in Github" box. Make sure you have the correct repository (your fork)
and the correct branch (probably `main`) selected.

Always add a *helpful* commit message!
```

- Here are some additional ways to [Use Colab with GitHub](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)
