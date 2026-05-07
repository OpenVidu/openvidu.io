**OpenVidu Meet**:

- **`OPENVIDU_URL`**: The URL used to access OpenVidu Meet, always `https://yourdomain.example.io/`.
- **`MEET_INITIAL_ADMIN_USER`**: The user account for accessing the OpenVidu Meet Console. Always `admin`.
- **`MEET_INITIAL_ADMIN_PASSWORD`**: The password for accessing the OpenVidu Meet Console.
- **`MEET_INITIAL_API_KEY`**: The API key for using the OpenVidu Meet Embedded and OpenVidu Meet REST API.

!!! note
    `MEET_INITIAL_ADMIN_USER`, `MEET_INITIAL_ADMIN_PASSWORD`, and `MEET_INITIAL_API_KEY` are initial settings only. Changing them here will not affect the deployment — they can only be modified from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT_URL`**: The URL used with LiveKit SDKs. This can be either `wss://yourdomain.example.io/` or `https://yourdomain.example.io/`, depending on the client library you are using.
- **`LIVEKIT_API_KEY`**: The API key for LiveKit SDKs.
- **`LIVEKIT_API_SECRET`**: The API secret for LiveKit SDKs.
