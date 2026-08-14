---
title: "OpenVidu Dashboard: live room monitoring"
description: "Watch rooms, participants, egresses and ingresses in real time from the OpenVidu Dashboard, and see exactly what a running deployment is doing."
tags:
  - setupcustomgallery
---

# OpenVidu Dashboard

It is a web application designed to provide **OpenVidu administrators** with a comprehensive view of **usage statistics** and **real-time monitoring** of video **Rooms**. OpenVidu Dashboard is included by default in any [OpenVidu deployment](../../deployment-types.md).

To access **OpenVidu Dashboard**, go to [https://your.domain/dashboard/]() and **log in** using your **admin credentials**.

  ![OpenVidu Dashboard login](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/login.png){ .mkdocs-img }

### Views

#### Analytics

Display **graphical analytics** for client SDKs, connection types, bandwidth usage, unique participants, rooms and egresses created over different **time periods** (last 24 hours, last 7 days, last 28 days or current month).

<div class="grid-container">

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics1.png" loading="lazy" alt="Analytics page of OpenVidu Dashboard with client SDK and connection charts"/></p></div>

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics2.png" loading="lazy" alt="Bandwidth usage charts in the OpenVidu Dashboard analytics page"/></p></div>

</div>

<div class="grid-container">

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics3.png" loading="lazy" alt="Participant and room charts in the OpenVidu Dashboard analytics page"/></p></div>

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/analytics4.png" loading="lazy" alt="Egress charts in the OpenVidu Dashboard analytics page"/></p></div>

</div>

#### Rooms

Review the total count of **active rooms** and **active participants**, along with a roster of currently active rooms and a history of **closed rooms** within the last 28 days. Detailed information on each room is accessible by clicking on the respective row.

  ![OpenVidu Dashboard rooms](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/rooms.png){ .mkdocs-img }

#### Room Details

!!! info "This view is part of <span>OpenVidu <a href="/pricing/#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

Retrieve in-depth information about a specific **room**, including its duration, bandwidth consumption, participants and related events. A chart illustrating the active participants count over time is also provided.

<div class="grid-container">

<div class="grid-33"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room_active.png" loading="lazy" alt="OpenVidu Dashboard listing with an active room"/></p></div>

<div class="grid-33"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room1.png" loading="lazy" alt="Room details page with duration, bandwidth and participants"/></p></div>

<div class="grid-33"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/room2.png" loading="lazy" alt="Timeline and related egresses in the room details page"/></p></div>

</div>

#### Participant Details

!!! info "This view is part of <span>OpenVidu <a href="/pricing/#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

Obtain detailed insights into each **participant**, covering their duration, bandwidth usage, average audio and video quality score, information about the client they are connecting with, connection stats, published tracks and related events.

<div class="grid-container">

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant1.png" loading="lazy" alt="Participant details page with duration and bandwidth usage"/></p></div>

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant2.png" loading="lazy" alt="Audio and video quality scores in the participant details page"/></p></div>

</div>

A participant may **connect** and **disconnect** from a room multiple times while it remains open. Each instance of connection using the same **participant identity** is referred to as a **`participant session`**. If multiple sessions occur, we will aggregate all participant sessions together and organize them into a timeline at the top of the participant details view. You can easily switch between participant sessions by clicking on each corresponding row:

  ![OpenVidu Dashboard participant sessions](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/participant3.png){ .mkdocs-img }

#### Egress-Ingress

Review an overview of all **egresses** and **ingresses**, including their duration and status. Detailed information for each egress or ingress can be accessed by clicking on the respective row.

  ![OpenVidu Dashboard egress-ingress](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress-ingress.png){ .mkdocs-img }

#### Egress Details

!!! info "This view is part of <span>OpenVidu <a href="/pricing/#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

Access comprehensive details about a specific **egress**, including its duration, current status, type, associated room, destinations, status timeline and request information.

<div class="grid-container">

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress1.png" loading="lazy" alt="Egress details page with duration, status and type"/></p></div>

<div class="grid-50"><p><img src="/assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/egress2.png" loading="lazy" alt="Destination and room information in the egress details page"/></p></div>

</div>

#### Ingress Details

!!! info "This view is part of <span>OpenVidu <a href="/pricing/#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

Explore detailed information about a specific **ingress**, including its total duration, status and a list of all associated rooms.

  ![OpenVidu Dashboard ingress](../../../../assets/images/platform/self-hosting/production-ready/observability/openvidu-dashboard/ingress.png){ .mkdocs-img }
