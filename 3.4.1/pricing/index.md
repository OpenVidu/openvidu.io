# Pricing

|                           | **OpenVidu COMMUNITY**                                                                                                  | **OpenVidu PRO**                                                                                                   |                                                                                                        |                                                                                                                            |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Price                     | Free                                                                                                                    | 0.0006$ core/minute                                                                                                |                                                                                                        |                                                                                                                            |
| Type of deployment        | [**OpenVidu Single NodeCOMMUNITY**](https://openvidu.io/3.4.1/docs/self-hosting/deployment-types/#openvidu-single-node) | [**OpenVidu Single Node PRO**](https://openvidu.io/3.4.1/docs/self-hosting/deployment-types/#openvidu-single-node) | [**OpenVidu Elastic**](https://openvidu.io/3.4.1/docs/self-hosting/deployment-types/#openvidu-elastic) | [**OpenVidu High Availability**](https://openvidu.io/3.4.1/docs/self-hosting/deployment-types/#openvidu-high-availability) |
| Suitability               | For applications with medium user load                                                                                  | Enjoy the benefits of OpenVidu PRO in a single-node installation                                                   | For applications with dynamic user load that require scalability                                       | For applications where both scalability and fault tolerance are critical                                                   |
| Features                  | Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability                                   | Same features as OpenVidu Single Node COMMUNITY plus **2x performance** and **advanced observability**             | Same benefits as OpenVidu Single Node PRO plus **scalability**                                         | Same benefits as OpenVidu Elastic plus **fault tolerance**                                                                 |
| Number of servers         | 1 Node                                                                                                                  | 1 Node                                                                                                             | 1 Master Node + N Media Nodes                                                                          | 4 Master Nodes + N Media Nodes                                                                                             |
| Installation instructions | [Install](https://openvidu.io/3.4.1/docs/self-hosting/single-node)                                                      | [Install](https://openvidu.io/3.4.1/docs/self-hosting/single-node-pro)                                             | [Install](https://openvidu.io/3.4.1/docs/self-hosting/elastic/index.md)                                | [Install](https://openvidu.io/3.4.1/docs/self-hosting/ha/index.md)                                                         |

OpenVidu offers two editions:

- **OpenVidu COMMUNITY**, completely open-source and free to use. Offers a single node deployment suitable for medium user load.
- **OpenVidu PRO**, which is proprietary and with a simple pay-per-use pricing model. Offers advanced multi-node deployments suitable for applications that require improved performance, scalability, fault tolerance, and observability.

OpenVidu offers two solutions: **OpenVidu Meet** and **OpenVidu Platform**. They target different use cases (see [OpenVidu Meet vs OpenVidu Platform](https://openvidu.io/3.4.1/openvidu-meet-vs-openvidu-platform/index.md)), but they **do not affect pricing**: you can have either solution in an **OpenVidu COMMUNITY** or **OpenVidu PRO** deployment.

## How is OpenVidu Pro priced?

OpenVidu Pro follows a simple pricing model based on the number of cores used by the OpenVidu Pro cluster:

$0.0006

per core per minute available\
for your OpenVidu PRO cluster

Taking into account the following points:

- You only pay for your OpenVidu Pro cluster(s) for the time they are running. Usage will be registered the moment you start your cluster and will stop as soon as you shut your cluster down. When turned on, your cluster will be charged even in idle state (without active Rooms).
- You pay for every available core at any given time: if you cluster grows for one hour, that hour you will pay more. If your cluster decreases the next hour, next hour will be cheaper. Master Nodes and Media Nodes have the same core per minute price.
- Your OpenVidu Pro cluster(s) need to allow outbound traffic to domain **`accounts.openvidu.io`** port **`443`**. If you are behind a very restrictive corporate firewall that doesn't allow this, please contact us through [commercial@openvidu.io](mailto:commercial@openvidu.io).

## There is a 15-day free trial period waiting for you!

[Get an OpenVidu License](/account/)

______________________________________________________________________

## Why is OpenVidu Pro priced like this?

There are deliberate reasons for this pricing model in OpenVidu Pro:

- We believe that a platform specifically designed to be self-hosted should have a pricing model that is as close to hardware as possible: that is the total number of cores available to the cluster over time.
- This pricing model is simple, transparent and easy to predict: you pay only for the time the cluster is running and always according to its size.
- The cost is directly proportional to the size of your cluster: larger clusters pay more, smaller clusters pay less.
- Elasticity is encouraged: adjust the size of your cluster according to the load at any given time to minimize costs.

## When and how are you charged?

Users must create an [OpenVidu account](/account/) and get an OpenVidu License. This license will be required to deploy an OpenVidu Pro cluster ([OpenVidu Elastic](https://openvidu.io/3.4.1/docs/self-hosting/elastic/index.md) or [OpenVidu High Availability](https://openvidu.io/3.4.1/docs/self-hosting/ha/index.md)).

When purchasing an OpenVidu License, you will have to indicate your billing address and a credit card. You will receive a **15-day free trial period** during which you will not be charged at all.

After the free trial period, a **monthly billing cycle** will charge all your expenses to your credit card. Therefore, you will receive an invoice each month. You can review your upcoming expenses and your past invoices in your [OpenVidu account](/account/) page. And don't worry: we don't store any credit card data. The entire billing process is securely done via [Stripe](https://stripe.com/) .

OpenVidu Pro clusters will automatically report their usage on a recurring basis. That's why they need outbound access to domain **`accounts.openvidu.io`** port **`443`**. If you are behind a very restrictive corporate firewall that doesn't allow this, please contact us through [commercial@openvidu.io](mailto:commercial@openvidu.io).

## Pricing examples

As explained above, every minute of an OpenVidu Pro cluster is charged according to the number of cores available for the cluster. So let's see some actual examples, first noting the following points:

- The examples represent a **continuous usage of the cluster**, but remember that you can shut it down whenever you are not using it and that you can drop nodes to save resources.
- Each example shows in a table the price for **8 hours, 1 day and 1 month** of continuous usage, as well as the approximated amount of video Tracks and Rooms of 8 participants the cluster would support. This is done to provide a basic insight into the capacity of each cluster. These **8-to-8 Rooms** assume 64 video Tracks (640x480) and 64 audio Tracks in them (2 tracks published and 14 tracks subscribed per Participant), with no Egress, Ingress or other additional features.

### OpenVidu Elastic with 12 cores in total

This OpenVidu Pro Elastic cluster has 1 Master Node of 4 cores and 2 Media Nodes of 4 cores each.

|                                              |         |
| -------------------------------------------- | ------- |
| **Number of video Tracks**                   | 2000    |
| **Number of Rooms with 8 Participants**      | 30      |
| **8 hours**                                  | $3.46   |
| **24 hours** (1 day of uninterrupted use)    | $10.37  |
| **720 hours** (1 month of uninterrupted use) | $311.04 |

______________________________________________________________________

### OpenVidu Elastic with 20 cores in total

This OpenVidu Pro Elastic cluster has 1 Master Node of 4 cores and 4 Media Nodes of 4 cores each.

|                                              |         |
| -------------------------------------------- | ------- |
| **Number of video Tracks**                   | 4000    |
| **Number of Rooms with 8 Participants**      | 60      |
| **8 hours**                                  | $5.76   |
| **24 hours** (1 day of uninterrupted use)    | $17.28  |
| **720 hours** (1 month of uninterrupted use) | $518.40 |

______________________________________________________________________

### OpenVidu High Availability with 32 cores in total

This OpenVidu Pro HA cluster has 4 Master Nodes of 4 cores each and 4 Media Nodes of 4 cores each. The number of simultaneous Rooms and Tracks will be the same as in the previous example, but this cluster will provide fault tolerance thanks to the replication of the Master Nodes.

|                                              |         |
| -------------------------------------------- | ------- |
| **Number of video Tracks**                   | 4000    |
| **Number of Rooms with 8 Participants**      | 60      |
| **8 hours**                                  | $9.21   |
| **24 hours** (1 day of uninterrupted use)    | $27.65  |
| **720 hours** (1 month of uninterrupted use) | $829.44 |

______________________________________________________________________

### OpenVidu Elastic with a variable number of cores

This OpenVidu Pro Elastic cluster takes advantage of the elasticity of the platform. It has a fixed Master Node of 4 cores, but a variable number of Media Nodes. Let's imagine a scenario where our days are divided in three phases according to the user load:

- First 8 hours of the day the demand is low. 1 Media Node of 4 cores is enough to handle it.
- The next 8 hours of the day the user load increases significantly (this is very typical if our application is used more during working hours). We add another Media Node of 8 cores to handle this new demand.
- The last 8 hours of the day the demand decreases, and we are able to remove the Media Node of 8 cores and keep only the Media Node of 4 cores.

|                                                                  |         |
| ---------------------------------------------------------------- | ------- |
| **First 8 hours of the day with low demand** (8 cores in total)  |         |
| **Next 8 hours of the day with high demand** (16 cores in total) |         |
| **Last 8 hours of the day with low demand** (8 cores in total)   |         |
| **Total for 1 day**                                              | $9.21   |
| **Total for 1 month**                                            | $276.30 |

______________________________________________________________________

## There is a 15-day free trial period waiting for you!

[Get an OpenVidu License](/account/)
