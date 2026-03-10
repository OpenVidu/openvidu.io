# Troubleshooting recordings

## Introduction

This is a guide to help identify and solve common issues related to recordings in OpenVidu.

Recordings are handled by the **Egress service** in OpenVidu, built on top of [LiveKit Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/){:target="\_blank"}. There are some general considerations to take into account:

- Recordings are **CPU intensive operations**. For recordings to work smoothly, the nodes hosting the Egress service must have sufficient free cores.
- The first symptom of something going wrong with recordings is usually **missing recordings**: you are expecting recording files to be available in your storage, but they are simply not there. Other common symptom is receiving an **error `503 Service Unavailable`** when starting a new recording [on-demand](#on-demand-vs-automatic-recordings).
- To be proactive when dealing with recording issues, **it is highly recommended to enable webhooks** in your OpenVidu deployment ([learn how](../self-hosting/how-to-guides/enable-webhooks.md)) and monitor it from your application's backend. In this way you can be notified of Egress-related events and errors as they happen.

### On-demand vs Automatic recordings

Recordings can be started **on-demand** or **automatically**:

- **On-demand recordings** are started by calling any of the these operations of the [LiveKit Egress API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/){:target="\_blank"}:
    - `StartRoomCompositeEgress`
    - `StartTrackCompositeEgress`
    - `StartParticipantEgress`
    - `StartTrackEgress`
    - `StartWebEgress`
- **Automatic recordings** are started when a room is created with auto-egress enabled. To do so just include an `egress` field when calling the [`CreateRoom` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#createroom){:target="\_blank"} method: then the room will be automatically recorded during its lifetime. See [auto-egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/autoegress/){:target="\_blank"} documentation for more details.

!!! warning

    It is important to distinguish between **on-demand recordings** and **automatic recordings** for a simple reason: your application is able to catch and handle errors when starting on-demand recordings, while automatic recordings will fail silently.

## List of possible recording issues

Below are some of the most common issues related to recordings in OpenVidu, along with their symptoms and possible solutions.

### CPU exhausted

**Description**

There are not enough free CPU cores to start a new egress.

**Symptoms**

- The operation to start a new egress returns a `503 Service Unavailable` error (text of the error: `no response from servers`). This applies when [starting egress on-demand](#on-demand-vs-automatic-recordings) from your application.
- Log lines of level `WARN` displaying `can not accept request` in service "egress". A typical log line of this type looks like this:

    ```{ .log .no-copy }
    2026-03-10T10:47:56.215Z	WARN	egress	stats/monitor.go:204 can not accept request
    {"nodeID": "NE_ynSpFdP6xfAS", "clusterID": "", "total": 16, "available": 3.175, "pending": 0,
    "used": 6.258, "activeRequests": 4, "activeWeb": 4, "memory": 2.9882, "memorySource": "proc_rss",
    "required": 4, "canAccept": false, "reason": "cpu", "error": "not enough CPU"}
    ```

- Log lines displaying `CPU exhausted` in service "egress".
- Log lines displaying `pipeline frozen` in service "egress".
- Log lines displaying `Can't record audio fast enough` in service "egress".

**Solutions**

- Scale out your OpenVidu deployment: deploy it in nodes with more CPU cores or add more Media Nodes to your cluster.
- Consider using a less CPU intensive egress type: [Track Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/track/){:target="\_blank"} does not require transcoding and composition, so it is much less CPU intensive than other egress types such as [Room Composite Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/media/ingress-egress/egress/composite-recording/){:target="\_blank"}.
- Review your [`egress.yaml` configuration file](../self-hosting/configuration/changing-config.md#config-files), specifically the properties within `cpu_cost`:

    ```yaml
    cpu_cost:
        max_cpu_utilization: 0.8
        room_composite_cpu_cost: 2.0
        audio_room_composite_cpu_cost: 1.0
        web_cpu_cost: 2.0
        audio_web_cpu_cost: 0.5
        participant_cpu_cost: 1.0
        track_composite_cpu_cost: 1.0
        track_cpu_cost: 0.5
    ```

    These properties determine two different things. OpenVidu configures sane defaults in all of them to prevent CPU exhaustion in most scenarios, but you may want to review and adjust them according to your specific use case:

    - The **`max_cpu_utilization`** property is the CPU usage threshold of the node above which the egress service won't accept new requests.
    - All the **`[...]_cpu_cost`** properties determine the amount of free CPU cores required in the node to accept a new egress request of each type.

!!! info "We strongly recommend reading the [Load balancing of egress](../self-hosting/production-ready/scalability.md#egress) documentation."

### Wrong auto-egress configuration

**Description**

By default, OpenVidu will automatically create a new room when a user tries to connect to a room that does not exist yet. This behavior can be disabled in [`livekit.yaml` configuration file](../self-hosting/configuration/changing-config.md#config-files):

```yaml
room:
  auto_create: false
```

When a room is auto-created on participant join, OpenVidu uses the room settings included in that participant’s token ([`RoomConfiguration` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#roomconfiguration){:target="\_blank"}).

A common problem appears when these chain of events happens:

1. Your application's backend explicitly creates a room with a specific `RoomConfiguration`. For example, with an `egress` field to enable auto-egress.
2. The room is unexpectedly deleted because of a timeout (properties `departure_timeout` or `empty_timeout` in [`livekit.yaml`](../self-hosting/configuration/changing-config.md#config-files)).
3. A participant tries to join the room using a token that does not include the same `egress` field in its `RoomConfiguration`.
4. OpenVidu auto-creates the room again, but now using the token’s `RoomConfiguration`, not the original one.

In this case, the room will not have auto-egress enabled, and therefore it will not be recorded. This behavior is also silent, as it is not an actual error but just a logic issue in your application.

**Symptoms**

You encounter this set of logs related to a room (in this example, room `DailyMeeting`):

1. You explicitly create the room from your application's backend with autoegress enabled:

    ```{ .log .no-copy }
    2026-01-19T09:00:03.302Z   INFO   openvidu.api   service/twirp.go:128   API RoomService.CreateRoom
    {"service": "RoomService", "method": "CreateRoom", "room": "DailyMeeting", "request":
    {"name": "DailyMeeting", "metadata": "<redacted (0 bytes)>", "egress": {"tracks": {"filepath":
    "recordings/{room_name}/{track_source}-{time}"}}}, "duration": "8.808101ms", "status": "200"}
    ```

2. The room is automatically deleted due to a timeout:

    ```{ .log .no-copy }
    2026-01-19T09:04:43.197Z	INFO	openvidu.room	rtc/room.go:854	closing idle room
    {"room": "DailyMeeting", "roomID": "RM_5dHqrCZBr5X5", "reason": "empty timeout"}
    ```

3. A participant connects to the room with a token that does not have autoegress enabled (no `egress` field in its  `RoomConfig`):

    ```log hl_lines="6"
    2026-01-19T09:00:02.925Z	INFO	openvidu	service/roommanager.go:432	starting RTC session
    {"room": "DailyMeeting", "roomID": "RM_u8NSwnuczia6", "participant": "Alice", "pID": "PA_CMwzkoL6Vp3q",
    "remote": false, "nodeID": "ND_QLa7LB7937db", "numParticipants": 1, "participantInit":
    {"Identity": "1589577", "Reconnect": false, "ReconnectReason": "RR_UNKNOWN", "AutoSubscribe": false,
    "Client": {...}, "Grants": {...}, "SIP": {...}, "Agent": {...},
    "RoomConfig": {"metadata": "<redacted (0 bytes)>"}, "RoomPreset": ""},
    "Region": "", "AdaptiveStream": true, "ID": "", "SubscriberAllowPause": "not-set", "DisableICELite": false, "CreateRoom": {"name": "DailyMeeting", "metadata": "<redacted (0 bytes)>"}}
    ```

**Solutions**

- Consider using [on-demand egress requests](#on-demand-vs-automatic-recordings) instead of auto egress to record rooms.
- Consider disabling auto-creation of rooms in file [`livekit.yaml`](../self-hosting/configuration/changing-config.md#config-files). This enforces rooms to always be created explicitly from your backend before a participant can join to it with a token. Of course, it also requires handling connection errors in the frontend if a participant tries to join a non-existing room.

    ```yaml
    room:
      auto_create: false
    ```

- If you want both auto-egress and auto-creation of rooms, make sure to include the same `egress` field in the [`RoomConfiguration` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#roomconfiguration){:target="\_blank"} in both the [`CreateRoom` :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/roomservice-api/#createroom){:target="\_blank"} request and the [participant's access token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/frontends/reference/tokens-grants/#room-configuration){:target="\_blank"}. In this way rooms will always behave the same way, no matter if they are explicitly created from your backend or auto-created when a participant tries to join.
- Increase the room timeout properties in [`livekit.yaml`](../self-hosting/configuration/changing-config.md#config-files). This can reduce the probability of rooms being cleaned up before a participant tries to join:

    ```yaml
    room:
        # number of seconds to keep the room open if no one joins
        empty_timeout: 300
        # number of seconds to keep the room open after everyone leaves
        departure_timeout: 20
    ```

### Misconfiguration of external storage

**Description**

You have configured an external storage for your recordings, but the recording files are not being uploaded to it. This can be caused by a misconfiguration or a connectivity issue between OpenVidu nodes and the external storage.

External storage is configured in the [`egress.yaml` configuration file](../self-hosting/configuration/changing-config.md#config-files) globally (with `storage` property):

```yaml
storage:
  s3:
    ...
  azure:
    ...
  gcp:
    ...
  alioss:
    ...
```

You can also configure external storage programmatically on a per-request basis when starting an egress.

**Symptoms**

- You don't see recording files in your external storage, and the backup folder for egress in your OpenVidu node (`/opt/openvidu/data/egress_data/home/egress/backup_storage`) is accumulating files:

    ```text
    root@media-node-1:/opt/openvidu/data/egress_data/home/egress/backup_storage# ls -la
    total 19036
    drwxr-xr-x 2 admin admin     4096 Mar 10 14:16 .
    drwxr-xr-x 8 admin admin     4096 Mar 10 10:47 ..
    -rw-r--r-- 1 admin root       335 Mar 10 14:11 EG_53MKZu5havzx.json
    -rw-r--r-- 1 admin root       335 Mar 10 14:09 EG_ZgeLTs8FdtzU.json
    -rw-r--r-- 1 admin root       448 Mar 10 14:16 EG_fnvyJkL8YVyt.json
    -rw-r--r-- 1 admin root  14721461 Mar 10 14:09 RoomComposite-RM_Mi5Lau9HWGQ8-TestRoom-2026-03-10T140854.mp4
    -rw-r--r-- 1 admin root   1772593 Mar 10 14:11 RoomComposite-RM_Mi5Lau9HWGQ8-TestRoom2-2026-03-10T141055.mp4
    -rw-r--r-- 1 admin root   2969013 Mar 10 14:16 TrackComposite-RM_JpcnziWBTEdY-TestRoom3-2026-03-10T141625.mp4
    ```

- The [EgressInfo :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/other/egress/api/#egressinfo){:target="\_blank"} objects returned by the Egress API or included in the `egress_ended` webhook event contains:
    - Field `backup_storage_used` with value `true`.
    - Or any other field with the substring `backup_storage` in its value (E.g. `manifestLocation = '/home/egress/backup_storage/EG_f5nHLam4xLb8.json'`{ .no-break }).

**Solutions**

- Review the configuration of the external storage: in the [`egress.yaml`](../self-hosting/configuration/changing-config.md#config-files) if you are using the global declarative configuration, or in the body of the `CreateRoom` or `StartEgress` operations if you are using the programmatic per-request configuration.
- Review the connectivity between your OpenVidu nodes and the external storage. Check if there are any network issues or firewall rules preventing OpenVidu nodes from reaching the external storage.

### No disk space free

**Description**

There is not enough free disk space in the node hosting the egress to start a new recording.

**Symptoms**

- The operation to start a new egress returns a `503 Service Unavailable` error (text of the error: `no response from servers`). This applies when [starting egress on-demand](#on-demand-vs-automatic-recordings) from your application.
- The egress service logs a warning message `can not accept request` followed by a JSON object containing `"error": "not enough disk space"`:

    ```
    {"nodeID": "NE_xRcu2tzJD5mC", "clusterID": "", "total": 16, "available": 12.022278481012659, "pending": 0, "used": 0, "activeRequests": 0, "activeWeb": 0, "memory": 0.06648635864257812, "memorySource": "proc_rss", "availableDiskMB": 30704.07421875, "minDiskSpaceMB": 99999999, "canAccept": false, "reason": "disk", "error": "not enough disk space"}
    ```

- Webhook event `egress_ended` with status `EGRESS_FAILED` and error `mkdir /home/egress/tmp/EGH_XXXXXXXXXXXX: no space left on device`

    ```
    {"event": "egress_ended", "id": "EV_zxMEf5XPp5yV", "webhookTime": 1771329474, "url": "http://127.0.0.1:6080/livekit/webhook", "egressID": "", "status": "EGRESS_FAILED", "error": "mkdir /home/egress/tmp/EGH_XXXXXXXXXXXX: no space left on device", "queueDuration": "7.815288ms", "qLen": 0, "sendDuration": "8.05349ms"}
    ```

**Solutions**

Increase disk space in the node hosting the egress.

### Egress CPU overload killer

**Description**

By default, OpenVidu will kill active egresses under sustained high CPU load (see [Egress CPU overload killer](../self-hosting/production-ready/scalability.md#egress-cpu-overload-killer)). This is generally expected and desired, but it can impact active egresses, causing them to be interrupted.

**Symptoms**
  
- The recordings are incomplete. They appear to be cut off unexpectedly.
- Log lines of level `WARN` displaying `killing egress due to sustained high cpu` in service "egress".

**Solutions**

- You can disable the Egress CPU overload killer by setting property `openvidu.disable_cpu_overload_killer` to `true` in the [**`egress.yaml`** configuration file](../self-hosting/configuration/changing-config.md#config-files). This must be done with caution and care, as it could lead to overloading the entire Media Node and affecting the performance of other processes.
- In the end this is just an under-provisioning issue: consider scaling out your OpenVidu deployment. Deploy it in nodes with more CPU cores or add more Media Nodes to your cluster.
