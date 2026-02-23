# OpenVidu Meet deployment overview

## Production ready

OpenVidu Meet is designed to be **self-hosted**, whether it is on premises or in a cloud provider. It brings to your own managed service advanced capabilities usually reserved only for SaaS solutions. There are two main reasons why you may need to self-host the real-time solution yourself:

- **Privacy**: you can't afford to let your client's data get out of your reach. OpenVidu allows you to meet all your privacy and regulatory requirements: no data at all is sent to any third-party server. Everything is self-contained on your own servers.
- **Leverage your resources**: your organization has access to its own infrastructure that can be used to host these services. SaaS solutions generally offer complete freedom from infrastructure management, but this comes with generally high prices that cover both the provider's infrastructure and their service surcharge. OpenVidu allows taking full advantage of your own infrastructure, reducing costs and increasing performance.

It is important to mention that when we talk about self-hosting OpenVidu, we don't just mean installing it in bare-metal servers or private VPCs. OpenVidu also supports deployments in the most popular cloud providers, using their native services when possible. **AWS** and **Azure** are currently supported, and others are coming soon. You can learn more about the different options to deploy OpenVidu in the [deployment types](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/index.md) section.

One of OpenVidu's main goals is offering a self-hosted, production-ready live-video platform with all the advanced capabilities typically reserved for SaaS solutions. This includes outstanding **performance**, **scalability**, **fault tolerance** and **observability**:

- **Performance**

  ______________________________________________________________________

  OpenVidu is built to be incredibly powerful. It is based on the best open source WebRTC stacks: [LiveKit](https://livekit.io/) and [mediasoup](https://mediasoup.org/) . By combining the best of both worlds, OpenVidu provides outstanding performance.

  [Learn more about performance](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/performance/index.md)

- **Scalability**

  ______________________________________________________________________

  OpenVidu has been designed from the outset with scalability in mind. Host videoconference rooms and large live streams with hundreds of participants. Autoscale your cluster to adapt to the demand and optimize your resources.

  [Learn more about scalability](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/scalability/index.md)

- **Fault Tolerance**

  ______________________________________________________________________

  OpenVidu offers fault tolerance in all its components. Deploy a reliable high-availability cluster knowing that if one of your node goes down, others will be able to continue working with no downtime.

  [Learn more about fault tolerance](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/fault-tolerance/index.md)

- **Observability**

  ______________________________________________________________________

  OpenVidu brings everything necessary to monitor the status, health, load and history of your deployment. It automatically collects events, metrics and logs, and provides [OpenVidu Dashboard](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/openvidu-dashboard/index.md) and a [Grafana stack](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/grafana-stack/index.md) to navigate them.

  [Learn more about observability](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/index.md)

## OpenVidu Meet editions

OpenVidu Meet is available in two editions:

### OpenVidu COMMUNITY

It is completely **open-source and free to use**. It includes all the features you need for your video conferencing solution. Everything listed in the [Features](https://openvidu.io/3.5.0/meet/#features) section is available in OpenVidu Meet COMMUNITY: HD video, HiFi audio, recording, screen sharing, chat, virtual backgrounds, and more.

OpenVidu Meet COMMUNITY is perfect for production deployments with moderate user load. It can be easily deployed on your own servers, and you can customize its branding to match your organization’s identity. If necessary, upgrading to OpenVidu PRO is seamless and non-disruptive.

### OpenVidu PRO

It is OpenVidu's **commercial edition** and requires a license. It is meant for high demanding environments with significant user load. On top of every functional feature available in OpenVidu COMMUNITY, OpenVidu PRO brings **2x performance**, **advanced observability**, **scalability** and **fault tolerance** features. As well as **priority support** from our team of experts.

OpenVidu PRO follows a simple pricing model based on the size of your deployment (number of CPU cores). Check the [OpenVidu pricing page](https://openvidu.io/pricing) for more details.

Info

Different OpenVidu [deployment types](#deployment-types) support different editions.

## Deployment types

OpenVidu Meet offers **user-friendly installers** that facilitate quick **on-premises deployments**, so you can self-host your real-time solution in your own infrastructure or any cloud provider.

The following documentation pages focus on three different deployments:

- [Local deployment](https://openvidu.io/3.5.0/meet/deployment/local/index.md), to test and develop in your machine.
- [Basic deployment](https://openvidu.io/3.5.0/meet/deployment/basic/index.md), a production installation requiring a single server.
- [Advanced deployments](https://openvidu.io/3.5.0/meet/deployment/advanced/index.md), a production installation requiring multiple servers for scalability and high-availability.

The table below summarizes the main characteristics of each deployment type.

| Type of deployment            | **OpenVidu Meet: Local deployment**                             | **OpenVidu Meet: Basic deployment**                                 | **OpenVidu Meet: Advanced deployment**                                                                                                        |
| ----------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenVidu Edition**          | COMMUNITY                                                       | COMMUNITY                                                           | PRO                                                                                                                                           |
| **Suitability**               | Suitable to test and develop                                    | Suitable for production applications with medium user load          | Suitable for production applications with dynamic user load and need for high availability                                                    |
| **Features**                  | Try out all OpenVidu Meet features in your laptop               | All OpenVidu Meet features, ready for production                    | All OpenVidu Meet features ready for production, plus **2x performance**, **advanced observability**, **scalability** and **fault tolerance** |
| **Number of servers**         | Your laptop                                                     | 1 server                                                            | Multiple servers                                                                                                                              |
| **Installation instructions** | [Try](https://openvidu.io/3.5.0/meet/deployment/local/index.md) | [Install](https://openvidu.io/3.5.0/meet/deployment/basic/index.md) | [Install](https://openvidu.io/3.5.0/meet/deployment/advanced/index.md)                                                                        |
