## Overview

OpenVidu Meet provides a REST API for managing **rooms**, **room members**, **recordings** and **users** programmatically from your application's backend. As a general rule, any action that is available in the OpenVidu Meet UI for these resources can also be performed using the REST API.

The available endpoints are:

- `/api/v1/rooms`: manage [rooms](https://openvidu.io/3.8/meet/features/rooms/overview/index.md).
- `/api/v1/rooms/{roomId}/members`: manage [room members](https://openvidu.io/3.8/meet/features/room-members/overview/index.md) (users and identified guests of a room).
- `/api/v1/recordings`: manage [recordings](https://openvidu.io/3.8/meet/features/recordings/overview/index.md).
- `/api/v1/users`: manage [users](https://openvidu.io/3.8/meet/features/users/overview/index.md).

## Authentication

Any request to the OpenVidu Meet REST API must include a valid API key in the `X-API-KEY` header:

```text
X-API-KEY: your-api-key
```

### Generate an API key

1. Connect to OpenVidu Meet app at `https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/meet`.
1. Navigate to the **"Embedded"** page.
1. Click on **"Generate API Key"** button.

## Reference

You can access the REST API reference documentation at:

- [**OpenVidu Meet REST API Reference**](https://openvidu.io/3.8/meet/embedded/reference/api.html)
- **Your own OpenVidu Meet deployment** serves the documentation at **`https://{{ your-openvidu-deployment-domain }}/meet/api/v1/docs/`**

### Code snippets

The reference documentation provides code snippets for each REST API method. You can choose from countless languages and frameworks and copy-paste directly to your code.

OpenVidu Meet Prejoin

OpenVidu Meet Prejoin

### Testing API Endpoints

When accessing the REST API documentation from your own OpenVidu Meet deployment at **`https://{{ your-openvidu-deployment-domain }}/meet/api/v1/docs/`**, you can test every endpoint directly from the browser. This is a great way to explore the API's body requests and responses.

Just configure a valid API key in the `X-API-KEY` header input.
