**OpenVidu Meet**:

- **`OPENVIDU-URL`**: The URL to access OpenVidu Meet, which is always `https://yourdomain.example.io/`
- **`MEET-INITIAL-ADMIN-USER`**: User to access OpenVidu Meet Console. It is always `admin`.
- **`MEET-INITIAL-ADMIN-PASSWORD`**: Password to access OpenVidu Meet Console.
- **`MEET-INITIAL-API-KEY`**: API key to use OpenVidu Meet Embedded and OpenVidu Meet REST API.

!!! note
    The `MEET-INITIAL-ADMIN-USER`, `MEET-INITIAL-ADMIN-PASSWORD`, and `MEET-INITIAL-API-KEY` values are initial settings that cannot be changed from Azure Key Vault. They can only be changed from the Meet Console.

**OpenVidu Platform:**

- **`LIVEKIT-URL`**: The URL to use LiveKit SDKs, which can be `wss://yourdomain.example.io/` or `https://yourdomain.example.io/` depending on the client library you are using.
- **`LIVEKIT-API-KEY`**: API Key for LiveKit SDKs.
- **`LIVEKIT-API-SECRET`**: API Secret for LiveKit SDKs.
