# Custom agents

OpenVidu provides a [set of built-in agents](./openvidu-agents/overview.md#list-of-available-openvidu-agents), each one offering a set of AI services to help enhance the user experience in your Rooms. But you can also create **your own custom agents** to fine-tune the AI capabilities of your OpenVidu application. You can do so using the powerful [LiveKit Agents framework :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/agents/){target="\_blank"}.

## 1. Implement your custom agent using the LiveKit Agents framework

LiveKit Agents consists of a **Python** or **Node** program that connects to LiveKit Rooms to perform some kind of AI pipeline over the media tracks published to the Room by regular Participants.

The agent actually behaves as any other regular Participant of the Room, but thanks to its connection to **Speech-to-Text** services, **LLMs** and **Text-to-Speech** service, it can transcribe audio tracks, analyze video tracks, generate speech, etc... and publish the results back to the Room. This allows building any kind of flow interaction between your users and the AI service, all in real-time.

An incredible set of [plugins :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/agents/tree/main/livekit-plugins){target="\_blank"} make it very easy to integrate your agent code with the most popular AI providers. You have further information in the [LiveKit Agents integrations :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/agents/integrations/){target="\_blank"} documentation.

!!! tip
    To start building your own custom agent, the best way is to follow the LiveKit's [Voice AI quickstart :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/agents/start/voice-ai/){target="\_blank"} guide. You can customize it to your needs once you grasp the basics of the Agents framework. You also have a great collection of [recipes :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/recipes/){target="\_blank"} to inspire you.

## 2. Dockerize your custom agent

Once you are satisfied with your custom agent implementation, you need to build a **Docker image** of it. When using the Python SDK and having a project structure similar to this...

```
.
├── agent.py
├── requirements.txt
└── Dockerfile
```

...here you have a typical example of an agent's Dockerfile:

```dockerfile
# This is an example Dockerfile that builds a minimal container for running LK Agents
# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11.11
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# Install gcc, g++ and other build dependencies.
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

USER appuser

RUN mkdir -p /home/appuser/.cache
RUN chown -R appuser /home/appuser/.cache

WORKDIR /home/appuser

COPY requirements.txt .
RUN python -m pip install --user --no-cache-dir -r requirements.txt

COPY ./*.py .

# ensure that any dependent models are downloaded at build-time
RUN python agent.py download-files

# Run the application.
CMD ["python", "agent.py", "start"]
```

## 3. Add your custom agent to your OpenVidu deployment

### 1. SSH into an OpenVidu Node and go to configuration folder

--8<-- "shared/self-hosting/ssh-openvidu-deployment.md"

### 2. Add a `agent-AGENT_NAME.yaml` file

Located in the [configuration folder](#1-ssh-into-an-openvidu-node-and-go-to-configuration-folder) of your OpenVidu node, create a file named `agent-AGENT_NAME.yaml`, where `AGENT_NAME` must be a unique name for your agent. The minimal content of this file is:

```yaml
# Docker image of the agent.
docker_image: YOUR_IMAGE

# Whether to run the agent or not.
enabled: true

CUSTOM_CONFIGURATION: ...
```

- The `docker_image` field must be the full name of the Docker image you built in [step 2](#2-dockerize-your-custom-agent). Of course, your OpenVidu nodes must have access to that Docker image's registry.

- The `enabled` field indicates whether the agent will be started by OpenVidu or not. Setting this to `false` will result in your agent NOT being launched and not being available, even if you later try to [manually dispatch](./openvidu-agents/agent-dispatch.md#explicit-agent-dispatch) your agent.

- You can add as many other properties as you want to this YAML file. You can access them within your agent's code (see [Accessing the agent's configuration file](#accessing-the-agents-configuration-file)).

### 3. Restart OpenVidu

Depending on your [OpenVidu deployment type](../self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

    Run where `docker-compose.yaml` is located:

    ```bash
    docker compose restart
    ```

=== "OpenVidu Single Node"

    Run this command in your node:

    ```bash
    sudo systemctl restart openvidu
    ```

=== "OpenVidu Elastic"

    Run this command in your Master Node:

    ```bash
    sudo systemctl restart openvidu
    ```

=== "OpenVidu High Availability"

    Run this command in one of your Master Nodes:

    ```bash
    sudo systemctl restart openvidu
    ```

After restarting OpenVidu your agent will be up and running, ready to process new Rooms.

!!! warning

    If your agent container keeps restarting, there might be an error in your configuration. Check its logs to find out what is wrong.

## Tips when coding your custom agent

When developing your custom agent using the Python or Node SDKs, there are some tips that can help:

### Dispatching your custom agent

You can control when to dispatch your agent in your agent's code. By default, agents will dispatch (connect) automatically to new Rooms. If you want to manually control when to dispatch your agent, simply add property `agent_name` to your `WorkerOptions` when creating the agent:

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    ```python
    opts = WorkerOptions(
        ...
        agent_name="my-custom-agent",
    )
    ```

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    ```javascript
    const opts = new WorkerOptions({
      ...
      agentName: "my-custom-agent",
    });
    ```

!!! note "Property `agent_name` must match the value `AGENT_NAME` in the file <code>agent-<strong>AGENT_NAME</strong>.yaml</code> created [here](#2-add-an-agent-agent_nameyaml-file)."

Then you can manually dispatch your agent using the [Dispatch API](./openvidu-agents/agent-dispatch.md#dispatch-via-api) or via a [Participant connection](./openvidu-agents/agent-dispatch.md#dispatch-via-a-participant-connection).

<!-- ### Env vars available for your custom agent

You can access the following useful environment variables from within your agent's code:

- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`

!!! tip
    These env vars are especially useful when creating your `WorkerOptions`, as they are required to connect your agent to your OpenVidu deployment. -->

### Accessing the agent's configuration file

It can be very useful to access your agent's YAML configuration file from within your agent's code. OpenVidu automatically mounts file `agent-AGENT_NAME.yaml` for your agent's Docker container. You have the path to the file in env var `AGENT_CONFIG_FILE`. You can read the file's content directly in your agent's code (a YAML parser can be very useful). For example:

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    ```python
    import os
    import yaml

    with open(os.environ["AGENT_CONFIG_FILE"], "r") as f:
        config = yaml.safe_load(f)

    print(config)
    ```

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    ```javascript
    import fs from 'fs';
    import yaml from 'js-yaml';

    const configFile = process.env.AGENT_CONFIG_FILE;
    const config = yaml.load(fs.readFileSync(configFile, 'utf8'));

    console.log(config);
    ```


## Elasticity and graceful shutdowns

Custom agents in multi-node OpenVidu deployments ([OpenVidu Elastic](../self-hosting/deployment-types.md#openvidu-elastic) and [OpenVidu High Availability](../self-hosting/deployment-types.md#openvidu-high-availability)) support automatic graceful shutdowns when Media Nodes are scaled down.

When a Media Node hosting custom agents is being removed from the OpenVidu cluster:

1. **Existing jobs complete**: Custom agents are allowed to finish processing their current jobs before stopping.
2. **New jobs rejected**: Custom agents reject new job requests, which will be redirected to other Media Nodes in the cluster.

This ensures no interruptions in the services provided by your custom agents when your OpenVidu cluster scales down.
