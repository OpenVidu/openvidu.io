---
draft: true
date: 2026-03-19
categories:
  - OpenVidu Features
  - WebRTC
authors:
  - pabloFuente
  - carlosRuiz
hide:
  - navigation
  - search-bar
  - version-selector
---

# How the network configuration of your clients affects their user experience and your infrastructure costs

![Header image suggestion: WebRTC connectivity paths showing UDP, TURN, TCP, TLS]

Real-time video applications seem fairly simple at first glance. A user clicks "Join", video and audio start flowing, and everyone can see and hear each other.

But under the hood, WebRTC is making a series of complex networking decisions that determine **how media actually travels across the internet**. Which ultimately impacts both the final users and your infrastructure.

These decisions made by WebRTC directly impact:

- Video quality and latency, and therefore user experience.
- Server resource consumption, and therefore infrastructure cost.

So: not all WebRTC connections are equal. With that affirmation as a starting point, in this post you will learn:

- How WebRTC selects connection paths using ICE.
- The role of STUN and TURN.
- Why UDP is always preferred.
- What happens in restrictive networks.
- How connection type impacts both user experience and infrastructure.

<!-- more -->

---

## Why Network Conditions Matter in WebRTC

When a client connects to a media server (like an OpenVidu Media Node), the ideal scenario is simple:

**Client → Media Server → Client**

But in reality, most users are behind:

- NAT routers
- Corporate firewalls
- Mobile carrier networks
- VPNs

These systems restrict connectivity in various ways, often blocking the optimal path for real-time media. The fact is that, objectively speaking, there is **an optimal path** for real-time media — defined by a specific **protocol**, **port**, and **hop between nodes**. But this optimal path is not always available due to the client network restrictions mentioned above.

This is where WebRTC's connectivity mechanisms come into play. Let's dive into ICE!

---

## ICE: The Engine Behind WebRTC Connectivity

WebRTC uses **ICE (Interactive Connectivity Establishment)** to determine how two endpoints should communicate.

Its job is simple: **try multiple network paths and select the best one that works.**

ICE gathers different **connection candidates**:

- **Host candidates**: the device's own local IP addresses.
- **Server-reflexive candidates**: the public IP address discovered via STUN.
- **Relay candidates**: addresses provided by a TURN relay server.

It then tests all combinations between the client and the server, ranks them by priority, and selects the best working option. The priority order is always the same: direct UDP first, relay via UDP second, TCP fallback third, and TLS as a last resort.

The important thing to understand here is that ICE doesn't just pick a random path — it follows a **strict priority order**, always aiming for the lowest latency and highest quality option. If the best path isn't available, it gracefully steps down to the next one.

> OpenVidu implements the ICE protocol.

---

## STUN: Discovering Your Public Identity

Your device's private IP address `192.168.1.x` is useless on the public internet. The idea that a server outside your local network can’t actively connect to you directly is pretty intuitive. So, how does a media server know where to send video back to you?

This is where **STUN (Session Traversal Utilities for NAT)** comes in.

A STUN server is a simple, lightweight service that tells your client: *"Hey, from the internet's perspective, your public IP address is X and your port is Y."*  Your client can then include this information in its ICE candidates, so that the remote media server knows how to reach you.

STUN is essentially free in terms of resources — it only handles a tiny exchange of messages at connection setup, and after that it gets out of the way. **No media ever flows through a STUN server.** Its only job is address discovery.

But STUN alone isn't enough. In many real-world networks, NAT traversal through STUN fails — for example, when a firewall is configured to block incoming connections that weren't explicitly allowed. That's when TURN steps in.

> OpenVidu integrates a STUN server as part of its deployment.

---

## TURN: Your Media Relay of Last Resort

**TURN (Traversal Using Relays around NAT)** takes a completely different approach. Instead of helping two peers talk directly as STUN does, it acts as a **relay**: all media flows *through* the TURN server.

This guarantees connectivity in almost any network scenario, because even the most restrictive firewalls typically allow outbound connections on well-known ports like 443. As long as your client can reach the TURN server through an allowed protocol and port, media can flow.

The tradeoff is real, though. Since all media is being proxied through an intermediate server:

- **Latency increases**, because packets travel an extra hop.
- **Server load increases**, because the TURN server now has to process all that media traffic.
- **Bandwidth costs go up**, since the server is carrying the full media stream for every relayed connection.

TURN is not bad — it's a lifesaver for users on restrictive networks. But it's a fallback, not a first choice.

> OpenVidu integrates a TURN server that works out of the box.

---

## The Four Connection Types, Ranked

Now that you know what STUN and TURN do, let's put it all together. WebRTC — and OpenVidu — will attempt the following connection types in strict priority order:

### 1. 🟢 ICE over UDP (Best)

This is the ideal scenario. After STUN discovers the client's public address, ICE performs **UDP hole punching**: both the client and the media server send UDP packets to each other simultaneously, convincing their respective firewalls to allow the traffic through.

**Result:** Media flows directly between client and server with no intermediate hops. Lowest latency, highest quality, zero extra infrastructure load.

**Requirements:** The client networks must allow outgoing and incoming UDP traffic on the port range used by the media server (typically 50000–60000), and the firewall must support stateful UDP (i.e., allow responses to outgoing UDP connections).

### 2. 🟠 TURN over UDP port 443 (Good)

If the high UDP port range is blocked but UDP itself is allowed on port 443, OpenVidu falls back to relaying media through a TURN server on UDP port 443.

**Result:** Media still travels over UDP — fast and low-latency — but through a relay. The extra hop adds a small amount of latency and slightly increases server load, but the experience is still good.

**Requirements:** The client networks must allow outgoing UDP traffic on port 443.

### 3. 🔴 ICE over TCP port 443 (Acceptable)

Some networks block UDP entirely — this is extremely common in strict corporate environments and certain VPNs. In this case, WebRTC can fall back to TCP on port 443, the same port used by HTTPS.

**Result:** The call works, but TCP is not designed for real-time media. Unlike UDP, TCP guarantees delivery and retransmits lost packets — which generally sounds good, but not for real-time media: it means a delayed packet causes everything behind it to wait. In a video call, this translates to increased latency and occasional stuttering rather than a brief glitch you'd barely notice with UDP. But again: this is better than no connection at all!

**Requirements:** The client networks must allow outgoing TCP traffic on port 443 (which is true in virtually all networks, since it's standard HTTPS traffic).

### 4. ⚫ TURN over TLS port 443 (Last Resort)

The final fallback is TURN over TLS — essentially media relayed through the TURN server, encrypted with TLS, all on port 443. This passes through even the most locked-down firewalls, since it's indistinguishable from regular HTTPS traffic. **If this does not work, then the client can't access the internet at all**.

**Result:** The call functions, but this combination — relay overhead, plus TLS encryption plus TCP's retransmission behavior — produces the highest latency and the greatest server resource consumption of all options. If a significant share of your users are hitting this path, it's worth contacting their IT teams to see if they can relax their firewall rules.

**Requirements:** The client networks must allow outgoing TCP traffic on port 443. Universally available: any network that allows general internet access will allow this.

---

## Why UDP Is Always Preferred for Real-Time Media

You might wonder: if TCP is the most reliable protocol, why does WebRTC prefer UDP?

The answer comes down to what "reliable" actually means for a video call.

TCP's reliability mechanism works by retransmitting lost packets and ensuring they arrive in order. For downloading a file, this is exactly what you want. For a live video call, it's counterproductive. If a packet carrying 20ms of audio gets lost and retransmitted, by the time it arrives it's already too late — that audio should have played 100ms ago. Delivering it now just causes a glitch worse than if it had been dropped.

UDP, on the other hand, sends packets and doesn't look back. If one is lost, WebRTC's own congestion control and error correction mechanisms (like NACK and FEC) handle it in ways that are optimized for real-time media. The result is smoother, more natural communication, even on imperfect networks.

**The rule of thumb:** UDP packet loss produces brief, barely-perceptible glitches. TCP packet loss in real-time media produces freezing, stuttering, and audio-video desync.

---

## The Real Cost of Restrictive Networks

Let's make all of this information something concrete with a scenario.

Imagine you're deploying a video conferencing platform for a company. A significant portion of their employees connect from a corporate network that blocks all UDP traffic. Every single one of those users falls back to TURN over TCP.

Here's what that means in practice:

- Each user's media stream passes *through* your TURN server instead of flowing directly to the media node.
- Your TURN server now carries the full bandwidth of every relayed session — video, audio, screen shares, raw data, all of it.
- Latency is higher for all relayed users, and TCP's behavior under packet loss amplifies quality issues.
- Your infrastructure costs go up, sometimes significantly, depending on the volume of relayed traffic.

Now flip it: the same company opens UDP ports 50000–60000 on their firewall to your node IPs. Suddenly, all those users establish direct ICE connections. Your TURN server is nearly idle. Latency drops. Video quality improves. Infrastructure costs decrease, as your CPU and bandwidth usage drop.

**Network configuration is not just a user experience concern — it's a cost optimization lever for your infrastructure.**

---

## How OpenVidu Handles All of This Automatically

Here's the good news: you don't have to manage any of this manually.

OpenVidu handles the entire ICE negotiation process automatically, for every client, on every connection. When a user joins a session, OpenVidu's signaling layer orchestrates the exchange of ICE candidates between the client and the Media Node, tries each path in priority order, and selects the best one that works.

Your OpenVidu deployment includes:

- A media server that implements the **ICE protocol** and supports all connection types.
- A **STUN service** to help clients discover their public addresses.
- A **TURN service** configured and ready to relay traffic on UDP 443, TCP 443, and TLS 443 — so that users on restrictive networks can always connect.
- Nodes that accept **direct UDP connections** on the high port range when the client's network allows it.

The initial session handshake is always established via TCP 443 to the load balancer, which is allowed in virtually every network. From there, OpenVidu negotiates transparently the best possible media path for each individual client.

If a user is on an open network, they get direct UDP. If they're behind a strict corporate firewall, they get TURN over TLS. And everything in between is handled gracefully, without any configuration on your part or theirs.

---

## Conclusions

WebRTC connectivity is not magic — it's a well-defined priority system that adapts to whatever the network allows. Understanding it helps you make better decisions about infrastructure, troubleshoot quality issues faster, and communicate clearly with IT teams about what port rules actually matter.

To summarize the key takeaways:

- **ICE** is the mechanism that selects the best available connection path.
- **STUN** discovers a client's public address — it carries no media.
- **TURN** relays media when direct connection fails — it costs bandwidth and adds latency.
- **UDP is always preferred** over TCP for real-time media, for fundamental protocol reasons.
- The four paths — direct UDP, TURN/UDP, ICE/TCP, TURN/TLS — represent a trade-off between quality and network permissiveness.
- Restrictive networks don't just affect user experience; they shift load to your relay infrastructure.

OpenVidu abstracts all of this complexity away, and all of our [official self-hosted deployments](../../docs/self-hosting/deployment-types.md) include the necessary components and configurations to ensure the best possible connectivity for your users. However, it’s always good to know what’s happening under the hood, so you can better communicate with your users and their IT teams about how to optimize their networks.