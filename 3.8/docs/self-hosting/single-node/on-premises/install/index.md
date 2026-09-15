# OpenVidu Single Node installation: On-premises

On-premises

This section contains instructions for deploying a production-ready OpenVidu Single Node deployment on-premises, in either the COMMUNITY or PRO edition. It is based on Docker and Docker Compose, which automatically configure all necessary services for OpenVidu to work properly.

Info

OpenVidu Single Node Pro is part of **OpenVidu** **PRO**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/3.8/account/index.md) to get your license key. There's a 15-day free trial waiting for you!

**Architecture overview**

This is what the deployment architecture looks like:

OpenVidu Single Node On Premises Architecture

All services are deployed on a single machine, which includes:

- **OpenVidu Server (LiveKit compatible)**.
- **Ingress** and **Egress** services.
- **OpenVidu Dashboard**, a web application interface to visualize your Rooms, Ingress, and Egress services.
- **MinIO** as an S3 storage service for recordings.
- **Redis** as a shared database for OpenVidu Server and Ingress/Egress services.
- **MongoDB** as a database for storing analytics and monitoring data.
- **Caddy** as a reverse proxy. It can be deployed with self-signed certificates, Let's Encrypt certificates, or custom certificates.
- **[OpenVidu Meet](https://openvidu.io/3.8/meet/index.md)**, an optional high-quality video calling service.
- **Grafana, Mimir, Promtail, and Loki (Observability module)** form an optional observability stack for monitoring, allowing you to keep track of logs and deployment statistics for OpenVidu.
- **OpenVidu V2 Compatibility (v2compatibility module)** **PRO** is an optional service that provides an API designed to maintain compatibility for applications developed with OpenVidu version 2.

## Prerequisites

Before starting the installation process, make sure you have the following prerequisites:

- **A machine with at least 4GB RAM and 4 CPU cores** and **Linux installed (Ubuntu recommended)**.
- **Generous disk space (100GB recommended)** if you are going to record your sessions.
- The machine **must have a Public IP**. An FQDN (Fully Qualified Domain Name) is optional. If not provided, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it.

## Port rules

Ensure all these rules are configured in your firewall, security group, or any network configuration on your machine.

**Inbound port rules**:

| Protocol | Ports         | Source          | Description                                                                                                                         |
| -------- | ------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| TCP      | 80            | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation.                                                                        |
| TCP      | 443           | 0.0.0.0/0, ::/0 | Allows access to the following: - LiveKit API. - OpenVidu Dashboard. - OpenVidu Meet. - WHIP API. - TURN with TLS. - Custom layouts |
| UDP      | 443           | 0.0.0.0/0, ::/0 | STUN/TURN server over UDP.                                                                                                          |
| TCP      | 1935          | 0.0.0.0/0, ::/0 | Needed if you want to ingest RTMP streams using Ingress service.                                                                    |
| TCP      | 7881          | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with the Pion engine.                                                                      |
| UDP      | 7885          | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP.                                                                                     |
| TCP      | 9000          | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly.                                                                                        |
| UDP      | 50000 - 60000 | 0.0.0.0/0, ::/0 | WebRTC Media traffic.                                                                                                               |
| TCP      | 50000 - 60000 | 0.0.0.0/0, ::/0 | **PRO** Needed for WebRTC media traffic over TCP when using the Mediasoup engine.                                                   |

Make sure the proper ports are opened in the internal Linux firewall!

If a Linux machine has an internal firewall installed, make sure you open the proper ports. For Ubuntu, you can follow these instructions:

1. Execute the following commands to install firewall-cmd and start it in the machine.

   ```text
   sudo apt install firewalld -y
   systemctl enable firewalld
   systemctl start firewalld
   ```

1. Execute the following commands to clear the iptables rules, accept all input, and deactivate iptables at startup:

   ```text
   sudo iptables -F
   sudo iptables -P INPUT ACCEPT
   ```

1. Execute the following commands to add the firewall rules:

   ```text
   firewall-cmd --add-port=80/tcp
   firewall-cmd --permanent --add-port=80/tcp
   ```

   ```text
   firewall-cmd --add-port=443/tcp
   firewall-cmd --permanent --add-port=443/tcp
   ```

   ```text
   firewall-cmd --add-port=443/udp
   firewall-cmd --permanent --add-port=443/udp
   ```

   ```text
   firewall-cmd --add-port=1935/tcp
   firewall-cmd --permanent --add-port=1935/tcp
   ```

   ```text
   firewall-cmd --add-port=7881/tcp
   firewall-cmd --permanent --add-port=7881/tcp
   ```

   ```text
   firewall-cmd --add-port=7885/udp
   firewall-cmd --permanent --add-port=7885/udp
   ```

   ```text
   firewall-cmd --add-port=9000/tcp
   firewall-cmd --permanent --add-port=9000/tcp
   ```

   ```text
   firewall-cmd --add-port=50000-60000/udp
   firewall-cmd --permanent --add-port=50000-60000/udp
   ```

PRO only, if you plan to use the Mediasoup engine:

```text
firewall-cmd --add-port=50000-60000/tcp
firewall-cmd --permanent --add-port=50000-60000/tcp
```

Finish with the following commands to apply the rules and verify they are correct:

```text
firewall-cmd --reload
firewall-cmd --runtime-to-permanent
```

```text
firewall-cmd --list-all
```

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Guided Installation

Before the installation, ensure that your machine meets the [prerequisites](#prerequisites) and the [port rules](#port-rules). Then, execute the following command on the machine where you want to deploy OpenVidu:

**OpenVidu COMMUNITY**

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh)
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

A wizard will guide you through the installation process. You will be asked for the following information:

- **Domain name** (Optional): The domain name for your deployment. If left empty, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it. For production environments, it's recommended to provide your own FQDN.

- - *Self Signed Certificate*: It will generate a self-signed certificate. It is not recommended for production environments, but it is useful for testing or development purposes.
  - *Let's Encrypt*: It will automatically generate a certificate for your domain.
  - *ZeroSSL*: It will automatically generate a certificate for your domain using ZeroSSL. An API Key is required and will be asked later in the wizard. **Note**: This option is only available when providing an FQDN (Fully Qualified Domain Name).
  - *Own Certificate*: It will ask you for the certificate and key files. Just copy and paste the content of the files when the wizard asks for them. **Note**: This option is only available when providing an FQDN (Fully Qualified Domain Name).

  **Select which certificate type to use**:

  Note

  If you want to manage the certificate in your own proxy server instead of relying in the Caddy server deployed with OpenVidu, take a look to this How-to guide: [How to deploy OpenVidu with an external proxy](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/deploy-with-external-proxy/index.md).

- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:

  - [*OpenVidu Meet*](https://openvidu.io/3.8/meet/index.md): A high-quality video calling service based on OpenVidu.
  - *Observability*: Grafana stack, which includes logs and monitoring stats.

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

When the installation process finishes, you will see the following message:

```text
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
>                                                                             <
>  🎉 OpenVidu Community Installation Finished Successfully! 🎉               <
>                                                                             <
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
```

**OpenVidu PRO**

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh)
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

A wizard will guide you through the installation process. You will be asked for the following information:

- **Domain name** (Optional): The domain name for your deployment. If left empty, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it. For production environments, it's recommended to provide your own FQDN.

- - *Self Signed Certificate*: It will generate a self-signed certificate. It is not recommended for production environments, but it is useful for testing or development purposes.
  - *Let's Encrypt*: It will automatically generate a certificate for your domain.
  - *ZeroSSL*: It will automatically generate a certificate for your domain using ZeroSSL. An API Key is required and will be asked later in the wizard. **Note**: This option is only available when providing an FQDN (Fully Qualified Domain Name).
  - *Own Certificate*: It will ask you for the certificate and key files. Just copy and paste the content of the files when the wizard asks for them. **Note**: This option is only available when providing an FQDN (Fully Qualified Domain Name).

  **Select which certificate type to use**:

  Note

  If you want to manage the certificate in your own proxy server instead of relying in the Caddy server deployed with OpenVidu, take a look to this How-to guide: [How to deploy OpenVidu with an external proxy](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/deploy-with-external-proxy/index.md).

- **Write your OpenVidu PRO License**: Write your OpenVidu PRO License.

- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:

  - [*OpenVidu Meet*](https://openvidu.io/3.8/meet/index.md): A high-quality video calling service based on OpenVidu.
  - *Observability*: Grafana stack, which includes logs and monitoring stats.
  - *OpenVidu V2 Compatibility*: Compatibility API for applications developed with OpenVidu v2.

- **Select which RTC engine to use**: Select the WebRTC engine you want to use. You can choose between **Pion (the default engine used by LiveKit)** and **Mediasoup (with a boost in performance)**. Learn more about the differences [here](https://openvidu.io/3.8/docs/self-hosting/production-ready/performance/index.md).

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

When the installation process finishes, you will see the following message:

```text
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

- OpenVidu Meet: `https://openvidu.example.io/`
- OpenVidu Dashboard: `https://openvidu.example.io/dashboard`
- MinIO: `https://openvidu.example.io/minio-console`
- Grafana: `https://openvidu.example.io/grafana`

## Configure your application to use the deployment

To point your applications to your OpenVidu deployment, check the following files:

- `/opt/openvidu/config/meet.env`: Contains the OpenVidu Meet parameters.
- `/opt/openvidu/config/openvidu.env`: Contains all the credentials of services deployed with OpenVidu Platform.

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

If you want to automate the installation process, you can generate a command with all the parameters needed to install OpenVidu by answering the wizard questions. You can do this by running the following command:

```text
docker run --pull always --rm -it \
    openvidu/openvidu-installer:latest \
    --deployment-type=single_node
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

This is going to generate a command like this, but it may vary depending on the answers you provide. Here are examples of the command you can run depending on the certificate type and domain configuration:

**OpenVidu COMMUNITY**

**Without Domain Name**

**Let's Encrypt certificates**

Example using Let's Encrypt certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --enabled-modules='observability,openviduMeet' \
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
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

**Self-signed certificates**

Example using self-signed certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --enabled-modules='observability,openviduMeet' \
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
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

**With Domain Name**

**Let's Encrypt certificates**

Example using Let's Encrypt certificates with an FQDN (Fully Qualified Domain Name):

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,openviduMeet' \
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
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

**Self-signed certificates**

Example using self-signed certificates with an FQDN (Fully Qualified Domain Name):

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,openviduMeet' \
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
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

**Custom certificates**

Example using custom certificates with an FQDN (Fully Qualified Domain Name):

```bash
CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
    --enabled-modules='observability,openviduMeet' \
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
    --certificate-type='owncert' \
    --owncert-private-key="$CERT_PRIVATE_KEY" \
    --owncert-public-key="$CERT_PUBLIC_KEY"
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- Note that you only need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.

**OpenVidu PRO**

**Without Domain Name**

**Let's Encrypt certificates**

Example using Let's Encrypt certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
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
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/3.8/account/index.md) .
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**Self-signed certificates**

Example using self-signed certificates without a domain name (the public IP is used as the domain name):

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
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
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/3.8/account/index.md) .
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**With Domain Name**

**Let's Encrypt certificates**

Example using Let's Encrypt certificates:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
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
    --certificate-type='letsencrypt'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/3.8/account/index.md) .
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**Self-signed certificates**

Example using self-signed certificates:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
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
    --certificate-type='selfsigned'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/3.8/account/index.md) .
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**Custom certificates**

Example using custom certificates:

```bash
CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
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
    --certificate-type='owncert' \
    --owncert-private-key="$CERT_PRIVATE_KEY" \
    --owncert-public-key="$CERT_PUBLIC_KEY"
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/3.8/account/index.md) .
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
- Note that you only need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.

You can run that command in a CI/CD pipeline or in a script to automate the installation process.

Some notes about the command:

- The argument `--domain-name` is optional. If not provided, the public IP is used as the domain name, and a [Let's Encrypt](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) certificate is issued for it.
- When using autogenerated domains (no FQDN (Fully Qualified Domain Name) provided), only `selfsigned` and `letsencrypt` certificate types are available.
- In the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `openviduMeet` [OpenVidu Meet service](https://openvidu.io/3.8/meet/index.md), `observability` (Grafana stack) and, PRO only, `v2compatibility` (OpenVidu v2 compatibility API).
- If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media.

To start OpenVidu, remember to run:

```bash
systemctl start openvidu
```

## Configuration and administration

Once you have OpenVidu deployed, you can check the [Administration](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md) section to learn how to manage your OpenVidu Single Node deployment.

## Plain Docker Compose installation

This installation method is targeted to advanced users, and is only available for the **COMMUNITY** edition

This installation mechanism is more friendly with GitOps procedures, because all the configuration and deployment is managed through plain text files.

Compared to the standard guided installation, it does not include a wizard to guide you through the installation process, so you need to manually edit the configuration files and manage the lifecycle of the deployment using standard Docker Compose commands.

Follow the instructions at this [Git repository](https://github.com/OpenVidu/openvidu-docker-compose-deployment) .
