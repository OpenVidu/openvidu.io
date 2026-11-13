---
title: "Install OpenVidu Elastic on-premises"
description: "Deploy OpenVidu Elastic on your own servers with the OpenVidu CLI: one master, then any number of media nodes that join it."
---

# OpenVidu Elastic installation: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>


--8<-- "self-hosting/common/elastic-license-intro.md"

Deploy OpenVidu Elastic on your own Linux servers with the [OpenVidu CLI](../../openvidu-cli.md) (`ov`). An Elastic stack is **deployed on one machine** (the master) exactly like a Single Node PRO, with `--deployment-type elastic`; every media node then **joins** it. Media nodes are elastic: add and remove them according to workload. Elastic requires OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }.

=== "Architecture overview"

    This is what the deployment architecture looks like:

    ![OpenVidu Elastic On Premises](../../../../assets/images/platform/self-hosting/elastic/on-premises/elastic-architecture.svg){ .round-corners .dark-img loading=lazy }

    - The Master Node acts as a load balancer, managing the traffic and distributing it among the Media Nodes and the services on the Master Node.
    - The Master Node runs Caddy as a Layer 4 (TURN with TLS and RTMPS) and Layer 7 (Dashboard, Meet, APIs) reverse proxy.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.

The Master Node runs the data tier (MinIO, Redis, MongoDB), Caddy, the Dashboard and the optional Meet, observability and v2compatibility services. Each Media Node runs OpenVidu Server PRO, Ingress and Egress, and the observability agents.

## Requirements

Same as a [Single Node](../../single-node/on-premises/install.md#requirements), with **at least two machines**: one Master Node and one or more Media Nodes, each with a minimum of 4 CPU cores and Linux (Ubuntu recommended). The Master Node needs at least **8 GB of RAM**; each Media Node at least **4 GB**, or 8 GB if it records. With speech to text from a local provider (`vosk` or `sherpa` in the [speech processing agent](../../../ai/live-captions.md)), give the nodes that run that agent 8 to 16 GB. These figures are estimates, not measured limits. The Master Node needs generous disk (100 GB recommended) for recordings; the nodes must reach each other on their private addresses. Each node runs the OpenVidu PRO license you pass to the master.

## Port rules

These are the inbound ports `ov` checks, with the names it prints for them. The master carries the public API; the media nodes carry the media. Open them before deploying; `ov` checks them for you ([Check the ports first](../../single-node/on-premises/install.md#check-the-ports)).

=== "Master Node"

    | Port | Scope | Level | Description |
    | --- | --- | --- | --- |
    | `443/tcp` | public | required | Caddy: LiveKit API, Dashboard, Meet, WHIP API, TURN with TLS, custom layouts. |
    | `80/tcp` | public | recommended | Caddy: HTTP-to-HTTPS redirect and Let's Encrypt validation. |
    | `6443/tcp` | admin | required | Stack remote admin control protocol: the port your machine administers the stack through. |
    | `22/tcp` | admin | required | SSH: the port `ov` reaches the node through. |

    The master's firewall must let the pod networks `10.42.0.0/16` and `10.43.0.0/16` reach it. The media nodes reach the master's `6443/tcp` and `8472/udp` (Kubernetes cluster traffic).

=== "Media Node"

    | Port | Scope | Level | Description |
    | --- | --- | --- | --- |
    | `443/udp` | public | recommended | OpenVidu LiveKit Server: STUN/TURN over UDP. |
    | `50000-60000/udp` | public | recommended | OpenVidu LiveKit Server: WebRTC media over UDP. |
    | `7881/tcp` | public | recommended | OpenVidu LiveKit Server: WebRTC media over TCP. |
    | `22/tcp` | admin | required | SSH: the port `ov` reaches the node through. |
    | `10250/tcp` | internal | required | Kubernetes cluster traffic, from the master only. |
    | `8472/udp` | internal | required | Kubernetes cluster traffic, from the master only. |

With the `ingress` module, also open `1935/tcp` (RTMP) on the master and `7885/udp` (WHIP) on the media nodes. `join` checks the internal ports in both directions and prints the rule to add if one is closed.

## Deploy the master

Deploy the first machine as the master, exactly like a [Single Node PRO](../../single-node/on-premises/install.md#deploy) but with `--deployment-type elastic`:

```console
$ mkdir ov-elastic && cd ov-elastic
$ ov stack deploy el --edition pro --environment on-premises --deployment-type elastic \
    --ssh ubuntu@172.30.0.101 --ssh-key ~/.ssh/id_ed25519 \
    --openvidu-pro-license <your-license> \
    --domain-name 172-30-0-101.openvidu-local.dev \
    --certificate-type owncert --owncert-public-key ~/certs/fullchain.pem --owncert-private-key ~/certs/privkey.pem \
    --mode auto

…
   ✓ Check the inbound ports
…
✔ deploy completed.
wrote spec to openvidu-stack.yml
✔ stack "el" recorded in this directory
```

The stack is up with its data tier on the master, but its media services have nowhere to run yet.

## Join a media node

From the stack's directory, `ov stack join --ssh` checks the new machine's ports, installs the node agent and joins it:

```console
$ ov stack join --ssh ubuntu@172.30.0.102 --as media
→ reading the join address and token from 172.30.0.101
→ checking the ports of 172.30.0.102 from here and from the stack's masters
  …

▶ Join the cluster…
   ✓ Join the cluster
…

✔ 172.30.0.102 joined the stack as a media node.
```

If a required port is not reachable, the join stops before installing anything and prints the rule to add. The login and key default to the ones the stack recorded. The join returns once the node takes work. Each media node is one more `ov stack join --ssh`; see [Add a media node](admin.md#add-a-media-node) for the other ways to join.

## Install on the servers themselves, or review the commands first

As on a Single Node, you can put `ov` on the master and deploy with [`--this-node`](../../single-node/on-premises/install.md#install-on-the-server-itself), and [review every command before it runs with `--mode assisted`](../../single-node/on-premises/install.md#assisted-mode). With a master deployed with `--this-node`, join each media node on the machine itself with `ov stack join --this-node` ([Add a media node](admin.md#add-a-media-node)).

## Configure your application to use the deployment

Your application connects with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. Read them from the stack's directory:

```bash
ov stack config get livekit-api-key
ov stack config get livekit-api-secret
```

`LIVEKIT_URL` is your domain as `wss://yourdomain.example.io/` or `https://yourdomain.example.io/`.

## Configuration and administration

Once deployed, see [Administration](admin.md) to operate the stack, add and remove media nodes, change the configuration and back up its data.
