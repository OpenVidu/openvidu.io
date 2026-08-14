# OpenVidu Elastic installation: On-premises

On-premises

Info

OpenVidu Elastic is part of **OpenVidu PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account/) to get your license key. There's a 15-day free trial waiting for you!

This section contains instructions for deploying a production-ready OpenVidu Elastic deployment on-premises. The deployment requires one Master Node and any number of Media Nodes. Media Nodes are elastic and can be scaled up and down according to workload.

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu Elastic On Premises

- The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
- The Master Node has its own Caddy server acting as a Layer 4 (for TURN with TLS and RTMPS) and Layer 7 (for OpenVidu Dashboard, OpenVidu Meet, etc., APIs) reverse proxy.
- WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.

For the Master Node, the following services are configured:

- **OpenVidu Dashboard**, a web application interface to visualize your Rooms, Ingress, and Egress services.
- **MinIO** as an S3 storage service for recordings.
- **Redis** as a shared database for OpenVidu Server PRO and Ingress/Egress services.
- **MongoDB** as a database for storing analytics and monitoring data.
- **Caddy** as a reverse proxy. It can be deployed with self-signed certificates, Let's Encrypt certificates, or custom certificates. Provides optional TLS for the TURN server.
- **[OpenVidu Meet](https://openvidu.io/3.8/meet/index.md)**, an optional high-quality video calling service.
- **OpenVidu V2 Compatibility (v2compatibility module)** is an optional service that provides an API designed to maintain compatibility for applications developed with OpenVidu version 2.
- **Grafana, Mimir, Promtail, and Loki (Observability module)** form an optional observability stack for monitoring, allowing you to keep track of logs and deployment statistics for OpenVidu.

For the Media Nodes, the following services are configured:

- **OpenVidu Server PRO (LiveKit compatible).**
- **Ingress** and **Egress** services.
- **Prometheus and Loki (Observability module)**. Used to send metrics and logs to the observability stack.

## Prerequisites

- **At least 2 machines**, each with a minimum of **4GB RAM**, **4 CPU cores**, and **Linux** installed (Ubuntu is recommended). One machine will serve as the Master Node, while the others will function as Media Nodes.

- Significant disk space on the **Master Node, with 100GB recommended**, especially if you plan to record your sessions (Egress). Media Nodes require less space; however, account for the space needed for ongoing recordings on these nodes.

- **Each machine must be assigned a Public IP**. An FQDN (Fully Qualified Domain Name) is optional for the Master Node. If not provided, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it.

- **All machines must have access to the following addresses and ports**:

  | Host                     | Port    |
  | ------------------------ | ------- |
  | `accounts.openvidu.io`   | `443`   |
  | `global.stun.twilio.com` | `3478`  |
  | `stun.l.google.com`      | `19302` |
  | `stun1.l.google.com`     | `19302` |

  Info

  If you are behind a very restrictive corporate firewall that doesn't allow outgoing traffic to those addresses, please contact us through [commercial@openvidu.io](mailto:commercial@openvidu.io).

## Port rules (Master Node)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Master Node.

**Inbound port rules**:

| Protocol | Ports | Source          | Description                                                                                                                                                                                         |
| -------- | ----- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TCP      | 80    | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation.                                                                                                                                        |
| TCP      | 443   | 0.0.0.0/0, ::/0 | Allows access to the following: - Livekit API. - OpenVidu v2 Compatibility API - OpenVidu Dashboard. - OpenVidu Meet. - WHIP API. - TURN with TLS. - Custom layouts                                 |
| TCP      | 1935  | 0.0.0.0/0, ::/0 | Needed if you want to ingest RTMP streams using Ingress service.                                                                                                                                    |
| TCP      | 9000  | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly.                                                                                                                                                        |
| TCP      | 4443  | Media Nodes     | Needed when *'OpenVidu v2 Compatibility'* module is used (`v2compatibility` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu V2 compatibility service |
| TCP      | 9080  | Media Nodes     | Needed when *'OpenVidu Meet'* module is used (`openviduMeet` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu Meet.                                   |
| TCP      | 3100  | Media Nodes     | Needed when *'Observability'* module is used (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Loki.                                            |
| TCP      | 7880  | Media Nodes     | Media Nodes need access to this port for Ingress, Egress and Agents to reach load balanced LiveKit API.                                                                                             |
| TCP      | 9009  | Media Nodes     | Needed when *'Observability'* module is used. (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Mimir.                                          |
| TCP      | 7000  | Media Nodes     | Media Nodes need access to this port to reach Redis Service.                                                                                                                                        |
| TCP      | 9100  | Media Nodes     | Media Nodes need access to this port to reach MinIO.                                                                                                                                                |
| TCP      | 20000 | Media Nodes     | Media Nodes need access to this port to reach MongoDB.                                                                                                                                              |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Port rules (Media Nodes)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Media Nodes:

**Inbound port rules**:

| Protocol | Ports       | Source          | Description                                                                                                                                                           |
| -------- | ----------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UDP      | 443         | 0.0.0.0/0, ::/0 | STUN/TURN over UDP.                                                                                                                                                   |
| TCP      | 7881        | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Pion.                                                                                                                   |
| UDP      | 7885        | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP.                                                                                                                       |
| UDP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over UDP.                                                                                                                             |
| TCP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Mediasoup.                                                                                                              |
| TCP      | 1935        | Master Node     | Needed if you want to ingest RTMP streams using Ingress service. Master Node needs access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
| TCP      | 5349        | Master Node     | Needed if you have configured TURN with a domain for TLS. Master Node needs access to this port to reach TURN service and expose it using TLS (TURNS).                |
| TCP      | 7880        | Master Node     | LiveKit API. Master Node needs access to load balance LiveKit API and expose it through HTTPS.                                                                        |
| TCP      | 8080        | Master Node     | Needed if you want to ingest WebRTC streams using WHIP. Master Node needs access to this port to reach WHIP HTTP service.                                             |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Guided installation

Before the installation, ensure that all your machines meet the [prerequisites](#prerequisites) and the port rules for the [Master Node](#port-rules-master-node) and [Media Nodes](#port-rules-media-nodes) are correctly configured.

To install OpenVidu Elastic, **begin by generating the commands required for setting up all nodes in the cluster**. This is a simple and straightforward process; simply **run the following command on any machine that has Docker installed**:

```bash
docker run --pull always --rm -it \
    openvidu/openvidu-installer:latest \
    --deployment-type=elastic
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

A wizard will guide you through the installation process. You will be asked for the following information:

- **Write the 'Master Node' Private IP**: Write the private IP of the machine where you are going to install the Master Node.
- **Write your OpenVidu PRO License**: Write your OpenVidu PRO License.

Info

If you don't have a license key for OpenVidu PRO, you can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).

- **Domain name** (Optional): The domain name for your deployment. If left empty, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it. For production environments, it's recommended to provide your own FQDN.

- **Select which certificate type to use**:

  - *Self Signed Certificate*: It will generate a self-signed certificate. It is not recommended for production environments, but it is useful for testing or development purposes.
  - *Let's Encrypt*: It will automatically generate a certificate for your domain. The Let's Encrypt email is required and will be asked later in the wizard.
  - *ZeroSSL*: It will automatically generate a certificate for your domain using ZeroSSL. An API Key is required and will be asked later in the wizard.
  - *Own Certificate*: It will ask you for the certificate and key files. Just copy and paste the content of the files when the wizard asks for them.

  Note

  If you want to manage the certificate in your own proxy server instead of relying in the Caddy server deployed with OpenVidu, take a look to this How-to guide: [How to deploy OpenVidu with an external proxy](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/deploy-with-external-proxy/index.md).

- **Select which RTC engine to use**: Select the WebRTC engine you want to use. You can choose between **Pion (the default engine used by LiveKit)** and **Mediasoup (with a boost in performance)**. Learn more about the differences [here](https://openvidu.io/3.8/docs/self-hosting/production-ready/performance/index.md).

- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:

  - [*OpenVidu Meet*](https://openvidu.io/3.8/meet/index.md): A high-quality video calling service based on OpenVidu.
  - *Observability*: Grafana stack, which includes logs and monitoring stats.
  - *OpenVidu V2 Compatibility*: Compatibility API for applications developed with OpenVidu v2.

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

This command will output the following instructions, which you should follow:

1. **Firewall Configuration for 'Master Node'**: These rules are the same as those specified in the instructions. Depending on the modules you have selected, some rules defined at [Port rules (Master Node)](#port-rules-master-node) may not appear (Optional ports). Double-check and modify it if you see something that can be enabled/disabled in your current port rules.

1. **Installation Commands for 'Master Node'**: This is the command needed to install your Master Node. It should look like this:

   ```bash
   sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
       --no-tty --install \
       --deployment-type='elastic' \
       --node-role='master-node' \
   ...
   ```

   Note

   In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

   Execute that command in your Master Node to install it. When the installation process finishes, you will see the following output:

   ```text
   > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
   >                                                                             <
   >  🎉 OpenVidu Elastic 'Master Node' Installation Finished Successfully! 🎉   <
   >                                                                             <
   > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
   ```

   The Master Node will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

   ```bash
   systemctl start openvidu
   ```

1. **Firewall Configuration for 'Media Nodes'**: These rules are the same as those defined previously as with the Master Node. Double-check the [Port rules (Media Nodes)](#port-rules-media-nodes) and modify them if you see something that can be enabled/disabled in your current port rules.

1. **Installation Commands for 'Media Nodes'**: This is the command needed to install your Media Nodes. It should look like this:

   ```bash
   sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
       --no-tty --install \
       --deployment-type='elastic' \
       --node-role='media-node' \
   ...
   ```

   Note

   In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

   Execute that command on your Media Nodes to install them. When the installation process finishes, you will see the following output:

   ```text
   > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
   >                                                                             <
   >  🎉 OpenVidu Elastic 'Media Node' Installation Finished Successfully! 🎉    <
   >                                                                             <
   > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
   ```

   The Media Node on each machine will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

   ```text
   systemctl start openvidu
   ```

If everything goes well, all containers will be up and running without restarts, and you will be able to access any of the following services:

- OpenVidu Meet: <https://openvidu.example.io/>
- OpenVidu Dashboard: [https://openvidu.example.io/dashboard](https://openvidu.example.io/dashboard/)
- MinIO: [https://openvidu.example.io/minio-console](https://openvidu.example.io/minio-console/)
- Grafana: [https://openvidu.example.io/grafana](https://openvidu.example.io/grafana/)

OpenVidu Server PRO URL (LiveKit compatible) will be available also in:

- OpenVidu Server PRO: <https://openvidu.example.io/>
- LiveKit API: <https://openvidu.example.io/> and <wss://openvidu.example.io/>

## Configure your application to use the deployment

To point your applications to your OpenVidu deployment, check the following files:

- `/opt/openvidu/config/cluster/master_node/meet.env`: Contains the OpenVidu Meet parameters.
- `/opt/openvidu/config/cluster/openvidu.env`: Contains all the credentials of services deployed with OpenVidu Platform.

The most relevant parameters are:

**OpenVidu Meet**:

- **`MEET_INITIAL_ADMIN_USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

Note

The `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` values are initial and cannot be changed from the `meet.env` file. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: API Secret for LiveKit SDKs.

**OpenVidu V2 Compatibility Credentials**

This section is only needed if you want to use OpenVidu v2 compatibility.

- **URL**: The URL to access OpenVidu, which is formed by the `DOMAIN_NAME` as `https://yourdomain.example.io/`
- **Username**: Basic auth user for OpenVidu v2 compatibility. It is always `OPENVIDUAPP`.
- **Password**: Basic auth password for OpenVidu v2 compatibility is the same as `LIVEKIT_API_SECRET`.

## Non-interactive installation

To automate the installation process, run the command specified in the [Guided installation](#guided-installation) section, and then run the generated commands.

Each installation command for each type of node looks like this:

**Master Node**

**Without Domain Name**

The Master Node can be configured with multiple kinds of certificates. Here are the examples for each type of certificate that is allowed when no FQDN is provided:

**Let's Encrypt certificates**

Example using Let's Encrypt certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
    --rtc-engine='pion' \
    --livekit-api-key='xxxxx' \
    --livekit-api-secret='xxxxx' \
    --dashboard-admin-user='xxxxx' \
    --dashboard-admin-password='xxxxx' \
    --redis-password='xxxxx' \
    --minio-access-key='xxxxx' \
    --minio-secret-key='xxxxx' \
    --mongo-admin-user='xxxxx' \
    --mongo-admin-password='xxxxx' \
    --mongo-replica-set-key='xxxxx' \
    --grafana-admin-user='xxxxx' \
    --grafana-admin-password='xxxxx' \
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='1.2.3.4' \
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

**Self-signed certificates**

Example using self-signed certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
    --rtc-engine='pion' \
    --livekit-api-key='xxxxx' \
    --livekit-api-secret='xxxxx' \
    --dashboard-admin-user='xxxxx' \
    --dashboard-admin-password='xxxxx' \
    --redis-password='xxxxx' \
    --minio-access-key='xxxxx' \
    --minio-secret-key='xxxxx' \
    --mongo-admin-user='xxxxx' \
    --mongo-admin-password='xxxxx' \
    --mongo-replica-set-key='xxxxx' \
    --grafana-admin-user='xxxxx' \
    --grafana-admin-password='xxxxx' \
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='1.2.3.4' \
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

**With Domain Name**

The Master Node can be configured with multiple kinds of certificates. Here are the examples for each type of certificate:

**Let's Encrypt certificates**

Example using Let's Encrypt certificates:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
    --rtc-engine='pion' \
    --livekit-api-key='xxxxx' \
    --livekit-api-secret='xxxxx' \
    --dashboard-admin-user='xxxxx' \
    --dashboard-admin-password='xxxxx' \
    --redis-password='xxxxx' \
    --minio-access-key='xxxxx' \
    --minio-secret-key='xxxxx' \
    --mongo-admin-user='xxxxx' \
    --mongo-admin-password='xxxxx' \
    --mongo-replica-set-key='xxxxx' \
    --grafana-admin-user='xxxxx' \
    --grafana-admin-password='xxxxx' \
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='1.2.3.4' \
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

Notes:

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

**Self-signed certificates**

Example using self-signed certificates:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
    --rtc-engine='pion' \
    --livekit-api-key='xxxxx' \
    --livekit-api-secret='xxxxx' \
    --dashboard-admin-user='xxxxx' \
    --dashboard-admin-password='xxxxx' \
    --redis-password='xxxxx' \
    --minio-access-key='xxxxx' \
    --minio-secret-key='xxxxx' \
    --mongo-admin-user='xxxxx' \
    --mongo-admin-password='xxxxx' \
    --mongo-replica-set-key='xxxxx' \
    --grafana-admin-user='xxxxx' \
    --grafana-admin-password='xxxxx' \
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='1.2.3.4' \
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

**Custom certificates**

Example using custom certificates:

```bash
CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
    --rtc-engine='pion' \
    --livekit-api-key='xxxxx' \
    --livekit-api-secret='xxxxx' \
    --dashboard-admin-user='xxxxx' \
    --dashboard-admin-password='xxxxx' \
    --redis-password='xxxxx' \
    --minio-access-key='xxxxx' \
    --minio-secret-key='xxxxx' \
    --mongo-admin-user='xxxxx' \
    --mongo-admin-password='xxxxx' \
    --mongo-replica-set-key='xxxxx' \
    --grafana-admin-user='xxxxx' \
    --grafana-admin-password='xxxxx' \
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='1.2.3.4' \
    --certificate-type='owncert' \
    --owncert-private-key="$CERT_PRIVATE_KEY" \
    --owncert-public-key="$CERT_PUBLIC_KEY"
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- Note that you only need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.
- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/).
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

**Media Node**

To install a Media Node, you can use the following command:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
    --no-tty --install \
    --node-role='media-node' \
    --master-node-private-ip='1.2.3.4' \
    --redis-password='xxxxx'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- The `--master-node-private-ip` is the private IP of the Master Node. Media Nodes should be able to reach the Master Node using this IP.
- The `--redis-password` is the password defined in the Master Node installation. It is used to connect to the Redis service in the Master Node and register itself as a Media Node in the cluster.
- If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media. If you decide to install the Media Node with `--public-ip`, you must reinstall the Master Node with `--force-media-node-public-ip`.

You can run these commands in a CI/CD pipeline or in a script to automate the installation process.

Some notes about the Master Node installation command:

- The argument `--domain-name` is optional. If not provided, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it.
- When using autogenerated domains (no FQDN (Fully Qualified Domain Name) provided), only `selfsigned` and `letsencrypt` certificate types are available.
- At the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `openviduMeet` [OpenVidu Meet service](https://openvidu.io/3.8/meet/index.md), `observability` (Grafana stack) and `v2compatibility` (OpenVidu v2 compatibility API).

To start each node, remember to execute the following command in each node:

```bash
systemctl start openvidu
```

## Configuration and administration

Once you have OpenVidu deployed, you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/admin/index.md) section to learn how to manage your OpenVidu Elastic deployment.
