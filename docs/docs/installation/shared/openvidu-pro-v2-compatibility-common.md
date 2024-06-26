If you are using in `COMPOSE_PROFILES` at the `.env` file the `v2compatibility` profile, you will need to set the following parameters in the `.env` file for the OpenVidu V2 Compatibility service:

| <div style="width:24em">Parameter</div> | Description | Default Value |
| --- | --- | --- |
| **`V2COMPAT_OPENVIDU_SECRET`** | OpenVidu secret used to authenticate the OpenVidu V2 Compatibility service. In the `.env` file, this value is defined with `LIVEKIT_API_SECRET`. | The value of `LIVEKIT_API_SECRET` in the `.env` file. |
| **`V2COMPAT_OPENVIDU_WEBHOOK`** | `true` to enable OpenVidu Webhook service. `false` otherwise. Valid values are `true` or `false`. | `false` |
| **`V2COMPAT_OPENVIDU_WEBHOOK_ENDPOINT`** | HTTP(S) endpoint to send OpenVidu V2 Webhook events. Must be a valid URL. Example: <br><br> `V2COMPAT_OPENVIDU_WEBHOOK_ENDPOINT=http://myserver.com/webhook` | - |
| **`V2COMPAT_OPENVIDU_WEBHOOK_HEADERS`** | JSON Array list of headers to send in the OpenVidu V2 Webhook events. Example: <br><br> `V2COMPAT_OPENVIDU_WEBHOOK_HEADERS=["Content-Type: application/json"]` | `[]` |
| **`V2COMPAT_OPENVIDU_WEBHOOK_EVENTS`** | Comma-separated list of OpenVidu V2 Webhook events to send. Example: <br><br> `V2COMPAT_OPENVIDU_WEBHOOK_EVENTS=sessionCreated,sessionDestroyed` | `sessionCreated`, `sessionDestroyed,` `participantJoined,` `participantLeft,` `webrtcConnectionCreated,` `webrtcConnectionDestroyed,` `recordingStatusChanged,` `signalSent` <br><br> _(All available events)_ |
| **`V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET`** | S3 Bucket where to store recording files. | `openvidu` |
| **`V2COMPAT_OPENVIDU_PRO_AWS_S3_SERVICE_ENDPOINT`** | S3 Endpoint where to store recording files. | `http://localhost:9100` |
| **`V2COMPAT_OPENVIDU_PRO_AWS_ACCESS_KEY`** | S3 Access Key of the S3 Bucket where to store recording files. | - |
| **`V2COMPAT_OPENVIDU_PRO_AWS_SECRET_KEY`** | S3 Secret Key of the S3 Bucket where to store recording files. | - |
| **`V2COMPAT_OPENVIDU_PRO_AWS_REGION`** | S3 Region of the S3 Bucket where to store recording files. | `us-east-1` |
