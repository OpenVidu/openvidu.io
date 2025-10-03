---
title: OpenVidu Meet deployment overview
description: OpenVidu offers a self-hosted, production-ready live-video platform with advanced capabilities, including performance, scalability, fault tolerance and observability.
---

# OpenVidu Meet deployment overview

## Production ready

OpenVidu Meet is designed to be **self-hosted**, whether it is on premises or in a cloud provider. It brings to your own managed service advanced capabilities usually reserved only for SaaS solutions. There are two main reasons why you may need to self-host the real-time solution yourself:

--8<-- "shared/self-hosting/production-ready.md"

## OpenVidu Meet editions

OpenVidu Meet is available in two editions:

### OpenVidu <span class="openvidu-tag openvidu-community-tag" style="font-size: 0.9em; vertical-align: top">COMMUNITY</span>

It is completely **open-source and free to use**. It includes all the features you need for your video conferencing solution. Everything listed in the [Features](../index.md#features) section is available in OpenVidu Meet COMMUNITY: HD video, HiFi audio, recording, screen sharing, advanced chat, virtual backgrounds, and more.

OpenVidu Meet COMMUNITY is perfect for production deployments with moderate user load. It can be easily deployed on your own servers, and you can customize its branding to match your organization’s identity. If necessary, upgrading to OpenVidu PRO is seamless and non-disruptive.

### OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: 0.9em; vertical-align: top">PRO</span>

It is OpenVidu's **commercial edition** and requires a license. It is meant for high demanding environments with significant user load. On top of every functional feature available in OpenVidu COMMUNITY, OpenVidu PRO brings **2x performance**, **advanced observability**, **scalability** and **fault tolerance** features. As well as **priority support** from our team of experts.

OpenVidu PRO follows a simple pricing model based on the size of your deployment (number of CPU cores). Check the [OpenVidu pricing page](https://openvidu.io/pricing) for more details.

!!! info
    Different OpenVidu [deployment types](#deployment-types) support different editions.

## Deployment types

OpenVidu Meet offers **user-friendly installers** that facilitate quick **on-premises deployments**, so you can self-host your real-time solution in your own infrastructure or any cloud provider.

The following documentation pages focus on three different deployments:

- [Local deployment](./local.md), to test and develop in your machine.
- [Basic deployment](./basic.md), a production installation requiring a single server.
- [Advanced deployments](./advanced.md), a production installation requiring multiple servers for scalability and high-availability.

The table below summarizes the main characteristics of each deployment type.

| Type of deployment        | <strong><span class="no-break">OpenVidu Meet:</span><br>Local deployment</strong> | <div style="width:10em"><strong>OpenVidu Meet:<br><span class="no-break">Basic deployment</span></strong></div> | <strong>OpenVidu Meet:<br><span class="no-break">Advanced deployment</span></strong> |
| ------------------------- | ------------------------------------ | -------------------- | ---------------- |
| **OpenVidu Edition**          | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> | <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> | <span class="openvidu-tag openvidu-pro-tag">PRO</span> |
| **Suitability**               | Suitable to test and develop | Suitable for production applications with medium user load | Suitable for production applications with dynamic user load and need for high availability |
| **Features**               | Try out all OpenVidu Meet features in your laptop | All OpenVidu Meet features, ready for production | All OpenVidu Meet features ready for production, plus **2x performance**, **advanced observability**, **scalability** and **fault tolerance** |
| **Number of servers**         | Your laptop | 1 server | Multiple servers |
| **Installation instructions** | [Try](./local.md){ .md-button } | [Install](./basic.md){ .md-button } | [Install](./advanced.md){ .md-button } |
