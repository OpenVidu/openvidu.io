---
title: Force traffic through 443 with TLS
description: Learn how to force all OpenVidu traffic, including WebRTC, through port 443 with TLS for enhanced security and compatibility with restrictive networks.
---

# Force all traffic including WebRTC to go through 443 with TLS

In certain scenarios, users may be behind restrictive firewalls or network policies that only permit traffic through port 443 using TLS. By default, OpenVidu is configured to support TURN with TLS using the main domain name. This allows users behind restrictive firewalls to connect through port 443.

In some cases, it is necessary to ensure that all traffic, including WebRTC, is routed through port 443 with TLS due to network policies, security requirements, or other considerations.

To enforce this configuration, ensure that the following ports are not open or are explicitly closed:


**Single Node closed Ports**

**Node**|**Port**|**Protocol**
---|---|---
OpenVidu Server|443|UDP
OpenVidu Server|50000-60000|UDP

**Elastic and High Availability closed Ports**

**Node**|**Port**|**Protocol**
---|---|---
Media Node|443|UDP
Media Node|50000-60000|UDP

In this way, all the traffic will go through port 443 with TLS using the main domain name.

## Considerations

- Media over UDP using WebRTC does not mean that the media is not encrypted. WebRTC encrypts the media using SRTP and DTLS. WebRTC is designed to be encrypted by default.

- Media going through 443 with TLS has a penalty in the media quality and CPU usage. This is because of the TLS roundtrip, TCP being used and media processed twice by the TURN server and the Media Server. This can lead to a worse user experience and higher CPU usage in the Media Server. We recommend using this configuration only if it is strictly necessary.
