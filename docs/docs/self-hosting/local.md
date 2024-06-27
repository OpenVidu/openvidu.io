# Local Installation (Development)

For development purposes, we provide an [easy to install local deployment](https://github.com/OpenVidu/openvidu-local-deployment){:target="\_blank"} based on Docker Compose which will automatically configure all the necessary services for OpenVidu to develop and test your applications seamlessly.

## Installation instructions

First, make sure you have the following prerequisites:

=== ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

    - Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/){:target="\_blank"}

=== ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

    - Install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/){:target="\_blank"}

=== ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

    - Install [Docker](https://docs.docker.com/engine/install/#supported-platforms){:target="\_blank"}
    - Install [Docker Compose](https://docs.docker.com/compose/install/linux/){:target="\_blank"}

The installation consists of cloning a repository and running a script to configure your local IP address in the deployment. Then, you can start, stop, and manage your deployment with Docker Compose.

To install OpenVidu locally, follow these steps:

=== "OpenVidu <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span>"

    1.  Clone the following repository:

        ```bash
        git clone https://github.com/OpenVidu/openvidu-local-deployment
        ```

        !!!info
            To use a specific OpenVidu version, switch to the desired tag with `git checkout <version>`, e.g., `git checkout 3.0.0`. By default, the latest version is used.

    2.  Configure the local deployment

        === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

            ```powershell
            cd openvidu-local-deployment/community
            .\configure_lan_private_ip_windows.bat
            ```

        === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

            ```bash
            cd openvidu-local-deployment/community
            ./configure_lan_private_ip_macos.sh
            ```

        === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

            ```bash
            cd openvidu-local-deployment/community
            ./configure_lan_private_ip_linux.sh
            ```

    3.  Run OpenVidu

        ```bash
        docker compose up
        ```

=== "OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>"

    1.  Clone the following repository:

        ```bash
        git clone https://github.com/OpenVidu/openvidu-local-deployment
        ```

        !!!info
            To use a specific OpenVidu version, switch to the desired tag with `git checkout <version>`, e.g., `git checkout 3.0.0`. By default, the latest version is used.


    2.  Configure the local deployment

        === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

            ```powershell
            cd openvidu-local-deployment/pro
            .\configure_lan_private_ip_windows.bat
            ```

        === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

            ```bash
            cd openvidu-local-deployment/pro
            ./configure_lan_private_ip_macos.sh
            ```

        === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

            ```bash
            cd openvidu-local-deployment/pro
            ./configure_lan_private_ip_linux.sh
            ```

    3.  Run OpenVidu

        ```bash
        docker compose up
        ```

    !!!info
        <th colspan="2" class="title"><strong style="white-space: nowrap">OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span></strong></th> runs locally in evaluation mode for free for development and testing purposes. Some limits apply:

        - Maximum 2 concurrent Rooms
        - Maximum 8 Participants per Room
        - Maximum 5 minutes duration per Room

        For a production environment, you need to [create an OpenVidu account](https://openvidu.io/account){:target="_blank"} to get a license key.
        There's a 15 day free trial waiting for you!

The deployment is ready when you see the following message:

```
 =========================================
 🎉 OpenVidu is ready! 🎉
 =========================================

 OpenVidu Server && LiveKit Server URLs:

     - From this machine:

         - http://localhost:7880
         - ws://localhost:7880

     - From other devices in your LAN:

         - https://xxx-yyy-zzz-www.openvidu-local.dev:7443
         - wss://xxx-yyy-zzz-www.openvidu-local.dev:7443

 =========================================

 OpenVidu Developer UI (services and passwords):

     - http://localhost:7880
     - https://xxx-yyy-zzz-www.openvidu-local.dev:7443

 =========================================
```

By visiting [http://localhost:7880](http://localhost:7880){:target="\_blank"} you have the OpenVidu Developer UI available with a summary of the services and passwords deployed. You can access the following services:

- **OpenVidu API (LiveKit compatible)** ([http://localhost:7880](http://localhost:7880){:target="\_blank"}): the main API endpoint for your OpenVidu and LiveKit applications. OpenVidu v2 compatibility API is only available in <th colspan="2" class="title"><strong style="white-space: nowrap">OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span></strong></th>.
- **OpenVidu Dashboard** ([http://localhost:7880/dashboard](http://localhost:7880/dashboard){:target="\_blank"}): a web application interface to visualize your Rooms, Ingress and Egress services.
- **MinIO** ([http://localhost:7880/minio-console](http://localhost:7880/minio-console){:target="\_blank"}): as an S3 storage service for recordings.
- **OpenVidu Call (Default Application)** ([http://localhost:7880/openvidu-call](http://localhost:7880/openvidu-call){:target="\_blank"}): an optional ready-to-use videoconferencing application.

You just need to point your OpenVidu and LiveKit applications to `http://localhost:7880` or `ws://localhost:7880` and start developing. Check our [tutorials](../tutorials/application-client/index.md){:target="\_blank"} if you want a step-by-step guide to develop your first application using OpenVidu.

## Accessing your local deployment from other devices on your network

Testing WebRTC applications can be challenging because devices require a secure context (HTTPS) to access the camera and microphone. When using LiveKit Open Source, this isn't an issue if you access your app from the same computer where the LiveKit Server is running, as `localhost` is considered a secure context even over plain HTTP. Consider the following architecture:

<figure markdown="span">
  ![Image title](../../assets/images/comparing-openvidu/livekit-architecture.svg){ width="450" style="border-radius: 8px" }
</figure>

The simplest way to test your application is:

1. Run LiveKit Server on your computer.
2. Connect your app to LiveKit Server through `localhost`.
3. Serve both your application client and server from the same computer.
4. Access your app from `localhost` in a browser on the same computer.

This setup is straightforward, but what if you need to test your app from multiple devices simultaneously, including real mobile devices? In this case, you must use a secure context (HTTPS), which introduces two challenges:

1. LiveKit Server open source does not natively support HTTPS. You'll need a reverse proxy to serve LiveKit Server over HTTPS.
2. Even with HTTPS, your SSL certificate might not be valid for local network addresses. You'll need to accept it in the browser for web apps, and install it on mobile devices.

OpenVidu Local Deployment addresses these issues by providing a magic domain name `openvidu-local.dev` that resolves to any IP specified as a subdomain and provides a valid wildcard certificate for HTTPS. This is similar to services like [nip.io](https://nip.io){:target="\_blank"}, [traefik.me](https://traefik.me){:target="\_blank"}, or [localtls](https://github.com/Corollarium/localtls){:target="\_blank}.

When using OpenVidu Local Deployment, you can access OpenVidu Server (which is 100% LiveKit compatible) and your app from any device on your local network with a valid HTTPS certificate. The following table shows the URLs to access the deployment and your application locally and from other devices on your network:

|                                   | Local access                                                   | Access from devices in your local network                                                                                      |
| --------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Usage                             | Access only from the development machine                       | Access from any device connected to your local network. In the URLs below, replace **`xxx-yyy-zzz-www`{.no-break}** with the local IP address of the development machine, replacing the dots (`.`) with dashes (`-`). You can find the configured local IP in the **`.env`** file in the **`LAN_PRIVATE_IP`** variable |
| Application Client (frontend)     | [http://localhost:5080](http://localhost:5080)                 | [https://xxx-yyy-zzz-www.openvidu-local.dev:5443](https://xxx-yyy-zzz-www.openvidu-local.dev:5443)                            |
| Application Server (backend)      | [http://localhost:6080](http://localhost:6080)                 | [https://xxx-yyy-zzz-www.openvidu-local.dev:6443](https://xxx-yyy-zzz-www.openvidu-local.dev:6443)                            |
| OpenVidu (LiveKit Compatible) URL | [http://localhost:7880](http://localhost:7880)                 | [https://xxx-yyy-zzz-www.openvidu-local.dev:7443](https://xxx-yyy-zzz-www.openvidu-local.dev:7443)                            |

!!!info
    - If you are developing locally, use `localhost` to access the services, but if you want to test your application from other devices on your network, use the `openvidu-local.dev` URLs.
    - Replace `xxx-yyy-zzz-www` with your local IP address. You can find it in the `.env` file in the `LAN_PRIVATE_IP` variable.
!!!warning
    If the URL isn't working because the IP address is incorrect or the installation script couldn't detect it automatically, you can update the `LAN_PRIVATE_IP` value in the `.env` file and restart the deployment with `docker compose up`.


When developing web applications with this deployment, you can use the following code snippet to dynamically determine the appropriate URLs for the application server and the OpenVidu server based on the browser's current location. This approach allows you to seamlessly run your application on both your development machine and other devices within your local network without needing to manually adjust the URLs in your code.

```javascript
if (window.location.hostname === "localhost") {
  APPLICATION_SERVER_URL = "http://localhost:6080";
  OPENVIDU_URL = "wss://localhost:7443";
} else {
  APPLICATION_SERVER_URL = "https://" + window.location.hostname + ":6443";
  OPENVIDU_URL = "ws://" + window.location.hostname + ":7880";
}
```

## About `openvidu-local.dev` domain and SSL certificates

This setup simplifies the configuration of local OpenVidu deployments with SSL, making it easier to develop and test your applications securely on your local network by using the `openvidu-local.dev` domain and a wildcard SSL certificate valid for `*.openvidu-local.dev`. However, it’s important to note that these certificates are publicly available and do not provide an SSL certificate for production use.

The HTTPS offered by `openvidu-local.dev` is intended for development or testing purposes with the only goal of making your local devices trust your application (which is mandatory in WebRTC applications). For any other use case, it should be treated with the same security considerations as plain HTTP.

For production, you should consider deploying a [production-grade OpenVidu deployment](deployment-types.md#openvidu-single-node).
