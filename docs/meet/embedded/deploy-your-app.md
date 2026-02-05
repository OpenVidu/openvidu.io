---
description: Learn how to deploy your custom application built with OpenVidu Meet in production, either alongside your OpenVidu deployment or in a separate environment.
---

# Deploy your OpenVidu Meet application

Once your application built with [OpenVidu Meet Embedded](./intro.md) is ready for production, you need to decide where to deploy it. Before proceeding, make sure you have a running OpenVidu Meet deployment. If you don't have one yet, check the [Deployment](../deployment/overview.md) section to set one up.

There are two options:

- [**Deploy alongside OpenVidu**](#deploy-alongside-openvidu): Run your application on the same server(s) as your OpenVidu deployment. OpenVidu will automatically proxy requests to your application.
- [**Deploy in a separate environment**](#deploy-in-a-separate-environment): Run your application on its own infrastructure and connect it to your OpenVidu deployment remotely.

!!! info
    All examples in this guide use the default OpenVidu Meet base path `/meet`. If you have changed it using the `MEET_BASE_PATH` parameter in `openvidu.env`, replace `/meet` with your configured path in all URLs mentioned below. See the [Customize OpenVidu Meet base path](/docs/self-hosting/how-to-guides/customize-meet-base-path/) how-to guide for more details.

---

## Deploy alongside OpenVidu

You can deploy your application directly on the same node(s) as OpenVidu. When OpenVidu detects an application listening on port **6080**, it will automatically proxy all requests to the root path `/` of your domain (e.g. `https://example.openvidu.io/`) to your application.

This means your application will be served at `https://your-domain/`, while the OpenVidu Meet console will remain accessible at `https://your-domain/meet`.

### 1. Point your application to OpenVidu Meet

Configure your application to use the OpenVidu Meet REST API. Since your application runs on the same node, you can use either the local address or the public domain:

- **Local address:** `http://localhost:9080/meet`
- **Public domain:** `https://your-domain/meet`

Both options work the same way. For example, your application can make API requests to `http://localhost:9080/meet/api/v1/rooms` or `https://your-domain/meet/api/v1/rooms`.

See the [REST API reference](./reference/rest-api.md) for the full list of available endpoints.

### 2. Deploy your application on the OpenVidu node

Deploy your application so that it listens on port **6080**. The specific node where you need to deploy depends on your deployment type:

=== "Single Node"

    Deploy your application on the single node of your OpenVidu deployment. Any request to `https://your-domain/` will be proxied to your application at `http://localhost:6080`.

=== "Elastic"

    Deploy your application on the **Master Node** of your OpenVidu Elastic deployment. Any request to `https://your-domain/` will be proxied to your application at `http://localhost:6080`.

=== "High Availability"

    Deploy your application on **every Master Node** of your OpenVidu HA deployment. Any request to `https://your-domain/` will be proxied to your application at `http://localhost:6080` on each Master Node.

    !!! warning
        Your application **must be horizontally scalable** for High Availability deployments. Since requests can be routed to any Master Node, your application must be deployed and running on all of them. Make sure your application handles shared state appropriately (e.g. using a shared database or external session store).

### 3. Configure the API key

Your application needs an API key to authenticate requests to the OpenVidu Meet REST API. You can obtain it from the OpenVidu Meet console:

1. Navigate to `https://your-domain/meet`.
2. Go to the **"Embedded"** page.
3. Click on **":material-key: Generate API Key"** if you haven't generated one already.

Use this API key in your application to authenticate REST API requests via the `X-API-KEY` header. See the [REST API authentication](./reference/rest-api.md#authentication) section for more details.

### 4. Configure the Web Component URL (if applicable)

If your application uses the [OpenVidu Meet Web Component](./reference/webcomponent.md), make sure the script tag points to your OpenVidu deployment's public domain:

```html
<script src="https://<YOUR_OPENVIDU_DOMAIN>/meet/v1/openvidu-meet.js"></script>
```

### 5. Configure webhooks (optional) { #alongside-webhooks }

If your application uses [OpenVidu Meet webhooks](./reference/webhooks.md), you need to configure the webhook URL to point to your application locally:

1. Navigate to `https://your-domain/meet`.
2. Go to the **"Embedded"** page.
3. Enable webhooks and set the webhook URL to:

    ```
    http://localhost:6080/<YOUR_WEBHOOK_PATH>
    ```

    Replace `<YOUR_WEBHOOK_PATH>` with the path where your application receives webhooks (e.g. `webhook`, `api/webhook`, etc.).

4. You can use the **"Test webhook"** button to verify that your application receives webhook events correctly.

!!! info
    Since your application runs on the same node as OpenVidu, the webhook URL uses `localhost`. This avoids any network overhead and does not require your webhook endpoint to be publicly accessible.

!!! info
    All webhook events are signed with your API key using HMAC SHA256. Always [validate webhook signatures](./reference/webhooks.md#validate-events) in your application to ensure authenticity and prevent tampering.

---

## Deploy in a separate environment

You can deploy your application on a completely separate server or infrastructure, connecting to the OpenVidu Meet deployment remotely. This gives you full control over your application's deployment, scaling, and infrastructure.

### 1. Point your application to OpenVidu Meet

Configure your application to use the OpenVidu Meet REST API at:

```
https://<YOUR_OPENVIDU_DOMAIN>/meet
```

For example, if your OpenVidu deployment is at `https://example.openvidu.io`, your application should make API requests to `https://example.openvidu.io/meet/api/v1/rooms`, `https://example.openvidu.io/meet/api/v1/recordings`, etc.

See the [REST API reference](./reference/rest-api.md) for the full list of available endpoints.

### 2. Configure the API key

Generate an API key from the OpenVidu Meet console and configure it in your application:

1. Navigate to your OpenVidu Meet console at `https://your-openvidu-domain/meet`.
2. Go to the **"Embedded"** page.
3. Click on **":material-key: Generate API Key"** if you haven't generated one already.
4. Configure the API key in your application. This key must be included in every request as the `X-API-KEY` header.

See the [REST API authentication](./reference/rest-api.md#authentication) section for more details.

### 3. Configure the Web Component URL (if applicable)

If your application uses the [OpenVidu Meet Web Component](./reference/webcomponent.md), make sure the script tag points to your OpenVidu deployment:

```html
<script src="https://<YOUR_OPENVIDU_DOMAIN>/meet/v1/openvidu-meet.js"></script>
```

### 4. Configure webhooks (optional) { #separate-webhooks }

If your application uses [OpenVidu Meet webhooks](./reference/webhooks.md), configure the webhook URL to point to your application's **publicly accessible** webhook endpoint:

1. Navigate to your OpenVidu Meet console at `https://your-openvidu-domain/meet`.
2. Go to the **"Embedded"** page.
3. Enable webhooks and set the webhook URL to your application's public endpoint:

    ```
    https://<YOUR_APP_DOMAIN>/<YOUR_WEBHOOK_PATH>
    ```

4. You can use the **"Test webhook"** button to verify that your application receives webhook events correctly.

!!! warning
    Your webhook endpoint **must be publicly accessible** from the OpenVidu deployment. Make sure your firewall and network configuration allow incoming HTTP requests from the OpenVidu server to your application's webhook URL.

!!! info
    All webhook events are signed with your API key using HMAC SHA256. Always [validate webhook signatures](./reference/webhooks.md#validate-events) in your application to ensure authenticity and prevent tampering.

---

## Notes

### Configuring API key and webhooks via `meet.env`

As an alternative to using the OpenVidu Meet console, you can configure the initial API key and webhook settings directly in the `meet.env` configuration file:

=== "Single Node"

    **Location:** `/opt/openvidu/config/meet.env`

=== "Elastic"

    **Location:** `/opt/openvidu/config/cluster/master_node/meet.env`

=== "High Availability"

    **Location:** `/opt/openvidu/config/cluster/master_node/meet.env`

The relevant parameters are:

| Parameter | Description |
| --------- | ----------- |
| **`MEET_INITIAL_API_KEY`** | API Key for the OpenVidu Meet service. Used by applications developed with OpenVidu Meet. |
| **`MEET_WEBHOOK_ENABLED`** | If `true`, the OpenVidu Meet service will send webhooks to the configured webhook endpoint. |
| **`MEET_WEBHOOK_URL`** | The URL where the OpenVidu Meet webhooks will be sent. |

After modifying the file, restart OpenVidu to apply the changes:

```bash
systemctl restart openvidu
```

See the [Configuration Reference](/docs/self-hosting/configuration/reference.md#meetenv) for all available `meet.env` parameters and the [Changing Configuration](/docs/self-hosting/configuration/changing-config.md) section for more details on how to modify configuration files.
