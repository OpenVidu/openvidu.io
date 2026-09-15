# Live Captions

OpenVidu Meet includes a built-in **Live Captions** feature that turns speech into text in real-time. This is a powerful tool for making your meetings more accessible to hearing-impaired participants, helping participants in noisy environments, and assisting non-native speakers.

## How to Enable Live Captions in OpenVidu Meet

Local Meet Deployment Limitation

Live Captions are **not available** in local Meet deployments. You must use either the [OpenVidu Local deployment](https://openvidu.io/3.8/docs/self-hosting/local/index.md) or an [OpenVidu production deployment](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md) to enable this feature.

### 1. Connect to your OpenVidu deployment

SSH into an OpenVidu Node and navigate to your OpenVidu deployment directory.

Depending on your [OpenVidu deployment type](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md):

**OpenVidu Local (Development)**

If you are using [OpenVidu Local (Development)](https://openvidu.io/3.8/docs/self-hosting/deployment-types/#openvidu-local-development), simply navigate to the configuration folder of the project:

```bash
# For OpenVidu Local COMMUNITY
cd openvidu-local-deployment/community

# For OpenVidu Local PRO
cd openvidu-local-deployment/pro
```

**OpenVidu Single Node**

If you are using [OpenVidu Single Node](https://openvidu.io/3.8/docs/self-hosting/deployment-types/#openvidu-single-node), SSH into the only OpenVidu node and navigate to:

```bash
cd /opt/openvidu/config
```

**OpenVidu Elastic**

If you are using [OpenVidu Elastic](https://openvidu.io/3.8/docs/self-hosting/deployment-types/#openvidu-elastic), SSH into the only Master Node and navigate to:

```bash
cd /opt/openvidu/config/cluster/media_node
```

**OpenVidu High Availability**

If you are using [OpenVidu High Availability](https://openvidu.io/3.8/docs/self-hosting/deployment-types/#openvidu-high-availability), SSH into any of your Master Nodes (doesn't matter which one) and navigate to:

```bash
cd /opt/openvidu/config/cluster/media_node
```

### 2. Enable the Speech Processing Agent

Modify file `agent-speech-processing.yaml` to enable the Live Captions Service with `processing: manual`:

```yaml
docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.8.0

enabled: true # (1)!

live_captions:
    processing: manual # (2)!
```

1. Set `enabled` to `true` to activate the Speech Processing Agent.
1. Set **processing** to `manual`; participants will activate captions on demand via a toolbar button.

Info

By default, the Speech Processing Agent uses a local Vosk model for speech-to-text transcription.

For a more advanced setup, consider using a cloud-based provider. See [Cloud providers](https://openvidu.io/3.8/docs/ai/live-captions/#cloud-providers) for more information.

Default language is English

The Speech Processing Agent uses **English** for speech-to-text transcription by default. To use a different language, you must configure a different Vosk model. See [Vosk models configuration](https://openvidu.io/3.8/docs/ai/live-captions/#vosk) for details on changing the language model.

### 3. Enable Captions in OpenVidu Meet configuration

Edit the `meet.env` file and ensure the following configuration variable is set:

```text
MEET_CAPTIONS_ENABLED=true
```

### 4. Restart OpenVidu

Apply your changes by restarting OpenVidu. This ensures the system recognizes the new live captioning capabilities.

Depending on your [OpenVidu deployment type](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md):

**OpenVidu Local (Development)**

Run where `docker-compose.yaml` is located:

```bash
docker compose restart
```

**OpenVidu Single Node**

Run this command in your node:

```bash
sudo systemctl restart openvidu
```

**OpenVidu Elastic**

Run this command in your Master Node:

```bash
sudo systemctl restart openvidu
```

**OpenVidu High Availability**

Run this command in one of your Master Nodes:

```bash
sudo systemctl restart openvidu
```

### 5. Enable/Disable Captions for specific Rooms

Captions are enabled by default when a room is [created](https://openvidu.io/3.8/meet/features/rooms/management/#create-rooms), whether through the UI or the [REST API](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/createRoom) . This behavior can be overridden to enable or disable captions on a per-room basis from the **Room Features** step of the room configuration wizard, using the **Captions** toggle.

Room wizard step enabling live captions for the room

## Using Live Captions in a Meeting

Once live captions are enabled for a room, any participant can turn them on during the meeting by clicking the **captions button** in the toolbar. Captions then appear instantly at the bottom of the screen as participants speak, with no additional configuration required. The interface is designed to be easy to read without blocking the video feed.
