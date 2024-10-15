# Cloud Hosting

## Pre-reading

- [Cloudflare: How does the Internet work?](https://www.cloudflare.com/learning/network-layer/how-does-the-internet-work/)

### Objectives

## Internet Protocol

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

You can find your private IP address with

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

> A computer’s IP address is like the physical address of a house. If someone calls a pizzeria to order a delivery, they need to provide their physical address. Without that address, the pizza delivery person will have no idea which house to deliver the pizza to. ~ [Cloudflare: What is my IP address?](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/)

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

## The Cloud

The ☁️ is just you renting time on someone elses computer.

<iframe
  src="https://iframe.videodelivery.net/ad2223e095b603c44858996d4a727ea4"
  width="640"
  height="360"
  frameborder="0"
  allow="autoplay; encrypted-media"
  allowfullscreen>
</iframe>

AWS, Azure, and [Digital Ocean](https://www.digitalocean.com/products/droplets) are all commercial cloud providers that will let you pay to rent their servers.
These servers are in locations throughout the world!

The [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) is extremely helpful for understanding the cloud:

```{figure} https://d1.awsstatic.com/security-center/Shared_Responsibility_Model_V2.59d1eccec334b366627e9295b304202faf7b899b.jpg

---
name: aws-shared-responsibility
url: https://aws.amazon.com/compliance/shared-responsibility-model/
---
The AWS Shared Responsibility Model details the divide between who secures the hardware and virtualization software "of" the cloud (AWS) vs. the applications running "in" the cloud (the customer).
```

It is *astonishing* what cloud providers can serve you! But that depends...

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">On how well your manners are, and how big your pocketbook is. <a href="https://t.co/rW1GyKhSpI">pic.twitter.com/rW1GyKhSpI</a></p>&mdash; Star Wars (@starwars) <a href="https://twitter.com/starwars/status/1523738635970834432?ref_src=twsrc%5Etfw">May 9, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

### Web Application Architecture

Web applications are frequently described in terms of "front end" and "back end."
In this class we are exclusively concerned with the back end.

- The **front end** is the pretty website that you see. It is a collection of HTML, CSS, and JavaScript.
Your web browser executes and renders the front end code.
- The **back end** is the part most people never see: the logic and databases that drive the application.
  This can be written in Go, Python, Rust, Kotlin, or many other languages.

```{figure}  https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210204220458/Web-Application-Three-Tier-Architecture.png

The common **Web Application Three Tier Architecture**.
See [GeeksForGeeks: Web Applications for Beginners](https://www.geeksforgeeks.org/how-web-works-web-application-architecture-for-beginners/)
for more information.
```

Databases are beyond the scope of this course.
As a result, the application program interfaces (APIs) we use will not have persistence.
Likewise, our business logic will consist almost entirely of conducting inference with a model.

### Cloud Resources

This is a crazy complex space. You can get various certifications or complete free learning:

- [AWS Training and Certification](https://aws.amazon.com/training/)
  - ([AWS Certified Cloud Solutions Architect](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
    is the one to start with if you *really* want to get into this world.)
- [Azure Training](https://learn.microsoft.com/en-us/training/azure/)

```{note}
This content is for educational purposes only.
Nothing on this page constitutes an endorsement by the U.S. Government.
```

AWS is currently the world leader, with Microsoft Azure and Google Cloud Provider (GCP) nipping at its heals.

DigitalOcean is smaller, but more user friendly (but also less capable) and oftentimes more affordable.
They also offer [$200 free credit via GitHub Student](https://www.digitalocean.com/github-students).

#### Virtual Machines

You can have your very own virtual machine through [AWS EC2](https://aws.amazon.com/ec2/)
or [DigitalOcean Droplets](https://www.digitalocean.com/products/droplets).

As of October 2024, here is the cheapest DO Droplet:

| Memory  | vCPU   | Transfer | SSD    | $/hr     | $/mo  |
|---------|--------|----------|--------|----------|-------|
| 512 MiB | 1 vCPU | 500 GiB  | 10 GiB | $0.00595 | $4.00 |

Cloud VMs are highly configurable, but a good default start is the latest LTS release of Ubuntu.

You can also pick a geographic **region** to deploy the VM to.
The location of a data center will impact latency, price, and legal considerations.

#### Object Storage

AWS Simple Scalable Storage ([S3](https://aws.amazon.com/s3/)) is the de facto standard for object storage.
It is *object storage*, meaning you have to store/fetch/delete entire files, rather than parts of a file
(changing parts of a file is *block storage*).

S3 is great for serving static webpages and files, off-site backups, or massive datalakes!

It has a generous free tier, then $0.023 per GB per month after that for storage.
But watch out, because the data transfer out can get pricy for large applications.

## Next Steps

1. Use `ping` to talk to another computer on the LAN.
2. Do an `nslookup` of a domain, and then `curl` the result.
3. Browse some of the cloud provider offerings.
