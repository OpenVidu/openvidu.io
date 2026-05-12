# OpenVidu agents: overview

## Basic concepts

The modules that provide AI services in OpenVidu are called **OpenVidu agents**. They are **pre-configured and ready-to-use AI modules**. OpenVidu agents interact with your Rooms in real time using the powerful [LiveKit Agents framework](https://docs.livekit.io/agents/) .

All OpenVidu agents follow the following general principles:

- **Agents run in your OpenVidu nodes**: in [OpenVidu Single Node](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-single-node), agents run in the same node. In [OpenVidu Elastic](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-elastic) and [OpenVidu High Availability](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-high-availability), agents run in Media Nodes. They run as Docker containers, just like any other OpenVidu service.
- **Agents are configured through YAML files**: you just have to add a file `agent-AGENT_NAME.yaml` to the configuration folder of your OpenVidu deployment, and the agent will be automatically launched. This declarative approach makes agents easy to deploy, manage and scale.

In more detail, each OpenVidu agent adheres to the following principles:

- **Each agent is automatically deployed as a Docker container once per node**: once in the only node of an [OpenVidu Single Node](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-single-node) deployment, and once in each Media Node of [OpenVidu Elastic](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-elastic) and [OpenVidu High Availability](https://openvidu.io/3.5.0/docs/self-hosting/deployment-types/#openvidu-high-availability) deployments.
- **Each agent is downloaded in background during OpenVidu startup**: take into account that it might not be available immediately after OpenVidu starts, as it may take some time to download the agent image from the Docker registry.
- **Each agent is identified, configured and deployed declaratively via its own `agent-AGENT_NAME.yaml` file**: your OpenVidu deployment will detect agent YAML files and will automatically launch and configure them. **`AGENT_NAME`** must be a unique identifier per agent.
- **Each agent container of each node can process multiple Rooms simultaneously**: the limit is set by the node's hardware.
- **Each enabled agent remains always running**: this happens even when not processing any Rooms. This idle state may consume some resources, but ensures that agents are ready to process Rooms immediately.

## List of available OpenVidu agents

- **Speech Processing agent**: provides all the AI services related to transcribing audio speech to text and processing the results in various ways.

[List of provided AI services](https://openvidu.io/3.5.0/docs/ai/overview/#speech-processing-agent) [Enable the agent](https://openvidu.io/3.5.0/docs/ai/openvidu-agents/speech-processing-agent/index.md)

## Troubleshooting OpenVidu agents

Sometimes agents fail to process a Room. Sometimes they don't even start properly. This is usually due to some misconfiguration, such as incorrect credentials in the agent configuration.

The best way to troubleshoot a failing agent is to **check its logs**. To do so:

```bash
docker logs agent-AGENT_NAME
```

- You can search for the logs in your [Grafana dashboard](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/grafana-stack/index.md).

- Or SSH into the single OpeVidu node and check docker logs:

  ```bash
  docker logs agent-AGENT_NAME
  ```

- You can search for the logs in your [Grafana dashboard](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/grafana-stack/index.md).

- You can also SSH into the Media Node where the problematic agent is running and check docker logs:

  ```bash
  docker logs agent-AGENT_NAME
  ```

- You can search for the logs in your [Grafana dashboard](https://openvidu.io/3.5.0/docs/self-hosting/production-ready/observability/grafana-stack/index.md).

- You can also SSH into the Media Node where the problematic agent is running and check docker logs:

  ```bash
  docker logs agent-AGENT_NAME
  ```
