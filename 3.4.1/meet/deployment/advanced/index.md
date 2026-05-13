Warning

OpenVidu Meet is currently considered in **BETA**. There may be bugs and its APIs are subject to change.

Info

**OpenVidu Meet** is under the hood an **OpenVidu Platform** deployment with a module on top of it. Therefore, all deployment documentation for OpenVidu Platform applies to OpenVidu Meet as well. The information in this page is a summary of the different deployment options and the links to their corresponding OpenVidu Platform documentation.

## Deployment types

OpenVidu Meet can be easily deployed in a single server (follow the [basic deployment guide](https://openvidu.io/3.4.1/meet/deployment/basic/index.md)). However, a single server won't be enough for environments that require scalability and high-availability. For such cases, it is necessary a multi-node deployment.

| Type of deployment            | [**OpenVidu Local (development)**](#openvidu-local-development)                                                                                                       | [**OpenVidu Single Node**](#openvidu-single-node)                                                                                                                                | [**OpenVidu Elastic**](#openvidu-elastic)                                                                     | [**OpenVidu High Availability**](#openvidu-high-availability)            |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **OpenVidu Edition**          | COMMUNITY                                                                                                                                                             | COMMUNITY PRO                                                                                                                                                                    | PRO                                                                                                           | PRO                                                                      |
| **Suitability**               | For local development in your laptop                                                                                                                                  | For applications with medium user load                                                                                                                                           | For applications with dynamic user load that require scalability                                              | For applications where both scalability and fault tolerance are critical |
| **Features**                  | Friendly Docker Compose setup with Redis, Egress, Ingress, S3 storage and observability. With automatic certificate management to test across devices in your network | COMMUNITY Custom LiveKit distribution with Redis, Egress, Ingress, S3 storage and observability. PRO Same features but adding **2x performance** and **advanced observability**. | Same benefits as OpenVidu Single Node plus **2x performance**, **advanced observability** and **scalability** | Same benefits as OpenVidu Elastic plus **fault tolerance**               |
| **Number of servers**         | Your laptop                                                                                                                                                           | 1 Node                                                                                                                                                                           | 1 Master Node + N Media Nodes                                                                                 | 4 Master Nodes + N Media Nodes                                           |
| **Installation instructions** | [Try](https://openvidu.io/3.4.1/meet/deployment/local/index.md)                                                                                                       | [Install](https://openvidu.io/3.4.1/meet/deployment/basic/index.md)                                                                                                              | [Install](https://openvidu.io/3.4.1/docs/self-hosting/elastic/index.md)                                       | [Install](https://openvidu.io/3.4.1/docs/self-hosting/ha/index.md)       |

Info

You can learn more about the **OpenVidu**COMMUNITY and **OpenVidu**PRO editions [here](https://openvidu.io/3.4.1/meet/deployment/overview/#openvidu-meet-editions).

### OpenVidu Local (development)

Run the OpenVidu Local deployment in your machine by following [this guide](https://openvidu.io/3.4.1/meet/deployment/local/index.md).

To run OpenVidu in your local machine, this is the quickest option. It is a Docker Compose setup that includes all the necessary services to run OpenVidu in your LAN, including automated SSL certificates that will be valid across all devices in your network.

OpenVidu Local (development)

### OpenVidu Single Node

You can install OpenVidu Meet as a Single Node deployment by following the [basic deployment guide](https://openvidu.io/3.4.1/meet/deployment/basic/index.md). You can also check out the [OpenVidu Platform documentation](https://openvidu.io/3.4.1/docs/self-hosting/single-node/index.md) for more detailed installation options.

This is the simplest production-ready OpenVidu deployment available. It provides all the features you need, but lacks scalability and fault tolerance. But make no mistake about it: it is perfectly suitable for medium-scale production deployments. For most projects OpenVidu Single Node will be enough, at least until your user load gets serious. You can host hundreds of simultaneous participants in your rooms by running OpenVidu Community on a sufficiently powerful server!

It is composed of a single OpenVidu Node hosting all the necessary services in a monolithic setup. It comes in two flavors:

- **OpenVidu Single Node COMMUNITY**: all the features you need to build your real-time application.
- **OpenVidu Single Node PRO**: for those users that want the benefits of OpenVidu PRO in a single-node setup. It includes **2x performance** and **advanced observability** features.

OpenVidu Single Node

### OpenVidu Elastic

Install OpenVidu Elastic by following the [OpenVidu Platform guide](https://openvidu.io/3.4.1/docs/self-hosting/elastic/index.md).

This is the intermediate OpenVidu deployment. It provides **scalability** for your video rooms. Suitable for applications with dynamic load in the media plane that require scalability.

It is composed of two different types of nodes, one of them running on a cluster of multiple servers and the other running as a single monolithic server:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster.
- **A single Master Node** hosting all the support services in a monolithic setup.

OpenVidu Elastic

### OpenVidu High Availability

Install OpenVidu High Availability by following the [OpenVidu Platform guide](https://openvidu.io/3.4.1/docs/self-hosting/ha/index.md).

This is the most complete OpenVidu deployment. It provides **scalability** for your video rooms and **fault tolerance** in all its services. Suitable for applications where both scalability and availability are critical.

It is composed of two different types of nodes running on two separate clusters:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster. The minimum number of nodes in this cluster is **1**, and it is designed to scale up and down dynamically according to workload.
- **A cluster of Master Nodes** hosting all the support services in their high availability format. Your deployment is fault-tolerant thanks to this cluster. The minimum number of nodes in this cluster is **4**, and it is designed to have a fixed number of nodes at all times.

OpenVidu High Availability cluster
