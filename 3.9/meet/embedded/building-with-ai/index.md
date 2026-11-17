# Embed OpenVidu Meet with an AI coding agent

An AI coding agent can do most of the work of embedding OpenVidu Meet: creating rooms from your backend, placing the `<openvidu-meet>` web component in your frontend, reacting to webhooks. The **OpenVidu Agent Plugin** helps it get that code right: it gives your agent the [REST API](https://openvidu.io/latest/meet/embedded/reference/rest-api/index.md), [web component](https://openvidu.io/latest/meet/embedded/reference/webcomponent/index.md) and [webhooks](https://openvidu.io/latest/meet/embedded/reference/webhooks/index.md) references for the OpenVidu version and edition you run, so the code it writes is up to date and accurate.

[Install the OpenVidu Agent Plugin](https://openvidu.io/latest/docs/building-with-ai/agent-plugin/#install)

## Try it

- "Add a backend endpoint that creates an OpenVidu Meet room and returns the URL our frontend passes to the web component."
- "Embed the `<openvidu-meet>` web component in our React page, and show our own screen when the participant leaves the meeting."
- "Which OpenVidu Meet webhook tells us a recording is ready, and what does its payload carry?"
- "Work out which OpenVidu version and edition this project connects to, and write them into AGENTS.md."

For a complete application built this way, see [Building a video-enabled CRM with an AI agent](https://openvidu.io/blog/2026/07/21/building-a-video-enabled-crm-with-an-ai-agent/index.md): a CRM with embedded OpenVidu Meet meetings, from an empty folder to per-guest room permissions in seven prompts.

## Learn more

The plugin serves OpenVidu Meet and OpenVidu Platform alike, so it is documented in the OpenVidu Platform section:

- [OpenVidu Agent Plugin](https://openvidu.io/latest/docs/building-with-ai/agent-plugin/index.md): what it is, and how to install and update it in each coding agent.
- [OpenVidu MCP servers](https://openvidu.io/latest/docs/building-with-ai/mcp-servers/index.md): the documentation server on its own, for clients that don't load plugins.
- [OpenVidu skills](https://openvidu.io/latest/docs/building-with-ai/skills/index.md): the skills on their own.
