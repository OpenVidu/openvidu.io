# OpenVidu agents: overview

## Basic concepts

The modules that provide AI services in OpenVidu are called **OpenVidu agents**. They are **pre-configured and ready-to-use AI modules**. OpenVidu agents interact with your Rooms in real time using the powerful [LiveKit Agents framework](https://docs.livekit.io/agents/){target="\_blank"}.

All OpenVidu agents follow the following general principles:

- **Agents run in your OpenVidu nodes**: in [OpenVidu Single Node](../../self-hosting/deployment-types.md#openvidu-single-node), agents run in the same node. In [OpenVidu Elastic](../../self-hosting/deployment-types.md#openvidu-elastic) and [OpenVidu High Availability](../../self-hosting/deployment-types.md#openvidu-high-availability), agents run in Media Nodes. They run as Docker containers, just like any other OpenVidu service.
- **Agents are configured through YAML files**: you just have to add a file <code>agent-<strong>AGENT_NAME</strong>.yaml</code> to the configuration folder of your OpenVidu deployment, and the agent will be automatically launched. This declarative approach makes agents easy to deploy, manage and scale.

!!! note "In more detail, each OpenVidu agent adheres to the following principles:"

    - **Each agent is automatically deployed as a Docker container once per node**: once in the only node of an [OpenVidu Single Node](../../self-hosting/deployment-types.md#openvidu-single-node) deployment, and once in each Media Node of [OpenVidu Elastic](../../self-hosting/deployment-types.md#openvidu-elastic) and [OpenVidu High Availability](../../self-hosting/deployment-types.md#openvidu-high-availability) deployments.
    - **Each agent is downloaded in background during OpenVidu startup**: take into account that it might not be available immediately after OpenVidu starts, as it may take some time to download the agent image from the Docker registry.
    - **Each agent is identified, configured and deployed declaratively via its own `agent-AGENT_NAME.yaml` file**: your OpenVidu deployment will detect agent YAML files and will automatically launch and configure them. **`AGENT_NAME`** must be a unique identifier per agent.
    - **Each agent container of each node can process multiple Rooms simultaneously**: the limit is set by the node's hardware.
    - **Each enabled agent remains always running**: this happens even when not processing any Rooms. This idle state may consume some resources, but ensures that agents are ready to process Rooms immediately.

## List of available OpenVidu agents

- **Speech Processing agent**: provides all the AI services related to transcribing audio speech to text and processing the results in various ways.

[:octicons-arrow-right-24: List of provided AI services](../overview.md#speech-processing-agent){.ai-agent-link}
[:octicons-arrow-right-24: Enable the agent](../speech-processing/enabling-agent.md){.ai-agent-link}

## Troubleshooting OpenVidu agents

Sometimes agents fail to process a Room. Sometimes they don't even start properly. This is usually due to some misconfiguration, such as incorrect credentials in the agent configuration.

The best way to troubleshoot a failing agent is to **check its logs**. To do so:

=== "OpenVidu Local (Development)"

    ```bash
    docker logs agent-AGENT_NAME
    ```

=== "OpenVidu Single Node"

    - You can search for the logs in your [Grafana dashboard](../../self-hosting/production-ready/observability/grafana-stack.md).

    - Or SSH into the single OpeVidu node and check docker logs:

        ```bash
        docker logs agent-AGENT_NAME
        ```

=== "OpenVidu Elastic"

    - You can search for the logs in your [Grafana dashboard](../../self-hosting/production-ready/observability/grafana-stack.md).

    - You can also SSH into the Media Node where the problematic agent is running and check docker logs:

        ```bash
        docker logs agent-AGENT_NAME
        ```

=== "OpenVidu High Availability"

    - You can search for the logs in your [Grafana dashboard](../../self-hosting/production-ready/observability/grafana-stack.md).

    - You can also SSH into the Media Node where the problematic agent is running and check docker logs:

        ```bash
        docker logs agent-AGENT_NAME
        ```
