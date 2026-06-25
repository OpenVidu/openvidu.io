## Overview

OpenVidu Meet provides a REST API for managing **rooms**, **room members**, **recordings** and **users** programmatically from your application's backend. As a general rule, any action that is available in the OpenVidu Meet UI for these resources can also be performed using the REST API.

The available endpoints are:

- `/api/v1/rooms`: manage [rooms](../../features/rooms/overview.md).
- `/api/v1/rooms/{roomId}/members`: manage [room members](../../features/room-members/overview.md) (users and identified guests of a room).
- `/api/v1/recordings`: manage [recordings](../../features/recordings/overview.md).
- `/api/v1/users`: manage [users](../../features/users/overview.md).

## Authentication

Any request to the OpenVidu Meet REST API must include a valid API key in the `X-API-KEY` header:

```
X-API-KEY: your-api-key
```

### Generate an API key

1. Connect to OpenVidu Meet app at `https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/meet`.
2. Navigate to the **"Embedded"** page.
3. Click on **"Generate API Key"** button.

<a class="glightbox" href="../../../../assets/videos/meet/generate-api-key.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery2"><video class="round-corners" style="margin-bottom: 2em" src="../../../../assets/videos/meet/generate-api-key.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

## Reference

You can access the REST API reference documentation at:

- [**OpenVidu Meet REST API Reference** :fontawesome-solid-external-link:{.external-link-icon}](./api.html){target="_blank"}
- **Your own OpenVidu Meet deployment** serves the documentation at **`https://{{ your-openvidu-deployment-domain }}/meet/api/v1/docs/`**{.no-break}

### Code snippets

The reference documentation provides code snippets for each REST API method. You can choose from countless languages and frameworks and copy-paste directly to your code.

<div class="grid cards no-border no-shadow two-columns" markdown>

<a class="glightbox" href="../../../../assets/images/meet/reference/rest-snippets-1.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../../assets/images/meet/reference/rest-snippets-1.png" loading="lazy" class="round-corners" alt="OpenVidu Meet Prejoin"/></a>

<a class="glightbox" href="../../../../assets/images/meet/reference/rest-snippets-2.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="../../../../assets/images/meet/reference/rest-snippets-2.png" loading="lazy" class="round-corners" alt="OpenVidu Meet Prejoin"/></a>

</div>

### Testing API Endpoints

When accessing the REST API documentation from your own OpenVidu Meet deployment at **`https://{{ your-openvidu-deployment-domain }}/meet/api/v1/docs/`**{.no-break}, you can test every endpoint directly from the browser. This is a great way to explore the API's body requests and responses.

Just configure a valid API key in the `X-API-KEY` header input.

<a class="glightbox" href="../../../../assets/videos/meet/rest-api-test.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../../assets/videos/meet/rest-api-test.mp4" defer muted playsinline autoplay loop async></video></a>