---
title: "Fault tolerance in OpenVidu deployments"
description: "How OpenVidu survives losing a node: which services are replicated, what happens to a room in progress, and what Elastic and HA each guarantee."
page_features:
  - revealonscroll
---

# Fault tolerance :material-shield-refresh:

Real-time media is particularly sensitive to downtime events, as they directly affect the user experience in a very disruptive way. OpenVidu is designed from the ground up to be fault tolerant in all its services in case of node downtime, especially in its High Availability deployment.

The extent of fault tolerance depends on the [OpenVidu deployment type](../deployment-types.md):

- **OpenVidu Single Node**: it is not fault tolerant. Fault tolerance requires a multi-node deployment.
- **OpenVidu Elastic**: fault tolerant only for Media Nodes.
- **OpenVidu High Availability**: fault tolerant for both Media Nodes and Master Nodes.

## Fault tolerance in OpenVidu Elastic

### Master Node

An OpenVidu Elastic deployment has a single Master Node, so a failure of this node is fatal and any ongoing video Rooms will be interrupted. The service won't be restored until the Master Node is recovered.

### Media Nodes

You can have any number of Media Nodes in an OpenVidu Elastic deployment. Media Nodes are stateless, meaning that they do not store critical information about the Rooms, Egress or Ingress processes they are handling. This means that they can be easily replicated in any other Media Node in case of a failure.

In the event of a Media Node failure, there are [3 services](../deployment-types.md#media-node-services) affected with the following behaviors:

- Active [Rooms :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/basics/rooms-participants-tracks/){:target="_blank"} hosted by the failed Media Node will suffer a temporary interruption of about 5 seconds (this is the time the clients take to realize the Media Node has crashed). After that time has elapsed, the Room will be automatically reconstructed in a healthy Media Node. Every participant and track will be recreated and the Room will be fully operational again.
- Active [Egress](../../reference/egress.md) hosted by the failed Media Node will be interrupted. If the node's disk is still accessible, egress output files can still be recovered. See [Recovering Egress from node failures](#recovering-egress-from-node-failures).
- Active [Ingress](../../reference/ingress.md) hosted by the failed Media Node will be interrupted. The participants of the Room will receive the proper [events](../../reference/client-sdk.md#room-events) indicating the Ingress participant has left the Room: `TrackUnpublished` and `ParticipantDisconnected`. Some popular tools for streaming such as OBS Studio will automatically try to reconnect the stream when they detect a connection loss, so in this case interruption will be minimal and the Ingress tracks will be restored on their own on a healthy Media Node.

## Fault tolerance in OpenVidu High Availability

OpenVidu High Availability delivers the highest possible degree of fault tolerance. This is achieved by running all of the [services in the Master Nodes and the Media Nodes](../deployment-types.md#node-services) in their **High Availability** flavour.

An OpenVidu High Availability deployment runs Master Nodes and Media Nodes in separate groups. Let's see the extent of fault tolerance for each node group:

### Master Nodes

The number of Master Nodes in an OpenVidu High Availability deployment is **4**. This minimum number of nodes ensures that every service running in the Master Nodes is fault tolerant.

If **one** Master Node fails, the service won't be affected. Some users may trigger [event](../../reference/client-sdk.md#room-events) `Reconnecting` closely followed by `Reconnected`, but the service will remain fully operational.

When two or more Master Nodes fail simultaneously, there can be some degradation of the service:

- If **two** Master Nodes fail, the service will still be operational for the most part. Only active [Egress](../../reference/egress.md) might be affected, as they won't be stored in the Minio storage. See [Recovering Egress from node failures](#recovering-egress-from-node-failures).
- If **three or four** Master Nodes fail, the service will be interrupted.

In the event of Master Node failures, the service will be automatically restored as soon as the failed node(s) are recovered.

### Media Nodes

Fault tolerance of Media Nodes in OpenVidu High Availability behaves the same as in [OpenVidu Elastic](#media-nodes).

## Fault tolerance in cloud providers

When OpenVidu Elastic or OpenVidu High Availability is deployed in a cloud provider with the official templates, all of their Media Nodes are replaced automatically when they become unhealthy, keeping the same number of Media Nodes. This applies whether the number of Media Nodes is fixed or managed by autoscaling.

### Detecting an unhealthy Media Node

Every Media Node runs a health watchdog, the `openvidu-media-health` systemd service, that checks the media server of the node every 30 seconds. The watchdog asks the cloud provider to replace the node when:

- The media server does not accept connections for **5 minutes**.
- The media server answers with errors or timeouts for **10 minutes**. These failures are not counted while the CPU of the node is saturated, because an overloaded media server briefly reports itself as not ready.
- The installation of the node failed. The watchdog waits **10 minutes** before acting, so the failure can be inspected and a persistent problem does not create new nodes in a loop.
- The installation of the node has not finished **90 minutes** after it booted.

An unhealthy Media Node does not wait for its Rooms, Egress and Ingress to finish, as a node does during a regular scale-in. They are affected as described in [Media Nodes](#media-nodes), so its Rooms are rebuilt in a healthy Media Node.

### Safeguards

- **No Media Node is replaced while no Master Node is reachable.** A Master Node outage makes every Media Node fail its health check at once, and a new Media Node could not join the cluster either. Once a Master Node is back, the media server gets its full time window to reconnect before the watchdog acts.
- **Failures are not counted during the first 15 minutes** after OpenVidu starts or restarts on the node.
- **The watchdog pauses itself while the node is draining** during a regular scale-in.

### How each cloud provider replaces the node

=== ":fontawesome-brands-aws:{.icon .lg-icon .tab-icon} AWS"

    The Media Node is marked as unhealthy in its Auto Scaling Group, which terminates it and launches a new one.

=== ":material-microsoft-azure:{.icon .lg-icon .tab-icon} Azure"

    The Media Node is reimaged in its Virtual Machine Scale Set, so the number of instances never changes.

=== ":fontawesome-brands-google:{.icon .lg-icon .tab-icon} GCP"

    The Media Node is recreated in its managed instance group with a fresh disk. In addition, the native autohealing of the group (a TCP health check on port 7880) recreates any Media Node VM that stops responding altogether.

=== ":fontawesome-brands-digital-ocean:{.icon .lg-icon .tab-icon} DigitalOcean"

    - **With autoscaling**: the Media Node is tagged so the autoscaler deletes it and creates a new one.
    - **With a fixed number of Media Nodes**: the Droplet is rebuilt in place.

=== ":custom-oracle-cloud-infrastructure:{.icon .lg-icon .tab-icon} OCI"

    - **With autoscaling**: the Media Node is terminated and its instance pool launches a new one.
    - **With a fixed number of Media Nodes**: the node is detached from its instance pool, which launches its replacement, and then terminated.

### Monitoring and pausing the watchdog

To see what the watchdog is doing, run this command in the Media Node:

```bash
journalctl -u openvidu-media-health
```

To pause the watchdog, for example during manual maintenance of the node, create this file:

```bash
sudo touch /etc/openvidu/media-health.disabled
```

Delete the file to resume it:

```bash
sudo rm /etc/openvidu/media-health.disabled
```

## Recovering Egress from node failures

[Egress](../../reference/egress.md) processes can be affected by the crash of a Master Node or a Media Node. To recover Egress from...

### From Master Node failures

!!! info "This only applies to OpenVidu High Availability"

If 2 Master Nodes crash, the Egress process won't be able to use the Minio storage. This has different consequences depending on the [configured outputs](../../reference/egress.md#outputs) for your Egress process:

- For **MP4, OGG or WEBM files**, if the Egress is stopped when 2 Master Nodes are down, the output files will not be uploaded to Minio.
- For **HLS**, the segments will stop being uploaded to Minio. If you are consuming these segments from another process, note that new segments will stop appearing.

In both cases, files are not lost and can be recovered. They will be available in the Egress backup path of the Media Node hosting the Egress process (by default `/opt/openvidu/egress_data/home/egress/backup_storage`).

### From a Media Node failure

!!! info "This applies to both OpenVidu High Availability and OpenVidu Elastic"

If the Media Node hosting an ongoing Egress process crashes, then the Egress process will be immediately interrupted. But as long as the disk of the crashed Media Node is still accessible, you may recover the output files. They will be available in the Media Node at path `/opt/openvidu/egress_data/home/egress/tmp`.

It is possible that if the crashed Egress had **MP4** as [configured output](../../reference/egress.md#outputs) (which is an option available for [Room Composite](../../reference/egress.md#egress-types) and [Track Composite](../../reference/egress.md#egress-types)) the recovered file may not be directly playable and it may require a repair process.

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Need specific uptime or SLA guarantees?</h2>
  <p class="cta-lead">Tell us your availability requirements and we will help you choose between Elastic and High Availability.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
