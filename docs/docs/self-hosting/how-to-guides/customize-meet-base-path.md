---
description: Learn how to change the base path where OpenVidu Meet is served in your deployment.
---

# Customize OpenVidu Meet base path

By default, OpenVidu Meet is served at the `/meet` path (e.g. `https://your-domain/meet`). You can change this by setting the `MEET_BASE_PATH` parameter in `openvidu.env`.

## Configuration

Edit the `openvidu.env` file on your deployment:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

Set the `MEET_BASE_PATH` parameter to your desired path:

```bash
MEET_BASE_PATH=/custom-path
```

Then restart OpenVidu to apply the changes:

```bash
systemctl restart openvidu
```

After restarting, OpenVidu Meet will be accessible at `https://your-domain/custom-path` instead of `https://your-domain/meet`.

## Setting `MEET_BASE_PATH` to `/` { #root-path }

You can set `MEET_BASE_PATH=/` to serve OpenVidu Meet at the root path of your domain. However, this has an important side effect: the automatic proxy from `/` to port **6080** will no longer be available. This means you **cannot** [deploy a custom application alongside OpenVidu](/meet/embedded/deploy-your-app.md#deploy-alongside-openvidu) using port 6080, because the root path is already taken by OpenVidu Meet.

If you need to deploy a custom application with `MEET_BASE_PATH=/`, you must [deploy it in a separate environment](/meet/embedded/deploy-your-app.md#deploy-in-a-separate-environment) instead.

## Update your application { #update-application }

If you have an application built with [OpenVidu Meet Embedded](/meet/embedded/intro.md), you need to update it to use the new base path. Replace `/meet` with your configured path in:

- **REST API URLs**: e.g. `https://your-domain/<MEET_BASE_PATH>/api/v1/rooms` instead of `https://your-domain/meet/api/v1/rooms`.
- **Web Component script tag**: update the `src` attribute to match the new path:

    ```html
    <script src="https://your-domain/<MEET_BASE_PATH>/v1/openvidu-meet.js"></script>
    ```

- **OpenVidu Meet console URL**: the console will be accessible at `https://your-domain/<MEET_BASE_PATH>` instead of `https://your-domain/meet`.
- **Webhook configuration**: if you configured webhooks from the console, navigate to the console at the new path to manage them.
