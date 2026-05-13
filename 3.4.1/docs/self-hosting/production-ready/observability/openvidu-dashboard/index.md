# OpenVidu Dashboard

It is a web application designed to provide **OpenVidu administrators** with a comprehensive view of **usage statistics** and **real-time monitoring** of video **Rooms**. OpenVidu Dashboard is included by default in any [OpenVidu deployment](https://openvidu.io/3.4.1/docs/self-hosting/deployment-types/index.md).

To access **OpenVidu Dashboard**, go to https://your.domain/dashboard/ and **log in** using your **admin credentials**.

### Views

#### Analytics

Display **graphical analytics** for client SDKs, connection types, bandwidth usage, unique participants, rooms and egresses created over different **time periods** (last 24 hours, last 7 days, last 28 days or current month).

#### Rooms

Review the total count of **active rooms** and **active participants**, along with a roster of currently active rooms and a history of **closed rooms** within the last 28 days. Detailed information on each room is accessible by clicking on the respective row.

#### Room Details

This view is part of OpenVidu [PRO](/pricing/#openvidu-pro) edition.

Retrieve in-depth information about a specific **room**, including its duration, bandwidth consumption, participants and related events. A chart illustrating the active participants count over time is also provided.

#### Participant Details

This view is part of OpenVidu [PRO](/pricing/#openvidu-pro) edition.

Obtain detailed insights into each **participant**, covering their duration, bandwidth usage, average audio and video quality score, information about the client they are connecting with, connection stats, published tracks and related events.

A participant may **connect** and **disconnect** from a room multiple times while it remains open. Each instance of connection using the same **participant identity** is referred to as a **`participant session`**. If multiple sessions occur, we will aggregate all participant sessions together and organize them into a timeline at the top of the participant details view. You can easily switch between participant sessions by clicking on each corresponding row:

#### Egress-Ingress

Review an overview of all **egresses** and **ingresses**, including their duration and status. Detailed information for each egress or ingress can be accessed by clicking on the respective row.

#### Egress Details

This view is part of OpenVidu [PRO](/pricing/#openvidu-pro) edition.

Access comprehensive details about a specific **egress**, including its duration, current status, type, associated room, destinations, status timeline and request information.

#### Ingress Details

This view is part of OpenVidu [PRO](/pricing/#openvidu-pro) edition.

Explore detailed information about a specific **ingress**, including its total duration, status and a list of all associated rooms.
