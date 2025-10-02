---
title: Configuration reference
description: Reference for the configuration files used in all different OpenVidu deployments.
---

# Configuration reference

## `openvidu.env`:

This file defines global configuration parameters used by other services. Such as the domain name, credentials, etc.

| <div style="width: 17em;">Parameter</div> | Description |
| --------- | ----------- |
| **`DOMAIN_NAME`** | The domain name for the deployment. Use this domain name to access. OpenVidu APIs and services. |
| **`LIVEKIT_API_KEY`** | Global LiveKit API Key and Secret used for apps to connect to OpenVidu. |
| **`LIVEKIT_API_SECRET`** | Global LiveKit API Key and Secret used for apps to connect to OpenVidu. |
| **`MINIO_ACCESS_KEY`** | Access key for MinIO. |
| **`MINIO_SECRET_KEY`** | Secret key for MinIO. |
| **`EXTERNAL_S3_ENDPOINT`** | If defined, Minio will not be used and the deployment will use an external S3 service. This is the endpoint of the external S3 service. |
| **`EXTERNAL_S3_ACCESS_KEY`** | Access key for the external S3 service if used. |
| **`EXTERNAL_S3_SECRET_KEY`** | Secret key for the external S3 service if used. |
| **`EXTERNAL_S3_REGION`** | Region of the external S3 service if used. |
| **`EXTERNAL_S3_PATH_STYLE_ACCESS`** | If `true`, use path-style access for the external S3 service if used. |
| **`EXTERNAL_S3_BUCKET_APP_DATA`** | External S3 bucket name for OpenVidu App Data. This is the bucket where application data like recordings, etc. will be stored. |
| **`EXTERNAL_S3_BUCKET_CLUSTER_DATA`** | External S3 bucket used in High Availability to store Observability data. |
| **`MONGO_ADMIN_USERNAME`** | MongoDB admin username. |
| **`MONGO_ADMIN_PASSWORD`** | MongoDB admin password. |
| **`DASHBOARD_ADMIN_USERNAME`** | Admin username for OpenVidu Dashboard |
| **`DASHBOARD_ADMIN_PASSWORD`** | Admin password for OpenVidu Dashboard |
| **`GRAFANA_ADMIN_USERNAME`** | Admin username for Grafana |
| **`GRAFANA_ADMIN_PASSWORD`** | Admin password for Grafana |
| **`OPENVIDU_PRO_LICENSE`** | <span class="openvidu-tag openvidu-pro-tag">PRO</span> OpenVidu Pro license key. Get an OpenVidu Pro License [here](/account/){:target="_blank"}. |
| **`OPENVIDU_RTC_ENGINE`** | <span class="openvidu-tag openvidu-pro-tag">PRO</span> The WebRTC engine to use. Can be `pion` or `mediasoup`. |

## `meet.env`:

This file defines the configuration parameters for the OpenVidu Meet service.

| Parameter | Description |
| --------- | ----------- |
| **`SERVER_PORT`** | Port where the OpenVidu Meet service will be running. |
| **`SERVER_CORS_ORIGIN`** | CORS origin for the OpenVidu Meet service. It is `*` by default, allowing all origins. |
| **`LIVEKIT_URL`** | LiveKit URL for the OpenVidu Meet service to connect to the LiveKit server. |
| **`LIVEKIT_URL_PRIVATE`** | LiveKit URL for the OpenVidu Meet service to connect to the LiveKit server internally. This is used in High Availability deployments. |
| **`LIVEKIT_API_KEY`** | LiveKit API Key for the OpenVidu Meet service to connect to the LiveKit server. |
| **`LIVEKIT_API_SECRET`** | LiveKit API Secret for the OpenVidu Meet service to connect to the LiveKit server. |
| **`MEET_INITIAL_ADMIN_USER`** | Username for the Admin user of the OpenVidu Meet service. |
| **`MEET_INITIAL_ADMIN_PASSWORD`** | Password for the Admin user of the OpenVidu Meet service. |
| **`MEET_INITIAL_API_KEY`** | API Key for the OpenVidu Meet service. This is used by applications developed with OpenVidu Meet. |
| **`MEET_WEBHOOK_ENABLED`** | If `true`, the OpenVidu Meet service will send webhooks to the configured webhook endpoint. |
| **`MEET_WEBHOOK_URL`** | Webhook URL for the OpenVidu Meet service. This is the URL where the webhooks will be sent. |
| **`MEET_PREFERENCES_STORAGE_MODE`** | Storage mode for user preferences in OpenVidu Meet. Valid values are: `s3` (S3 bucket) and `abs` (Azure Blob Storage). |
| **`MEET_S3_BUCKET`** | S3 bucket name for OpenVidu Meet service. It is used to store recordings. |
| **`MEET_S3_SUBBUCKET`** | Path for the S3 bucket where OpenVidu Meet service will store recordings and user preferences. |
| **`MEET_S3_SERVICE_ENDPOINT`{.no-break}** | S3 service endpoint for OpenVidu Meet service. |
| **`MEET_S3_ACCESS_KEY`** | S3 access key for OpenVidu Meet service. |
| **`MEET_S3_SECRET_KEY`** | S3 secret key for OpenVidu Meet service. |
| **`MEET_AWS_REGION`** | AWS region of the S3 Bucket application. |
| **`MEET_S3_WITH_PATH_STYLE_ACCESS`{.no-break}** | If `true`, use path-style access for S3. |
| **`MEET_AZURE_CONTAINER_NAME`** | Azure Blob Storage container name for OpenVidu Meet service. It is used to store recordings. |
| **`MEET_AZURE_SUBCONATAINER_NAME`** | Path for the Azure Blob Storage container where OpenVidu Meet service will store recordings and user preferences. |
| **`MEET_AZURE_ACCOUNT_NAME`** | Azure Blob Storage account name for OpenVidu Meet service. |
| **`MEET_AZURE_ACCOUNT_KEY`** | Azure Blob Storage account key for OpenVidu Meet service. |
| **`MEET_REDIS_HOST`** | Redis host used by the OpenVidu Meet service to store session data. |
| **`MEET_REDIS_PORT`** | Redis port used by the OpenVidu Meet service to connect to the Redis server. |
| **`MEET_REDIS_USERNAME`** | Redis username used by the OpenVidu Meet service to connect to the Redis server. |
| **`MEET_REDIS_PASSWORD`** | Redis password used by the OpenVidu Meet service to connect to the Redis server. |
| **`MEET_REDIS_DB`** | Redis database used by the OpenVidu Meet service. Default value is `0`. |
| **`MEET_REDIS_SENTINEL_HOST_LIST`** | Redis Sentinel host list used by the OpenVidu Meet service to connect to Redis Sentinel servers. |
| **`MEET_REDIS_SENTINEL_PASSWORD`** | Redis Sentinel password used by the OpenVidu Meet service to connect to Redis Sentinel servers. |
| **`MEET_REDIS_SENTINEL_MASTER_NAME`{.no-break}** | Redis Sentinel master name used by the OpenVidu Meet service to connect to Redis Sentinel servers. |
| **`MEET_LOG_LEVEL`** | Log level for OpenVidu Meet service. Valid values are: `error`, `warn`, `info`, `verbose`, `debug`, `silly`. |

## <span class="openvidu-tag openvidu-pro-tag">PRO</span> `v2compatibility.env`

!!! info
    
    OpenVidu V2 Compatibility is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px; vertical-align: top;">PRO</span>**. Before deploying, you need to [create an OpenVidu account](/account/){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

This file defines the configuration parameters for the OpenVidu V2 Compatibility Server. They resemble the configuration parameters of [**OpenVidu 2** :fontawesome-solid-external-link:{.external-link-icon}](https://docs.openvidu.io/en/latest/reference-docs/openvidu-config/){:target=_blank}, adding prefix `V2COMPAT_` to the parameter name.

| Parameter | Description |
| --------- | ----------- |
| **`OPENVIDU_PRO_LICENSE`** |  OpenVidu Pro license key. Get an OpenVidu Pro License [here](/account/){:target="_blank"}. |
| **`V2COMPAT_OPENVIDU_SHIM_PORT`** | Port where the OpenVidu V2 Compatibility will be running. By default is `4443` |
| **`V2COMPAT_OPENVIDU_SHIM_URL`** | Public URL used for openvidu v2 applications used by external clients to connect to the OpenVidu V2 Compatibility Server. |
| **`V2COMPAT_OPENVIDU_SECRET`** | OpenVidu Secret used by openvidu v2 applications to connect to the OpenVidu deployment. |
| **`V2COMPAT_LIVEKIT_URL`** | LiveKit URL used by external clients to connect to the OpenVidu V2 Compatibility Server using the LiveKit protocol. |
| **`V2COMPAT_LIVEKIT_URL_PRIVATE`** | LiveKit URL used by the OpenVidu V2 Compatibility Server to connect to the LiveKit Server internally. |
| **`V2COMPAT_LIVEKIT_API_KEY`** | LiveKit API Key used by the OpenVidu V2 Compatibility Server to interact with the LiveKit Server. |
| **`V2COMPAT_LIVEKIT_API_SECRET`** | LiveKit API Secret used by the OpenVidu V2 Compatibility Server to interact with the LiveKit Server. |
| **`V2COMPAT_REDIS_HOST`** | Redis host used by the OpenVidu V2 Compatibility Server to store session data. |
| **`V2COMPAT_REDIS_PORT`** | Redis port used by the OpenVidu V2 Compatibility Server to connect to the Redis server. |
| **`V2COMPAT_REDIS_PASSWORD`** | Redis password used by the OpenVidu V2 Compatibility Server to connect to the Redis server. |
| **`V2COMPAT_REDIS_SENTINEL_HOST_LIST`** | Redis Sentinel host list used by the OpenVidu V2 Compatibility Server to connect to Redis Sentinel servers. |
| **`V2COMPAT_REDIS_SENTINEL_PASSWORD`** | Redis Sentinel password used by the OpenVidu V2 Compatibility Server to connect to Redis Sentinel servers. |
| **`V2COMPAT_REDIS_MASTER_NAME`** | Redis Sentinel master name used by the OpenVidu V2 Compatibility Server to connect to Redis Sentinel servers. |
| **`V2COMPAT_REDIS_DB`** | Redis database used by the OpenVidu V2 Compatibility Server. Default value is `0`. |
| **`V2COMPAT_OPENVIDU_RECORDING_PATH`** | Path where the OpenVidu V2 Compatibility Server will store recordings locally. By default in the deployments is `/opt/openvidu/recordings`. |
| **`V2COMPAT_OPENVIDU_PRO_RECORDING_STORAGE`{.no-break}** | Where to store the recordings. Valid values are: <ul><li>`local`: Store the recordings in the local filesystem at the path `V2COMPAT_OPENVIDU_RECORDING_PATH`</li><li>`s3`: Store the recordings in the configured S3 bucket</li></ul> Default value is `local` |
| **`V2COMPAT_OPENVIDU_RECORDING_CUSTOM_LAYOUT_URL`** | URL of the custom layout used by the OpenVidu V2 Compatibility Server to generate the recordings. |
| **`V2COMPAT_OPENVIDU_PRO_AWS_S3_WITH_PATH_STYLE_ACCESS`{.no-break}** | If `true`, use path-style access for S3. |
| **`V2COMPAT_OPENVIDU_RECORDING_ZIP_FILES`** | If `true`, save individual recordings as zip files |
| **`V2COMPAT_OPENVIDU_RECORDING_RAW_FILES`** | If `true`, save individual recordings as files directly |
| **`V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET`** | Default bucket name for recordings |
| **`V2COMPAT_OPENVIDU_PRO_AWS_S3_SERVICE_ENDPOINT`{.no-break}** | S3 service endpoint for the recordings |
| **`V2COMPAT_OPENVIDU_PRO_AWS_ACCESS_KEY`** | Access key for the recordings S3 bucket |
| **`V2COMPAT_OPENVIDU_PRO_AWS_SECRET_KEY`** | Secret key for the recordings S3 bucket |
| **`V2COMPAT_OPENVIDU_PRO_AWS_REGION`** | AWS region of the recordings S3 bucket |
| **`V2COMPAT_OPENVIDU_WEBHOOK`** | If `true`, the OpenVidu V2 Compatibility Server will send webhooks to `V2COMPAT_OPENVIDU_WEBHOOK_ENDPOINT` |
| **`V2COMPAT_OPENVIDU_WEBHOOK_HEADERS`** | JSON Array list of headers to send in the OpenVidu V2 Webhook events. For example: <br>`["Content-Type: application/json"]` |
| **`V2COMPAT_OPENVIDU_WEBHOOK_EVENTS`** | Comma-separated list of OpenVidu V2 Webhook events to send. All available events are: <ul><li>sessionCreated</li><li>sessionDestroyed</li><li>participantJoined</li><li>participantLeft</li><li>webrtcConnectionCreated</li><li>webrtcConnectionDestroyed</li><li>recordingStatusChanged</li><li>signalSent</li></ul> |

## `livekit.yaml`:

As OpenVidu Server is [built on top of LiveKit](../../comparing-openvidu.md#openvidu-vs-livekit), the configuration of OpenVidu Server is done in the `livekit.yaml` file in its own `openvidu` section in this file. The rest of the configuration is the same as the [LiveKit server configuration :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/blob/master/config-sample.yaml){:target="_blank"}.

### <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span> OpenVidu Server Configuration:

```yaml
openvidu:
    analytics: # (1)
        enabled: true # (2)
        mongo_url: mongodb://<MONGO_ADMIN_USERNAME>:<MONGO_ADMIN_PASSWORD>@localhost:20000/ # (3)
        interval: 10s # (4)
        expiration: 768h # (5)
```

1. The `analytics` configuration should be defined at the `openvidu` level in the `livekit.yaml` file.
2. This must be set to `true` to send analytics data to MongoDB. If set to `false`, no analytics data will be sent.
3. MongoDB connection string. In OpenVidu Single Node, the MongoDB service is running on the same machine, so you can use `localhost` as the hostname. The default port in OpenVidu for MongoDB is `20000`. `MONGO_ADMIN_USERNAME` and `MONGO_ADMIN_PASSWORD` are the credentials to access the MongoDB database.
4. Time interval to send analytics data to MongoDB.
5. Time to keep the analytics data in MongoDB. In this example, it is set to 32 days.

### <span class="openvidu-tag openvidu-pro-tag">PRO</span> OpenVidu Server Configuration:


!!! info
    
    Before deploying OpenVidu PRO, you need to [create an OpenVidu account](/account/){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

```yaml
openvidu:
    license: <YOUR_OPENVIDU_PRO_LICENSE> # (1)
    cluster_id: <YOUR_DOMAIN_NAME> # (2)
    analytics: # (3)
        enabled: true # (4)
        interval: 10s # (5)
        expiration: 768h # (6)
        mongo_url: <MONGO_URL> # (7)
    rtc:
        engine: pion # (8)
    mediasoup:
        debug: "" # (9)
        log_level: error # (10)
        log_tags: [info, ice, rtp, rtcp, message] # (11)
```

1. Specify your OpenVidu Pro license key. If you don't have one, you can request one [here](/account/){:target=_blank}.
2. The cluster ID for the OpenVidu deployment. It is configured by default by OpenVidu Installer with the domain name of the deployment.
3. The `analytics` configuration should be defined at the `openvidu` level in the `livekit.yaml` file.
4. This must be set to `true` to send analytics data to MongoDB. If set to `false`, no analytics data will be sent.
5. Time interval to send analytics data to MongoDB.
6. Time to keep the analytics data in MongoDB. In this example, it is set to 32 days.
7. MongoDB URL. This is the connection string to the MongoDB database where the analytics data will be stored.
8. The `rtc.engine` parameter is set to `pion` by default. This is the WebRTC engine used by OpenVidu. Depending on your requirements, you can use:
    - `pion`
    - `mediasoup`
9. Global toggle to enable debugging logs from Mediasoup. In most debugging cases, using just an asterisk ("*") here is enough, but this can be fine-tuned for specific log levels. [More info :fontawesome-solid-external-link:{.external-link-icon}](https://mediasoup.org/documentation/v3/mediasoup/debugging/){:target=_blank}.
    - Default is an empty string.
10. Logging level for logs generated by Mediasoup. [More info :fontawesome-solid-external-link:{.external-link-icon}](https://mediasoup.org/documentation/v3/mediasoup/debugging/){:target=_blank}.
    - Valid values are: `debug`, `warn`, `error`, `none`.
    - Default is `error`.
11. Comma-separated list of log tag names, for debugging. [More info :fontawesome-solid-external-link:{.external-link-icon}](https://mediasoup.org/documentation/v3/mediasoup/debugging/){:target=_blank}.
    - Valid values are: `info`, `ice`, `dtls`, `rtp`, `srtp`, `rtcp`, `rtx`, `bwe`, `score`, `simulcast`, `svc`, `sctp`, `message`.
    - Default is `[info, ice, rtp, rtcp, message]`.

## Other Services Configuration

OpenVidu comes with other services configured to work in the deployment. These are the configuration files for each service:

| Service             | Description | Reference documentation |
| ------------------- | ----------- | ------------------ |
| **OpenVidu Server**     | Manage Rooms and Media Streams. | <ul><li>[OpenVidu Config](#livekityaml)</li><li>[LiveKit Config :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/livekit/blob/v1.7.2/config-sample.yaml){:target=_blank}</li></ul>
| **Ingress Service**     | Imports video from other sources into OpenVidu rooms. | [LiveKit Ingress Config :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/ingress/blob/v1.4.2/README.md#config){:target=_blank} |
| **Egress Service**      | Exports video from OpenVidu rooms for recording or streaming. | [LiveKit Egress Config :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/egress/blob/v1.8.4/README.md#config){:target=_blank} |
| **Caddy Server** | Serves OpenVidu services and handles HTTPS. | [Caddy JSON Structure :fontawesome-solid-external-link:{.external-link-icon}](https://caddyserver.com/docs/json/){:target=_blank} |
| **Grafana Service**     | Used for visualizing monitoring data. | [Grafana Config :fontawesome-solid-external-link:{.external-link-icon}](https://grafana.com/docs/grafana/latest/administration/configuration/){:target=_blank} |
| **Mimir Service** | Service for long-term prometheus storage | [Mimir Config :fontawesome-solid-external-link:{.external-link-icon}](https://grafana.com/docs/mimir/v2.11.x/configure/about-configurations/){:target=_blank} |
| **Loki Service**        | Used for log aggregation. | [Loki Config :fontawesome-solid-external-link:{.external-link-icon}](https://grafana.com/docs/loki/v2.8.x/configuration/){:target=_blank} |
| **Prometheus Service**  | Used for monitoring. | [Prometheus Config :fontawesome-solid-external-link:{.external-link-icon}](https://prometheus.io/docs/prometheus/latest/configuration/configuration/){:target=_blank} |
| **Promtail Service**    | Collects logs and sends them to Loki. | [Promtail Config :fontawesome-solid-external-link:{.external-link-icon}](https://grafana.com/docs/loki/v2.8.x/clients/promtail/configuration/){:target=_blank} |
