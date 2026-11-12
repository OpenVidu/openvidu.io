---
title: "Force media traffic through port 443"
description: "Run OpenVidu with port 443 as its only open port, so media still reaches users behind corporate firewalls that block everything else."
---

# Force media traffic through port 443

By default, OpenVidu uses a range of ports for WebRTC traffic. However, in certain scenarios, you may need to route all traffic through a single port (443), either over UDP or TLS. This guide explains how to configure the port rules to achieve this.

## 443 UDP

When you want all WebRTC media traffic to be routed through port 443 UDP using TURN, you need to close the ports used for direct WebRTC communication. This forces all media to go through the TURN server on port 443 UDP.

To enforce this configuration, your inbound port rules should look like this:

=== "Single Node"

    **Inbound port rules**:

    | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
    | -------- | ----- | ------ | ----------- |
    | TCP | 80 | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
    | TCP | 443 | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
    | UDP | 443 | 0.0.0.0/0, ::/0 | TURN server over UDP. |
    | TCP | 1935 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to ingest RTMP streams using Ingress service. |
    | TCP | 9000 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to expose MinIO publicly. |
    | UDP | 50000-60000 | Own Node | Open only these ports internally so the node itself via its own private IP can reach itself. Needed for TURN to relay media to the Media Servers. |

    Also keep the admin ports open to the machine you run `ov` from, as in the [install port rules](../single-node/on-premises/install.md#port-rules): `22/tcp` (SSH) and, on a **PRO**{ .openvidu-tag .openvidu-pro-tag } single node, `6443/tcp` (stack remote admin control protocol).

    **Outbound port rules**:

    All outbound is recommended. If not possible, at least the following rules should be added:

    - Internet access for the node itself to download Docker images and installation. Also, requests to `accounts.openvidu.io` are needed for OpenVidu PRO license validation.
    - Internal access to the node itself via its own private IP for TURN to relay media to the Media Servers.

=== "Elastic"

    === "Master Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | TCP | 80 | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
        | TCP | 443 | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
        | TCP | 1935 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to ingest RTMP streams using Ingress service. |
        | TCP | 9000 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to expose MinIO publicly. |

        Keep the admin ports and the Kubernetes cluster traffic between the master and the media nodes as described in the [Elastic install port rules](../elastic/on-premises/install.md#port-rules). An Elastic stack is PRO on Kubernetes, so the data services (Redis, MongoDB, MinIO) and the other OpenVidu services run as pods and communicate over the pod network, not over host ports between nodes.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Media Nodes via their private IPs.


    === "Media Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | UDP | 443 | 0.0.0.0/0, ::/0 | STUN/TURN over UDP. |
        | UDP | 50000-60000 | Media Nodes | Open only these ports internally. Needed for TURN to relay media to the Media Servers. |

        The media nodes also carry the Kubernetes cluster traffic from the master (`10250/tcp`, `8472/udp`), as described in the [Elastic install port rules](../elastic/on-premises/install.md#port-rules). The external services run as pods over the pod network, so no inter-node host ports to Redis, MongoDB, MinIO, Loki or Mimir are needed.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Nodes via their private IPs.
        - Internal access to the Media Nodes via their private IPs for TURN to relay media to the Media Servers.

=== "High Availability"

    === "Master Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-15em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | TCP | 1945 | Load Balancer | Needed for RTMP Ingress service. Master Nodes need access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
        | TCP | 5349 | Load Balancer | Needed for TURN with TLS. Master Nodes need access to this port to reach TURN service and expose it using TLS (TURNS). |
        | TCP | 7880 | Load Balancer | Allows access to the following to the Load Balancer: <ul><li>LiveKit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>Custom layouts</li></ul> |

        Keep the Kubernetes cluster traffic as described in the [High Availability install port rules](../ha/on-premises/install-nlb.md#port-rules): `6443/tcp` and `2379-2380/tcp` between the master nodes, and `10250/tcp` and `8472/udp` across the nodes. A High Availability stack is PRO on Kubernetes, so the data services (Redis, MongoDB, MinIO) and observability run as pods and communicate over the pod network, not over host ports between nodes.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Nodes via their private IPs.
        - Internal access to the Media Nodes via their private IPs.

    === "Media Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | UDP | 443 | 0.0.0.0/0, ::/0 | STUN/TURN over UDP. |
        | UDP | 50000-60000 | Media Nodes | Open only these ports internally. Needed for TURN to relay media to the Media Servers. |

        The media nodes also carry the Kubernetes cluster traffic from the master nodes (`10250/tcp`, `8472/udp`), as described in the [High Availability install port rules](../ha/on-premises/install-nlb.md#port-rules). The external services run as pods over the pod network, so no inter-node host ports to Redis, MongoDB, MinIO, Loki or Mimir are needed.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Nodes via their private IPs.
        - Internal access to the Media Nodes via their private IPs for TURN to relay media to the Media Servers.

## 443 TLS

In certain scenarios, users may be behind restrictive firewalls or network policies that only permit traffic through port 443 using TLS. By default, OpenVidu is configured to support TURN with TLS using the main domain name. This allows users behind restrictive firewalls to connect through port 443.

In some cases, it is necessary to ensure that all traffic, including WebRTC, is routed through port 443 with TLS due to network policies, security requirements, or other considerations.

To enforce this configuration, your inbound port rules should look like this:

=== "Single Node"

    **Inbound port rules**:

    | Protocol | Ports | <div class="w-8em">Source</div> | Description |
    | -------- | ----- | ------ | ----------- |
    | TCP | 80 | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
    | TCP | 443 | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
    | TCP | 1935 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to ingest RTMP streams using Ingress service. |
    | TCP | 9000 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to expose MinIO publicly. |
    | UDP | 50000-60000 | Own Node | Open only these ports internally so the node itself via its own private IP can reach itself. Needed for TURN to relay media to the Media Servers. |

    Also keep the admin ports open to the machine you run `ov` from, as in the [install port rules](../single-node/on-premises/install.md#port-rules): `22/tcp` (SSH) and, on a **PRO**{ .openvidu-tag .openvidu-pro-tag } single node, `6443/tcp` (stack remote admin control protocol).

    **Outbound port rules**:

    All outbound is recommended. If not possible, at least the following rules should be added:

    - Internet access for the node itself to download Docker images and installation. Also, requests to `accounts.openvidu.io` are needed for OpenVidu PRO license validation.
    - Internal access to the node itself via its own private IP for TURN to relay media to the Media Servers.

=== "Elastic"

    === "Master Node"

        **Inbound port rules**:

        | Protocol | Ports | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | TCP | 80 | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
        | TCP | 443 | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
        | TCP | 1935 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to ingest RTMP streams using Ingress service. |
        | TCP | 9000 | 0.0.0.0/0, ::/0 | (Optional) Needed if you want to expose MinIO publicly. |

        Keep the admin ports and the Kubernetes cluster traffic between the master and the media nodes as described in the [Elastic install port rules](../elastic/on-premises/install.md#port-rules). An Elastic stack is PRO on Kubernetes, so the data services (Redis, MongoDB, MinIO) and the other OpenVidu services run as pods and communicate over the pod network, not over host ports between nodes.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Media Nodes via their private IPs.

    === "Media Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | UDP | 50000-60000 | Media Nodes | Open only these ports internally. Needed for TURN to relay media to the Media Servers. |

        The media nodes also carry the Kubernetes cluster traffic from the master (`10250/tcp`, `8472/udp`), as described in the [Elastic install port rules](../elastic/on-premises/install.md#port-rules). The external services run as pods over the pod network, so no inter-node host ports to Redis, MongoDB, MinIO, Loki or Mimir are needed.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Node via its private IP.
        - Internal access to the Media Nodes via their private IPs for TURN to relay media to the Media Servers.

=== "High Availability"

    === "Master Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-15em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | TCP | 1945 | Load Balancer | Needed for RTMP Ingress service. Master Nodes need access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
        | TCP | 5349 | Load Balancer | Needed for TURN with TLS. Master Nodes need access to this port to reach TURN service and expose it using TLS (TURNS). |
        | TCP | 7880 | Load Balancer | Allows access to the following to the Load Balancer: <ul><li>LiveKit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>Custom layouts</li></ul> |

        Keep the Kubernetes cluster traffic as described in the [High Availability install port rules](../ha/on-premises/install-nlb.md#port-rules): `6443/tcp` and `2379-2380/tcp` between the master nodes, and `10250/tcp` and `8472/udp` across the nodes. A High Availability stack is PRO on Kubernetes, so the data services (Redis, MongoDB, MinIO) and observability run as pods and communicate over the pod network, not over host ports between nodes.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Nodes via their private IPs.
        - Internal access to the Media Nodes via their private IPs.

    === "Media Node"

        **Inbound port rules**:

        | Protocol | <div class="w-8em">Ports</div> | <div class="w-8em">Source</div> | Description |
        | -------- | ----- | ------ | ----------- |
        | UDP | 50000-60000 | Media Nodes | Open only these ports internally. Needed for TURN to relay media to the Media Servers. |

        The media nodes also carry the Kubernetes cluster traffic from the master nodes (`10250/tcp`, `8472/udp`), as described in the [High Availability install port rules](../ha/on-premises/install-nlb.md#port-rules). The external services run as pods over the pod network, so no inter-node host ports to Redis, MongoDB, MinIO, Loki or Mimir are needed.

        **Outbound port rules**:

        All outbound is recommended. If not possible, at least the following rules should be added:

        - Internet access for the node itself to download Docker images, installation and requests to `accounts.openvidu.io` for OpenVidu PRO license validation.
        - Internal access to the Master Nodes via their private IPs.
        - Internal access to the Media Nodes via their private IPs for TURN to relay media to the Media Servers.

## Restart required

!!! info
    If you are installing OpenVidu for the first time, you can configure the ports before starting the service. In this case, no restart is needed.

After closing ports, the media services must be restarted so they autoconfigure with the new port rules. Restart the whole stack with the CLI, which restarts the services on every node:

```bash
ov stack restart
```

## How it works

Both configurations work thanks to the [TURN protocol :fontawesome-solid-external-link:{.external-link-icon}](https://en.wikipedia.org/wiki/Traversal_Using_Relays_around_NAT){:target="_blank"}, which acts as a relay between the client and the Media Server. When a client connects through port 443 (either UDP or TLS), the TURN server receives the traffic on that port and relays it internally to the Media Server. This relay happens entirely within the internal network: the TURN server presents the node's private IP as the relay address and forwards the media to the Media Server using the configured RTC port range (50000-60000 by default).

This is why the port rules above require the internal UDP range (50000-60000) to be open between cluster nodes (or to the node itself in Single Node deployments) — it is the path used by TURN to deliver relayed media to the Media Server.

OpenVidu includes built-in security layers in its TURN server implementation to ensure relay connections are tightly controlled:

- **Cluster-aware IP allowlist**: TURN only permits relay traffic to IPs belonging to registered cluster nodes. In multi-node deployments, this is dynamically maintained via the shared cluster state, so only legitimate nodes can receive relayed media.
- **Port range enforcement**: Every relayed packet is validated against the configured RTC port range at the packet level. Traffic destined to ports outside this range is rejected.
- **TCP relay denial**: TCP relay allocations ([RFC 6062 :fontawesome-solid-external-link:{.external-link-icon}](https://datatracker.ietf.org/doc/html/rfc6062){:target="_blank"}) are denied by default ([`turn.enable_rfc6062`](turn-security.md#tcp-relay-disabled-rfc-6062)), limiting TURN to its intended use for UDP media relay.

## Troubleshooting: media not flowing

If media is not flowing after applying the port rules above, check the following:

### 1. Verify internal port rules

Ensure that the internal UDP port range used by TURN for relay is open between your nodes:

- **Outgoing**: UDP ports 40000-50000 from the TURN server.
- **Incoming**: UDP ports 50000-60000 to the Media Server.

Both ranges must be reachable within the internal network between Media Nodes (or to the node itself in Single Node deployments).

### 2. Verify the relay IP

By default, OpenVidu automatically detects the best possible private IP of each node to use as the TURN relay address, and in most cases no manual configuration is needed. You can check which address is being used by looking at the OpenVidu logs:

```bash
ov stack logs 2>&1 | grep "TURN relay address"
```

You should see a log entry like:

```
INFO    openvidu    service/turn.go:204    Using first local IP as TURN relay address    {"relayAddress": "192.168.1.10", "preferredInterface": ""}
```

If the `relayAddress` does not match the node's private IP used to communicate with other cluster nodes (e.g., the node has multiple network interfaces), media relay will fail because traffic will be sent to an unreachable address.

To fix this, explicitly set the network interface that TURN should use for relay, in the media server's `livekit.yaml` service file. Edit it with the CLI, which applies the change and restarts the media server when you save:

```bash
ov stack config file edit livekit.yaml
```

Set the interface under the `turn:` section:

```yaml
turn:
  # ... other properties ...
  relay_preferred_interface: <interface-name>
```

Where `<interface-name>` is the network interface used by the node to communicate with other nodes in the cluster (e.g., `eth0`, `ens5`). For Single Node deployments, it should be the main network interface of the machine.

## Considerations

- Media over UDP using WebRTC does not mean that the media is not encrypted. WebRTC encrypts the media using SRTP and DTLS. WebRTC is designed to be encrypted by default.
- Media going through 443 UDP has a minor performance impact compared to direct WebRTC. Since all media is relayed through the TURN server, it is processed twice (by the TURN server and the Media Server), which adds some latency and CPU overhead. However, because UDP is still used, the impact is significantly lower than with TLS.
- Media going through 443 with TLS has a greater penalty in media quality and CPU usage. This is because of the TLS roundtrip, TCP being used and media processed twice by the TURN server and the Media Server. This can lead to a worse user experience and higher CPU usage in the Media Server. Additionally, in Elastic and High Availability deployments, all media traffic will flow through the Master Node (or Load Balancer), which can become a bottleneck as the number of participants grows. We recommend using this configuration only if it is strictly necessary.
