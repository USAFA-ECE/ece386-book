# Cloud Hosting


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
