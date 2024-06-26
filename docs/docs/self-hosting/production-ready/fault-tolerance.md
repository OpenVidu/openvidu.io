# Fault Tolerance :material-shield-refresh:

Real-time media is particularly sensitive to downtime events, as they directly affect the user experience in a very disruptive way. OpenVidu is designed from the ground up to be fault tolerant in all its services in case of node downtime, especially in its High Availability deployment.

The extent of fault tolerance depends on the [OpenVidu deployment type](../deployment-types.md):

- **OpenVidu Single Node**: it is not fault tolerant. Fault tolerance requires a multi-node deployment.
- **OpenVidu Elastic**: fault tolerant only for Media Nodes.
- **OpenVidu High Availability**: fault tolerant for both Media Nodes and Master Nodes.

## Fault tolerance in OpenVidu Elastic

### Master Node

An OpenVidu Elastic deployment has a single Master Node, so a failure on this node is fatal and any ongoing video Rooms will be interrupted. The service won't be restored until the Master Node is recovered.

### Media Nodes

You can have any number of Media Nodes in an OpenVidu Elastic deployment. Media Nodes are stateless, meaning that they do not store critical information about the Rooms, Egress or Ingress processes they are handling. This means that they can be easily replicated in any other Media Node in case of a failure.

In the event of a Media Node failure, there are [3 services](../deployment-types.md#media-node-services) affected with the following behaviors:

- Active [Rooms](https://docs.livekit.io/realtime/concepts/api-primitives/){:target=_blank} hosted by the failed Media Node will suffer a temporary interruption of about 5 seconds (this is the time the clients take to realize the Media Node has crashed). After that time has elapsed, the Room will be automatically reconstructed in a healthy Media Node. Every participant and track will be recreated and the Room will be fully operational again.
- Active [Egress](https://docs.livekit.io/egress-ingress/egress/overview/){:target=_blank} hosted by the failed Media Node will be interrupted. If the node's disk is still accessible, egress output files can still be recovered. See [Recovering Egress from node failures](#recovering-egress-from-node-failures).
- Active [Ingress](https://docs.livekit.io/egress-ingress/ingress/overview/){:target=_blank} hosted by the failed Media Node will be interrupted. The participants of the Room will receive the proper [events](https://docs.livekit.io/realtime/client/events/#Events){:target=_blank} indicating the Ingress participant has left the Room: `TrackUnpublished` and `ParticipantDisconnected`. Some famous tools for streaming such as OBS Studio will automatically try to reconnect the stream when they detect a connection loss, so in this case interruption will be minimal and the Ingress tracks will be restored on their own on a healthy Media Node.

## Fault tolerance in OpenVidu High Availability

OpenVidu High Availability delivers the highest possible degree of fault tolerance. This is achieved by running all of the [services in the Master Nodes and the Media Nodes](../deployment-types.md#node-services) in their **High Availability** flavour.

An OpenVidu High Availability deployment runs Master Nodes and Media Nodes in separated groups. Let's see the extent of fault tolerance for each node group:

### Master Nodes

The number of Master Nodes in an OpenVidu High Availability deployment is **4**. This minimum number of nodes ensures that every service running in the Master Nodes is fault tolerant.

If **one** Master Node fails, the service won't be affected. Some users may trigger [event](https://docs.livekit.io/realtime/client/events/#Events){:target=_blank} `Reconnecting` closely followed by `Reconnected`, but the service will remain fully operational.

When two or more Master Nodes fail simultaneously, there can be some degradation of the service:

- If **two** Master Nodes fail, the service will still be operational for the most part. Only active [Egress](https://docs.livekit.io/egress-ingress/egress/overview/){:target=_blank} might be affected, as they won't be stored in the Minio storage. See [Recovering Egress from node failures](#recovering-egress-from-node-failures).
- If **three or four** Master Nodes fail, the service will be interrupted.

In the event of Master Node failures, the service will be automatically restored as soon as the failed node(s) are recovered.

### Media Nodes

Fault tolerance of Media Nodes in OpenVidu Elastic behaves the same as in [OpenVidu High Availability](#media-nodes).

## Recovering Egress from node failures

[Egress](https://docs.livekit.io/egress-ingress/egress/overview/){:target=_blank} processes can be affected by the crash of a Master Node or a Media Node. To recover Egress from...

### From Master Node failures

!!! info "This only applies to OpenVidu High Availability"

If 2 Master Nodes crash, the Egress process won't be able to use the Minio storage. This has different consequences depending on the [configured outputs](https://docs.livekit.io/egress-ingress/egress/overview/#Supported-Outputs){:target=_blank} for your Egress process:

- For **MP4, OGG or WEBM files**, if the Egress is stopped when 2 Master Nodes are down, the output files will not be uploaded to Minio.
- For **HLS**, the segments will stop being uploaded to Minio. If you are consuming these segments from another process, note that new segments will stop appearing.

In both cases, files are not lost and can be recovered. They will be available in the Egress backup path of the Media Node hosting the Egress process (by default `/opt/openvidu/egress_data/home/egress/backup_storage`).

### From a Media Node failure

!!! info "This applies to both OpenVidu High Availability and OpenVidu Elastic"

If the Media Node hosting an ongoing Egress process crashes, then the Egress process will be immediately interrupted. But as long as the disk of the crashed Media Node is still accessible, you may recover the output files. They will be available in the Media Node at path `/opt/openvidu/egress_data/home/egress/tmp`.

It is possible that if the crashed Egress had **MP4** as [configured output](https://docs.livekit.io/egress-ingress/egress/overview/#Supported-Outputs){:target=_blank} (which is an option available for [Room Composite](https://docs.livekit.io/egress-ingress/egress/overview/#Room-Composite-Egress){:target=_blank} and [Track Composite](https://docs.livekit.io/egress-ingress/egress/overview/#Track-Composite-Egress){:target=_blank}) the recovered file may not be directly playable and it may require a repair process.
