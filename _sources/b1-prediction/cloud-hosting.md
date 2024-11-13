# Cloud Hosting

## Pre-Reading

- [Cloudflare: What is the Cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/)
- IBM's [What is an API (application programming interface)?](https://www.ibm.com/topics/api)

and

<iframe
  src="https://iframe.videodelivery.net/ad2223e095b603c44858996d4a727ea4"
  width="640"
  height="360"
  frameborder="0"
  allow="autoplay; encrypted-media"
  allowfullscreen>
</iframe>

## The Cloud

The ☁️ is just you renting time on someone elses computer.

AWS, Azure, and [Digital Ocean](https://www.digitalocean.com/products/droplets) are all commercial cloud providers that will let you pay to rent their servers.
These servers are in locations throughout the world!
Organizations can also run their own private "cloud," meaning servers that they directly control and manage.

The [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) is extremely helpful for understanding the cloud:

```{figure} https://d1.awsstatic.com/security-center/Shared_Responsibility_Model_V2.59d1eccec334b366627e9295b304202faf7b899b.jpg

---
name: aws-shared-responsibility
url: https://aws.amazon.com/compliance/shared-responsibility-model/
---
The AWS Shared Responsibility Model details the divide between who secures the hardware and virtualization software "of" the cloud (AWS) vs. the applications running "in" the cloud (the customer).
```

It is *astonishing* what cloud providers can serve you! **But that depends...**

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">On how well your manners are, and how big your pocketbook is. <a href="https://t.co/rW1GyKhSpI">pic.twitter.com/rW1GyKhSpI</a></p>&mdash; Star Wars (@starwars) <a href="https://twitter.com/starwars/status/1523738635970834432?ref_src=twsrc%5Etfw">May 9, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

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

#### Security

To be *extremely brief*:

1. **Identity and Access Management (IAM) is tricky.** provides fine granularity of what people and programs can and cannot read/modify/delete *but* because it can be tricky to get these permissions correct, organizations often over-allocate permissions. Hackers love to take advantage of that.
2. **"Secure" is rarely the default**. (According to the shared responsibility model, that's your job!). For example, although [S3 is now encrypted by default](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-encryption-faq.html), it took years and several high-profile breeches for this to be the case!
3. **Managed Services Cost Money.** If you want things like automatic updates, automatic logging, and more, the cloud provide can do that for you - this will help your security posture - but it cost more cash.

## Web Application Architecture

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

**Databases** are beyond the scope of this course. As a result, the apps we build will be stateless.
They will focus on providing inference via a pre-trained model.

### APIs

Application Program Interfaces (APIs) are a programmatic way to interact with a web application.

There are many types, but we will use HTTP [RESTful APIs](https://restfulapi.net/) in this course.

Representational State Transfer (REST) is a software architecture that imposes conditions on how an API should work. These APIs are **stateless**, meaning each request contains authentication tokens and other information and is isolated from other requests. This is in contrast to keeping a long-lived connection open.

Our APIs will primarily be HTTP **GET** requests - which get information from the server -
or **POST** requests - which submit data to be processed.

As an example **GET** request, you can fetch your username from GitHub!
Use the `curl` command (which makes a GET request by default):

```bash
# Replace octocat with your GitHub username
curl https://api.github.com/users/octocat
```

#### FastAPI

A popular Python API Framework is FastAPI. Two big reasons to use it:

1. The documentation is a pleasure to read
2. It supports type annotations in [path parameters](https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class) and [return types](https://fastapi.tiangolo.com/tutorial/response-model/#response-model-return-type)

> FastAPI will use this return type to:
>
> **Validate** the returned data.
>
> - If the data is invalid (e.g. you are missing a field), it means that your app code is broken, not returning what it should, and it will return a server error instead of returning incorrect data. This way you and your clients can be certain that they will receive the data and the data shape expected.
>
> **Add a JSON Schema** for the response, in the OpenAPI path operation.
>
> - This will be used by the automatic docs.
> - It will also be used by automatic client code generation tools.
>
> But most importantly:
>
> It will **limit and filter** the output data to what is defined in the return type.
>
> - This is particularly important for **security**
>
> [*~ Tutorial User Guide*](https://fastapi.tiangolo.com/tutorial/response-model/)

## Next Steps: FastAPI Demo

We will run a simple FastAPI example!

% TODO: Add FastAPI Example
% TODO: decide if going with Poetry or venv
