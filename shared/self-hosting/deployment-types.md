## OpenVidu Local (development)

To run OpenVidu in your local machine, this is the quickest option. It is a Docker Compose setup that includes all the necessary services to run OpenVidu in your LAN, including automated SSL certificates that will be valid across all devices in your network.

It comes in two flavors:

 - <strong>OpenVidu Local <span class="openvidu-tag openvidu-community-tag" style="font-size: 14px;">COMMUNITY</span></strong>: mirrors the experience of <strong>OpenVidu Single Node <span class="openvidu-tag openvidu-community-tag" style="font-size: 14px;">COMMUNITY</span></strong>, fine tuned for local development.
 - <strong>OpenVidu Local <span class="openvidu-tag openvidu-pro-tag" style="font-size: 14px;">PRO</span></strong>: mirrors the experience of <strong>OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: 14px;">PRO</span></strong>, fine tuned for local development. In this case, OpenVidu runs in evaluation mode for free for development and testing purposes (some limits apply: maximum 8 Participants across all Rooms, maximum 5 minutes duration per Room).

<figure markdown>
  ![OpenVidu Single Node](../../assets/images/openvidu-local-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Local (development)</figcaption>
</figure>

## OpenVidu Single Node

This is the simplest production-ready OpenVidu deployment available. It provides all the features you need, but lacks scalability and fault tolerance. But make no mistake about it: it is perfectly suitable for medium-scale production deployments. For most projects OpenVidu Single Node will be enough, at least until your user load gets serious. You can host hundreds of simultaneous participants in your rooms by running OpenVidu Community on a sufficiently powerful server!

It is composed of a single OpenVidu Node hosting all the necessary services in a monolithic setup. It comes in two flavors:

 - <strong>OpenVidu Single Node <span class="openvidu-tag openvidu-community-tag" style="font-size: 14px;">COMMUNITY</span></strong>: all the features you need to build your real-time application.
 - <strong>OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: 14px;">PRO</span></strong>: for those users that want the benefits of OpenVidu PRO in a single-node setup. It includes **2x performance** and **advanced observability** features.

<figure markdown>
  ![OpenVidu Single Node](../../assets/images/openvidu-single-node-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Single Node</figcaption>
</figure>

## OpenVidu Elastic

This is the intermediate OpenVidu deployment. It provides **scalability** for your video rooms. Suitable for applications with dynamic load in the media plane that require scalability.

It is composed of two different types of nodes, one of them running on a cluster of multiple servers and the other running as a single monolithic server:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster.
- **A single Master Node** hosting all the support services in a monolithic setup.

<figure markdown>
  ![OpenVidu Elastic](../../assets/images/openvidu-elastic-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu Elastic</figcaption>
</figure>

## OpenVidu High Availability

This is the most complete OpenVidu deployment. It provides **scalability** for your video rooms and **fault tolerance** in all its services. Suitable for applications where both scalability and availability are critical.

It is composed of two different types of nodes running on two separate clusters:

- **A cluster of Media Nodes** hosting all the media-related services. Your video rooms scale up and down thanks to this cluster. The minimum number of nodes in this cluster is **1**, and it is designed to scale up and down dynamically according to workload.
- **A cluster of Master Nodes** hosting all the support services in their high availability format. Your deployment is fault tolerant thanks to this cluster. The minimum number of nodes in this cluster is **4**, and it is designed to have a fixed number of nodes at all times.

<figure markdown>
  ![OpenVidu High Availability cluster](../../assets/images/openvidu-ha-architecture.svg){ .svg-img .dark-img }
  <figcaption>OpenVidu High Availability cluster</figcaption>
</figure>