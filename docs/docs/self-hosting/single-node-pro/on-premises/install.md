---
title: OpenVidu Single Node PRO installation on-premises
description: Learn how to deploy OpenVidu Single Node PRO on-premises
---

# OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: .6em; vertical-align: text-bottom">PRO</span> installation: On-premises

This section contains the instructions to deploy a production-ready OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px">PRO</span> deployment on-premises. It is a deployment based on Docker and Docker Compose, which will automatically configure all the necessary services for OpenVidu to work properly.

=== "Architecture overview"

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Single Node On Premises Architecture](../../../../assets/images/self-hosting/single-node/on-premises/single-node-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Single Node On Premises Architecture</figcaption>
    </figure>

All services are deployed on a single machine, which includes:

- **OpenVidu Server (LiveKit compatible)**.
- **Ingress** and **Egress** services.
- **OpenVidu Dashboard**, a web application interface to visualize your Rooms, Ingress, and Egress services.
- **MinIO** as an S3 storage service for recordings.
- **Redis** as a shared database for OpenVidu Server and Ingress/Egress services.
- **MongoDB** as a database for storing analytics and monitoring data.
- **Caddy** as a reverse proxy. It can be deployed with self-signed certificates, Let's Encrypt certificates, or custom certificates.
- **[OpenVidu Meet](../../../../meet/index.md)**, an optional high-quality video calling service.
- **OpenVidu V2 Compatibility (v2compatibility module)** is an optional service that provides an API designed to maintain compatibility for applications developed with OpenVidu version 2.
- **Grafana, Mimir, Promtail, and Loki (Observability module)** form an optional observability stack for monitoring, allowing you to keep track of logs and deployment statistics for OpenVidu.

## Prerequisites

Before starting the installation process, make sure you have the following prerequisites:

- **A machine with at least 4GB RAM and 4 CPU cores** and **Linux installed (Ubuntu recommended)**.
- **Generous disk space (100GB recommended)** if you are going to record your sessions.
- The machine **must have a Public IP** and an FQDN (Fully Qualified Domain Name) pointing to it.

## Port rules

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your machine.

**Inbound port rules**:

| Protocol    | Ports          | <div style="width:8em">Source</div>          | Description                                                |
| ----------- | -------------- | --------------- | ---------------------------------------------------------- |
| TCP         | 80             | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
| TCP         | 443            | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu Dashboard.</li><li>OpenVidu Meet.</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
| UDP         | 443            | 0.0.0.0/0, ::/0 | STUN/TURN server over UDP. |
| TCP         | 1935           | 0.0.0.0/0, ::/0 | Needed if you want to ingest RTMP streams using Ingress service. |
| TCP         | 9000           | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly. |
| TCP         | 7881           | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Pion. |
| UDP         | 7885           | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP. |
| UDP         | 50000-60000    | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over UDP. |
| TCP         | 50000-60000    | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Mediasoup. |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Guided Installation

Before the installation, ensure that your machine meets the [prerequisites](#prerequisites) and the [port rules](#port-rules). Then, execute the following command on the machine where you want to deploy OpenVidu:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh)
```

--8<-- "shared/self-hosting/install-version.md"

A wizard will guide you through the installation process. You will be asked for the following information:

- **Write your OpenVidu PRO License**: Write your OpenVidu PRO License.
- **Select which certificate type to use**:
    - _Self Signed Certificate_: It will generate a self-signed certificate. It is not recommended for production environments, but it is useful for testing or development purposes.
    - _Let's Encrypt_: It will automatically generate a certificate for your domain. The Let's Encrypt email is required and will be asked later in the wizard.
    - _ZeroSSL_: It will automatically generate a certificate for your domain using ZeroSSL. An API Key is required and will be asked later in the wizard.
    - _Own Certificate_: It will ask you for the certificate and key files. Just copy and paste the content of the files when the wizard asks for them.

    !!! Note
        If you want to manage the certificate in your proxy own proxy server instead of relaying in the Caddy server deployed with OpenVidu, take a look to this How-to guide: [How to deploy OpenVidu with an external proxy](../../how-to-guides/deploy-with-external-proxy.md).

- **Domain name**: The domain name for your deployment. It must be an FQDN pointing to the machine where you are deploying OpenVidu.
- **(Optional) Turn domain name**: The domain name for your TURN server with TLS. It must be an FQDN pointing to the machine where you are deploying OpenVidu and must be different from the OpenVidu domain name. Recommended if users who are going to connect to your OpenVidu deployment are behind restrictive firewalls.
- **Select which RTC engine to use**: Select the WebRTC engine you want to use. You can choose between **Pion (the default engine used by LiveKit)** and **Mediasoup (with a boost in performance)**. Learn more about the differences [here](../../production-ready/performance.md).
- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:
    - [_OpenVidu Meet_](../../../../meet/index.md): A high-quality video calling service based on OpenVidu.
    - _Observability_: Grafana stack, which includes logs and monitoring stats.
    - _OpenVidu V2 Compatibility_: Compatibility API for applications developed with OpenVidu v2.

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

When the installation process finishes, you will see the following message:

```
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
>                                                                             <
>  🎉 OpenVidu Single Node PRO Installation Finished Successfully! 🎉         <
>                                                                             <
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
```

OpenVidu will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

```bash
systemctl start openvidu
```

If everything goes well, all containers will be up and running without restarts, and you will be able to access any of the following services:

- OpenVidu Meet: [https://openvidu.example.io/](https://openvidu.example.io/){:target=_blank}
- OpenVidu Dashboard: [https://openvidu.example.io/dashboard](https://openvidu.example.io/dashboard/){:target=_blank}
- MinIO: [https://openvidu.example.io/minio-console](https://openvidu.example.io/minio-console/){:target=_blank}
- Grafana: [https://openvidu.example.io/grafana](https://openvidu.example.io/grafana/){:target=_blank}

## Configure your application to use the deployment

To point your applications to your OpenVidu deployment, check the file at `/opt/openvidu/.env`. All access credentials of all services are defined in this file.

Your authentication credentials and URLs to point your applications to are:

- **URL**: The value in `.env` of `DOMAIN_OR_PUBLIC_IP` as a URL. It could be `wss://openvidu.example.io/` or `https://openvidu.example.io/` depending on the SDK you are using.
- **API Key**: The value in `.env` of `LIVEKIT_API_KEY`
- **API Secret**: The value in `.env` of `LIVEKIT_API_SECRET`

## Non-interactive installation

If you want to automate the installation process, you can generate a command with all the parameters needed to install OpenVidu by answering the wizard questions. You can do this by running the following command:

```
docker run --pull always --rm -it \
    openvidu/openvidu-installer:latest \
    --deployment-type=single_node_pro
```

--8<-- "shared/self-hosting/install-version.md"

This is going to generate a command like this, but it may vary depending on the answers you provide. Here are three examples of the command you can run depending on the certificate type you choose:

=== "Let's Encrypt certificates"

    Example using Let's Encrypt certificates:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
        --no-tty --install \
        --openvidu-pro-license='xxxxx' \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,v2compatibility,openviduMeet' \
        --turn-domain-name='turn.example.io' \
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
        --meet-admin-user='xxxxx' \
        --meet-admin-password='xxxxx' \
        --meet-api-key='xxxxx' \
        --certificate-type='letsencrypt' \
        --letsencrypt-email='example@example.io'
    ```

    --8<-- "shared/self-hosting/install-version.md"

        - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](/account/){:target="_blank"}.
        - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

=== "Self-signed certificates"

    Example using self-signed certificates:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
        --no-tty --install \
        --openvidu-pro-license='xxxxx' \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,v2compatibility,openviduMeet' \
        --turn-domain-name='turn.example.io' \
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
        --meet-admin-user='xxxxx' \
        --meet-admin-password='xxxxx' \
        --meet-api-key='xxxxx' \
        --certificate-type='selfsigned' \
        --letsencrypt-email='example@example.io'
    ```

    --8<-- "shared/self-hosting/install-version.md"

    - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](/account/){:target="_blank"}.
    - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

=== "Custom certificates"

    Example using custom certificates:

    ```bash
    CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
    CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

    # Optional, only if you want to enable TURN with TLS
    CERT_TURN_PRIVATE_KEY=$(cat turn-privkey.pem | base64 -w 0)
    CERT_TURN_PUBLIC_KEY=$(cat turn-fullchain.pem | base64 -w 0)

    sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
        --no-tty --install \
        --openvidu-pro-license='xxxxx' \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,v2compatibility,openviduMeet' \
        --turn-domain-name='turn.example.io' \
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
        --meet-admin-user='xxxxx' \
        --meet-admin-password='xxxxx' \
        --meet-api-key='xxxxx' \
        --certificate-type='owncert' \
        --owncert-private-key="$CERT_PRIVATE_KEY" \
        --owncert-public-key="$CERT_PUBLIC_KEY" \
        --turn-owncert-private-key="$CERT_TURN_PRIVATE_KEY" \
        --turn-owncert-public-key="$CERT_TURN_PUBLIC_KEY"
    ```

    --8<-- "shared/self-hosting/install-version.md"

    - Note that you just need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.
    - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](/account/){:target="_blank"}.
    - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
    - `--turn-owncert-private-key` and `--turn-owncert-public-key` are optional. You only need to pass them if you want to enable TURN with TLS.

You can run that command in a CI/CD pipeline or in a script to automate the installation process.

Some notes about the command:

- The argument `--turn-domain-name` is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls.
- At the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `openviduMeet` [OpenVidu Meet service](../../../../meet/index.md), `observability` (Grafana stack) and `v2compatibility` (OpenVidu v2 compatibility API).
- If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media.

To start OpenVidu, remember to run:

```bash
systemctl start openvidu
```

## Configuration and administration

Once you have OpenVidu deployed, you can check the [Administration](./admin.md) section to learn how to manage your OpenVidu Single Node deployment.
