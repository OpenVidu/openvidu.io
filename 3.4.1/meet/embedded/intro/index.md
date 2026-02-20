With **OpenVidu Meet Embedded**, you can integrate the best video calling experience directly into your own application:

- Quick setup using a **URL**, an **iframe** or a **Web Component**.
- Integrate into your application's logic using **REST API** and **Webhooks**.
- Customizable user interface to match your app's **branding and style**.

**Add video calling capabilities to your app with a single line of HTML**

```html
<openvidu-meet room-url="https://YOUR_DOMAIN/room/your-room?secret=1234567"></openvidu-meet>
```

- **Create rooms through REST API**

  ```bash
  curl --request POST \
    --url https://YOUR_DOMAIN/api/v1/rooms \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --header 'X-API-KEY: YOUR_API_KEY' \
    --data '{"roomName": "my-room"}'
  ```

- **Manage recordings through REST API**

  ```bash
  curl --request GET \
    --url https://YOUR_DOMAIN/api/v1/recordings \
    --header 'Accept: application/json' \
    --header 'X-API-KEY: YOUR_API_KEY'
  ```

**Integrate OpenVidu Meet into your own UI and business logic**

______________________________________________________________________

## Where to start? We recommend following the [**step by step guide**](https://openvidu.io/3.4.1/meet/embedded/step-by-step-guide) or exploring one of our [**tutorials**](https://openvidu.io/3.4.1/meet/embedded/tutorials).
