# Live Captions

OpenVidu Meet includes a built-in **Live Captions** feature that turns speech into text in real-time. This is a powerful tool for making your meetings more accessible to hearing-impaired users, helping participants in noisy environments, and assisting non-native speakers.

## How to Enable Live Captions in OpenVidu Meet

Local Meet Deployment Limitation

Live Captions are **not available** in local Meet deployments. You must use either the [OpenVidu Local deployment](https://openvidu.io/3.7.0/docs/self-hosting/local/index.md) or a [OpenVidu production deployment](https://openvidu.io/3.7.0/docs/self-hosting/deployment-types/index.md) to enable this feature.

### 1. Connect to your OpenVidu deployment

SSH into an OpenVidu Node and navigate to your OpenVidu deployment directory.

Depending on your [OpenVidu deployment type](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md):

If you are using [OpenVidu Local (Development)](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md#openvidu-local-development), simply navigate to the configuration folder of the project:

```bash
# For OpenVidu Local COMMUNITY
cd openvidu-local-deployment/community

# For OpenVidu Local PRO
cd openvidu-local-deployment/pro
```

If you are using [OpenVidu Single Node](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md#openvidu-single-node), SSH into the only OpenVidu node and navigate to:

```bash
cd /opt/openvidu/config
```

If you are using [OpenVidu Elastic](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md#openvidu-elastic), SSH into the only Master Node and navigate to:

```bash
cd /opt/openvidu/config/cluster/media_node
```

If you are using [OpenVidu High Availability](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md#openvidu-high-availability), SSH into any of your Master Nodes (doesn't matter which one) and navigate to:

```bash
cd /opt/openvidu/config/cluster/media_node
```

### 2. Enable the Speech Processing Agent

Modify file `agent-speech-processing.yaml` to enable the Live Captions Service with `processing: manual`:

```yaml
docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.7.0

enabled: true # (1)!

live_captions:
  processing: manual # (2)!
```

1. Set `enabled` to `true` to activate the Speech Processing Agent.
1. Set **processing** to `manual`; participants will activate captions on demand via a toolbar button.

Info

By default, the Speech Processing Agent uses a local Vosk model for speech-to-text transcription.

For a more advanced setup, consider using a cloud-based provider. See [Cloud providers](https://openvidu.io/3.7.0/docs/ai/live-captions/#cloud-providers) for more information.

Default language is English

The Speech Processing Agent uses **English** for speech-to-text transcription by default. To use a different language, you must configure a different Vosk model. See [Vosk models configuration](https://openvidu.io/3.7.0/docs/ai/live-captions/#vosk) for details on changing the language model.

### 3. Enable Captions in OpenVidu Meet configuration

Edit the `meet.env` file and ensure the following configuration variable is set:

```text
MEET_CAPTIONS_ENABLED=true
```

### 4. Restart OpenVidu

Apply your changes by restarting OpenVidu. This ensures the system recognizes the new live captioning capabilities.

Depending on your [OpenVidu deployment type](https://openvidu.io/3.7.0/meet/features/docs/self-hosting/deployment-types.md):

Run where `docker-compose.yaml` is located:

```bash
docker compose restart
```

Run this command in your node:

```bash
sudo systemctl restart openvidu
```

Run this command in your Master Node:

```bash
sudo systemctl restart openvidu
```

Run this command in one of your Master Nodes:

```bash
sudo systemctl restart openvidu
```

### 5. Enable/Disable Captions for specific Rooms

Captions are enabled by default when a room is created, whether through the UI or the [REST API](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/createRoom). This behavior can be overridden to enable or disable captions on a per-room basis.

## Using Live Captions in a Meeting

Once live captions are enabled for a room, participants can activate them during the meeting:

1. **Activate Captions:** Click the **captions button** in the toolbar to enable live captions.
1. **Real-time Transcription:** Once activated, captions appear instantly at the bottom of the screen as participants speak—no additional configuration is required.
1. **Clear Visibility:** The interface is designed to be easy to read without blocking the video feed.
