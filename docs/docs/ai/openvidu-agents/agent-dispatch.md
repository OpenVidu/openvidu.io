# OpenVidu agents dispatch

OpenVidu agents remain idle until they are dispatched to a Room. This **idle state** may consume some resources, but ensures agents are ready to process Rooms immediately. This is done to optimize resource usage and ensure that agents are only active when needed.

## Automatic agent dispatch

To configure automatic dispatch for an agent's AI service, set this property in your <code>agent-<strong>AGENT_NAME</strong>.yaml</code> file:

```yaml
AI_SERVICE:
    processing: automatic
```

!!! tip
    For example, for the [Live Captions](../live-captions.md) service:

    ```yaml
    live_captions:
        processing: automatic
    ```
    

Agents configured with `processing: automatic` in one of their AI services will immediately join new Rooms and will start processing media tracks as soon as possible. This _"as soon as possible"_ moment can vary depending on the type of agent, the AI service that is is providing, and its configuration.

!!! info "Automatic dispatch is useful when the same AI service needs to be present in all Rooms, at all times."

## Explicit agent dispatch

To configure explicit dispatch for an agent's AI service, set this property in your <code>agent-<strong>AGENT_NAME</strong>.yaml</code> file:

```yaml
AI_SERVICE:
    processing: manual
```

!!! tip
    For example, for the [Live Captions](../live-captions.md) service:

    ```yaml
    live_captions:
        processing: manual
    ```

Agents configured with `processing: manual` in their AI services will not join any Room automatically. Instead, the agent must be explicitly dispatched to the required Room at the required time.

!!! info "Explicit dispatch is useful when you need fine control over which Rooms the agent should process, and when."

There are 2 different ways to explicitly dispatch an agent to a specific Room:

### Dispatch via API

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    Using [LiveKit Node SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/server-sdk-js/){target="\_blank"}

    ```javascript
    import { AgentDispatchClient } from 'livekit-server-sdk';

    const OPENVIDU_URL = 'https://my-openvidu-host';
    const API_KEY = 'api-key';
    const API_SECRET = 'api-secret';

    const agentDispatchClient = new AgentDispatchClient(OPENVIDU_URL, API_KEY, API_SECRET);

    // create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    const dispatch = await agentDispatchClient.createDispatch('my-room', 'AGENT_NAME');

    console.log('Dispatch created:', dispatch);
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    Using [LiveKit Go SDK :fontawesome-solid-external-link:{.external-link-icon}](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2){target="\_blank"}

    ```go
    import (
        livekit "github.com/livekit/protocol/livekit"
        lksdk "github.com/livekit/server-sdk-go/v2"
    )

    const OPENVIDU_URL = "https://my-openvidu-host"
    const API_KEY = "api-key"
    const API_SECRET = "api-secret"

    dispatchClient := lksdk.NewAgentDispatchServiceClient(OPENVIDU_URL, API_KEY, API_SECRET)

    // create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    dispatchAgentRequest := &livekit.CreateAgentDispatchRequest{
        AgentName: "AGENT_NAME",
        Room:      "my-room",
    }
    dispatch, err := dispatchClient.CreateDispatch(context.Background(), dispatchAgentRequest)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Dispatch created: %v\n", dispatch)
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    Using [LiveKit Ruby SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-ruby){target="\_blank"}

    ```ruby
    require 'livekit'

    OPENVIDU_URL = "https://my-openvidu-host"
    API_KEY = "api-key"
    API_SECRET = "api-secret"

    agentDispatchClient = LiveKit::AgentDispatchServiceClient.new(
        OPENVIDU_URL,
        api_key: API_KEY,
        api_secret: API_SECRET
    )

    # create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    response = agentDispatchClient.create_dispatch(roomName, agent)
    if response.error
        puts "Error creating dispatch: #{response.error}"
    else
        dispatch = response.data
        puts "Dispatch created: #{dispatch}"
    end
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    Using [LiveKit Kotlin SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/server-sdk-kotlin){target="\_blank"}

    ```java
    import io.livekit.server.AgentDispatchServiceClient;
    import livekit.LivekitAgentDispatch.AgentDispatch;

    final String  OPENVIDU_URL = "https://my-openvidu-host";
    final String  API_KEY = "api-key";
    final String  API_SECRET = "api-secret";

    AgentDispatchServiceClient agentDispatchClient = AgentDispatchServiceClient.createClient(
        OPENVIDU_URL,
        API_KEY,
        API_SECRET
    );

    // create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    AgentDispatch dispatch = agentDispatchClient.createDispatch("my-room", "AGENT_NAME")
        .execute().body();

    System.out.println("Dispatch created: " + dispatch.getId());
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    Using [LiveKit Python SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/livekit/python-sdks){target="\_blank"}

    ```python
    from livekit.api import LiveKitAPI, CreateAgentDispatchRequest

    OPENVIDU_URL = "https://my-openvidu-host"
    API_KEY = "api-key"
    API_SECRET = "api-secret"

    lkapi = LiveKitAPI(
        url=OPENVIDU_URL, api_key=API_KEY, api_secret=API_SECRET
    )

    # create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    request = CreateAgentDispatchRequest(
        agent_name="AGENT_NAME",
        room="my-room",
    )
    dispatch = await lkapi.agent_dispatch.create_dispatch(request)

    print("Dispatch created:\n", dispatch)
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    Using [LiveKit .NET SDK :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/pabloFuente/livekit-server-sdk-dotnet){target="\_blank"}

    ```csharp
    using Livekit.Server.Sdk.Dotnet;

    const string OPENVIDU_URL = "https://my-openvidu-host";
    const string API_KEY = "api-key";
    const string API_SECRET = "api-secret";

    AgentDispatchServiceClient agentDispatchServiceClient = new AgentDispatchServiceClient(
        OPENVIDU_URL,
        API_KEY,
        API_SECRET
    );

    // create a dispatch request for an agent named "AGENT_NAME" to join "my-room"
    var agentDispatch = await agentDispatchServiceClient.CreateDispatch(new CreateAgentDispatchRequest
    {
        AgentName = "AGENT_NAME",
        Room = "my-room"
    });
    Console.Out.WriteLine("Dispatch created: " + agentDispatch.Id);
    ```

=== ":material-api:{.icon .lg-icon .tab-icon} Server API"

    If your backend technology does not have its own SDK, you have two different options:

    1. Consume the Agent Dispatch API directly:

        ```bash
        curl -X POST https://my-openvidu-host/twirp/livekit.AgentDispatchService/CreateDispatch \
             -H "Authorization: Bearer VALID_AUTHORIZATION_TOKEN" \
             -H "Content-Type: application/json" \
             -d '{"agent_name": "AGENT_NAME", "room": "my-room"}'
        ```

        > You need as `VALID_AUTHORIZATION_TOKEN` a token with `room` and `roomAdmin` permissions. Visit LiveKit docs: [Creating a token :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/get-started/authentication/#creating-a-token){target="\_blank"}

        <br>

    2. Use the [livekit-cli :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/cli/cli-setup/){target="\_blank"}:

        ```bash
        export LIVEKIT_URL=https://my-openvidu-host
        export LIVEKIT_API_KEY=api-key
        export LIVEKIT_API_SECRET=secret-key

        lk dispatch create \
            --agent-name AGENT_NAME \
            --room my-room
        ```

!!! note "Notes about the Agent Dispatch API"

    - The **`agent_name`** field must match the `AGENT_NAME` you used in the `agent-AGENT_NAME.yaml` file.
    - The **`room`** field must match the `room` where you want to dispatch the agent.

### Dispatch via a Participant connection

You can configure a Participant's token to trigger the dispatch of an agent right at the moment that Participant connects to a Room. This is very useful to dispatch an agent to a specific Room only when a specific Participant joins.

To create a Participant's token with Agent dispatch, you just need to include in the token the proper `RoomConfiguration` options, specifically the **`agents`** property. Visit [LiveKit docs :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/get-started/authentication/#room-configuration){target="\_blank"} to learn how.