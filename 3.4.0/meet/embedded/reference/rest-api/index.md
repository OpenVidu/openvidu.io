## Overview

OpenVidu Meet provides a REST API for managing **rooms** and **recordings** programmatically from your application's backend. As a general rule, any action that is available in OpenVidu Meet UI for rooms and recordings can also be performed using the REST API.

There are two endpoints:

- `/api/v1/rooms`: manage [rooms](https://openvidu.io/3.4.0/meet/features/rooms-and-meetings/index.md).
- `/api/v1/recordings`: manage [recordings](https://openvidu.io/3.4.0/meet/features/recordings/index.md).

## Authentication

Any request to the OpenVidu Meet REST API must include a valid API key in the `X-API-KEY` header:

```text
X-API-KEY: your-openvidu-meet-api-key
```

### Generate an API key

1. Connect to OpenVidu Meet console at `https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/`.
1. Navigate to the **"Embedded"** page.
1. Click on **" Generate API Key"** button.

\[[](../../../../assets/videos/meet/generate-api-key.mp4)\](https://openvidu.io/3.4.0/assets/videos/meet/generate-api-key.mp4)

## Reference

You can access the REST API reference documentation at:

- [**OpenVidu Meet REST API Reference**](https://openvidu.io/3.4.0/meet/embedded/reference/api.html)
- **Your own OpenVidu Meet deployment** serves the documentation at **`https://{{ your-openvidu-deployment-domain }}/api/v1/docs/`**

### Code snippets

The reference documentation provides code snippets for each REST API method. You can choose from countless languages and frameworks and copy-paste directly to your code.

### Testing API Endpoints

When accessing the REST API documentation from your own OpenVidu Meet deployment at **`https://{{ your-openvidu-deployment-domain }}/api/v1/docs/`**, you can test every endpoint directly from the browser. This is a great way to explore the API's body requests and responses.

Just configure a valid API key in the `X-API-KEY` header input.

\[[](../../../../assets/videos/meet/rest-api-test.mp4)\](https://openvidu.io/3.4.0/assets/videos/meet/rest-api-test.mp4)
