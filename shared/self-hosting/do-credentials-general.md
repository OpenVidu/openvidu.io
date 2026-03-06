**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET_INITIAL_ADMIN_USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

!!! note
    The `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` values are initial settings that changing them will not affect to the deployment. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: API Secret for LiveKit SDKs.
