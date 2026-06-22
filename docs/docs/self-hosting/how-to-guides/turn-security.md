---
title: TURN server security
description: Understand how OpenVidu's embedded TURN server protects relayed media — peer IP allowlist, relay port restriction, disabled TCP relays — and the configuration values that control it.
---

# TURN server security

OpenVidu embeds a [TURN](https://en.wikipedia.org/wiki/Traversal_Using_Relays_around_NAT){:target="_blank"} server so that clients on restrictive networks can still exchange WebRTC media: when a direct WebRTC connection is not possible, media is relayed through the TURN server on port `443` (UDP) or over `443` TLS. See [Force media traffic through port 443](force-single-port.md) for the networking side of this.

A TURN relay is, by design, a packet forwarder. Left unrestricted, an authenticated client could try to use it as an open proxy to reach hosts and ports it should never touch — a well-documented class of attack (see [TURN security best practices](https://www.enablesecurity.com/blog/turn-security-best-practices/){:target="_blank"} by Enable Security). To prevent this, OpenVidu's TURN server ships with several **security mechanisms enabled by default**. This guide explains that behavior and the configuration values that control it.

## Why the relay needs protecting

On startup, each node determines whether it is **publicly reachable** on the WebRTC media port range:

- If a 1-to-1 NAT public IP is configured, the node is considered publicly reachable.
- If the node's announced IP is one of its own local interface IPs, it is **not** publicly reachable.
- Otherwise OpenVidu runs a **UDP hairpin test**: it sends a packet to its own public IP on a port from the media range and checks whether it comes back. If it does not (the media ports are not open from the outside, the node sits in a private network, or there is a reverse proxy in front), the node is marked **not publicly reachable**.

When a node is **not** publicly reachable, OpenVidu auto-configures itself to keep working: it announces the node's **private IP as the TURN relay candidate** and routes media through TURN on `443` (UDP) or TLS. This is what makes OpenVidu work behind NAT or behind a proxy without manual tuning — but it also means the relay is now reachable and advertises an internal address, which is precisely why the default security mechanisms below matter.

!!! info
    You can see which address a node picked as its relay candidate in the logs:
    ```bash
    docker logs openvidu 2>&1 | grep "TURN relay address"
    # INFO  openvidu  service/turn.go  Using first local IP as TURN relay address  {"relayAddress": "192.168.1.10", ...}
    ```

## Default security mechanisms

These protections are active out of the box, on every deployment type, and require no configuration.

### Peer IP allowlist

The TURN server only relays traffic to a restricted set of peer IPs:

- The node's **own local interface IPs** (the embedded relay may need to forward to any local interface, e.g. a Docker bridge), and...
- The IPs of **registered cluster nodes**. In Elastic and High Availability deployments this set is maintained dynamically from the shared cluster state, so newly added nodes are picked up automatically; in Single Node it is the node's own IP / relay address.

Any attempt to create a permission for an IP outside this set (a public host, the cloud metadata endpoint, an arbitrary internal host, …) is rejected. The relay cannot be used to reach destinations that are not part of the OpenVidu deployment.

### Relay port restriction

Every relayed packet is validated **at the packet level** against the configured WebRTC media port range (`rtc.port_range_start`–`rtc.port_range_end`, `50000`–`60000` by default). Packets destined to a port outside this range are dropped.

!!! warning
    If no media port range is configured, **all** relay ports are denied. The relay only ever forwards to the media port range used by the Media Servers.

### TCP relay disabled (RFC 6062)

[RFC 6062](https://datatracker.ietf.org/doc/html/rfc6062){:target="_blank"} (TURN Extensions for TCP Allocations) lets a client ask the server to relay traffic to a peer over an **outbound TCP connection** (`Connect` / `ConnectionBind`). OpenVidu **disables this by default**: clients can only allocate UDP relays, which is all WebRTC media needs. TCP allocation requests are rejected.

### Time-limited, per-participant credentials

TURN credentials are not static. They are derived per participant from the deployment's API key/secret and are time-limited (`turn.ttl_seconds`, `300` s by default). The expiry is enforced on the initial relay allocation.

## Configuration values

All TURN security settings live under the `turn:` section of the LiveKit configuration file:

=== "Single Node"

    `/opt/openvidu/config/livekit.yaml`

=== "Elastic / High Availability"

    `/opt/openvidu/config/cluster/media_node/livekit.yaml`

```yaml
turn:
    # ... other properties ...

    # Enable RFC 6062 (TURN TCP allocations). Disabled by default; clients can
    # only allocate UDP relays unless this is set to true.
    enable_rfc6062: false

    # Peer CIDRs explicitly allowed to be relayed to. Any peer IP in one of these
    # CIDRs is permitted, regardless of whether it is private, public or a cluster
    # node. In addition, when this list is non-empty, restricted peer IPs
    # (loopback, link-local, multicast, private, unspecified) that are NOT listed
    # here are denied. Empty by default.
    allow_restricted_peer_cidrs:
        - 10.0.0.0/8

    # Peer CIDRs to deny. Applies to all peer IPs and takes precedence over
    # everything else (allow list, local IPs and cluster nodes). Empty by default.
    deny_peer_cidrs:
        - 169.254.0.0/16

    # Explicitly set the relay IP advertised by TURN (skips auto-discovery).
    # relay_address: 10.0.0.1

    # Network interface to take the relay address from during auto-discovery on
    # nodes that are not publicly reachable. Ignored when relay_address is set or
    # the node is publicly reachable.
    # relay_preferred_interface: eth0
```

| Property | Type | Default | Description |
| -------- | ---- | ------- | ----------- |
| `enable_rfc6062` | boolean | `false` | Allow TURN TCP allocations (RFC 6062). Keep disabled unless you specifically need TCP relays. |
| `allow_restricted_peer_cidrs` | list | _empty_ | CIDRs whose peer IPs are explicitly allowed to be relayed to. When non-empty, also denies restricted peer IPs not listed. |
| `deny_peer_cidrs` | list | _empty_ | CIDRs whose peer IPs are denied. Takes precedence over the allow list, local IPs and cluster nodes. |
| `relay_address` | string | _auto_ | Force the relay IP. Overrides auto-discovery. |
| `relay_preferred_interface` | string | _auto_ | Interface to source the relay IP from when the node is not publicly reachable. |

After changing any of these values, restart the service:

```bash
systemctl restart openvidu
```

### How the relay permission decision is made

For a given peer IP, the TURN server decides whether to allow a relay permission in this order (first match wins):

1. The IP matches `deny_peer_cidrs` → **denied**.
2. The IP matches `allow_restricted_peer_cidrs` → **allowed**.
3. An allow list is configured **and** the IP is restricted (private, loopback, link-local, multicast, unspecified) and not listed → **denied**.
4. The IP is one of the node's local interface IPs or a registered cluster node → **allowed**.
5. Otherwise → **denied**.

Independently, the **relay port restriction** and the **RFC 6062** check are always applied when forwarding packets and when allocating relays, respectively.

!!! danger "Don't lock out your own nodes"
    The allow/deny CIDR checks run **before** the built-in local/cluster allowlist. If you set `allow_restricted_peer_cidrs` to a range that does **not** include your nodes' private subnets, the relay will deny traffic to your own Media Servers and **media will stop flowing**. When you use an allow list, always include the local/cluster ranges. Likewise, a `deny_peer_cidrs` entry that covers a cluster node's IP will block media to that node.

## Considerations

- These mechanisms protect the relay; they do not change how media is encrypted. WebRTC media is always encrypted (SRTP/DTLS), whether relayed or not.
- In most deployments you should not need to touch any of these values. The defaults already block relay abuse while allowing legitimate intra-cluster media.
- Use `allow_restricted_peer_cidrs` / `deny_peer_cidrs` only for advanced scenarios (e.g. allowing an additional trusted peer range, or explicitly blocking a subnet).

## Related guides

- [Force media traffic through port 443](force-single-port.md)
- [Deploy and configure with an external proxy](deploy-with-external-proxy.md)
- [TURN security best practices](https://www.enablesecurity.com/blog/turn-security-best-practices/){:target="_blank"}