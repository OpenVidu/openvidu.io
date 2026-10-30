---
title: "OpenVidu Agent Plugin for AI coding agents"
description: "Install the OpenVidu Agent Plugin in Claude Code, Cursor, VS Code, GitHub Copilot, Codex or Kiro to build with the official OpenVidu documentation."
---

# OpenVidu Agent Plugin

The **OpenVidu Agent Plugin** brings the official OpenVidu documentation into your AI coding agent. Install it once in Claude Code, Cursor, VS Code, GitHub Copilot, Codex or Kiro, and your agent reads the documentation for the OpenVidu version, edition and product your project uses, so the code it writes is up to date and accurate.

<div class="grid cards" markdown>

-   :material-book-search-outline:{ .lg .middle } **OpenVidu MCP servers**

    ---

    The OpenVidu Meet and OpenVidu Platform documentation of every release from 3.4, for your agent to search and read.

    [:octicons-arrow-right-24: OpenVidu MCP servers](mcp-servers.md)

-   :material-script-text-outline:{ .lg .middle } **OpenVidu skills**

    ---

    Procedures your agent follows, such as finding out which OpenVidu your project uses when an answer depends on it.

    [:octicons-arrow-right-24: OpenVidu skills](skills.md)

</div>

## What is an agent plugin?

An agent plugin is a package that a coding agent installs in one step, bundling MCP servers and skills. Its format is the [Agent Plugins specification :fontawesome-solid-external-link:{.external-link-icon}](https://agent-plugins.org/specification){:target="_blank"}, an open standard implemented by VS Code, Cursor, GitHub Copilot, Codex, Kiro and other clients. Claude Code has a format of its own, and the OpenVidu Agent Plugin ships in both from [OpenVidu/openvidu-agent-plugin :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin){:target="_blank"}.

The plugin helps you build *with* OpenVidu. To add AI agents to your rooms, see [AI Services](../ai/overview.md).

## Install

Support for agent plugins is recent in every client: if a step below does nothing, update your client first.

=== ":simple-claude:{.icon .lg-icon .tab-icon} Claude Code"

    ```
    /plugin marketplace add OpenVidu/openvidu-agent-plugin
    /plugin install openvidu@openvidu
    ```

    From a shell: `claude plugin marketplace add OpenVidu/openvidu-agent-plugin` and `claude plugin install openvidu@openvidu`. Add `--scope project` to the second one to share the plugin with your team through the repository.

    **Updates.** Turn them on in `/plugin` → **Marketplaces** → `openvidu` → **Enable auto-update**, or run `claude plugin update openvidu@openvidu`.

=== ":material-microsoft-visual-studio-code:{.icon .lg-icon .tab-icon} VS Code"

    Run **Chat: Install Plugin From Source** from the Command Palette, and paste the repository URL:

    ```
    https://github.com/OpenVidu/openvidu-agent-plugin
    ```

    **Updates.** Run **Extensions: Check for Extension Updates**, or enable `extensions.autoUpdate` to check every 24 hours.

=== ":simple-cursor:{.icon .lg-icon .tab-icon} Cursor"

    Clone the repository into Cursor's local plugin folder, then run **Developer: Reload Window**:

    ```bash
    git clone https://github.com/OpenVidu/openvidu-agent-plugin ~/.cursor/plugins/local/openvidu
    ```

    On Teams and Enterprise plans, an admin can import the repository as a team marketplace instead, from **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo**.

    **Updates.** `git pull` the clone and reload the window. A team marketplace updates on its own if an admin enables **Enable Auto Refresh**.

=== ":simple-githubcopilot:{.icon .lg-icon .tab-icon} GitHub Copilot CLI"

    ```bash
    copilot plugin install OpenVidu/openvidu-agent-plugin
    ```

    **Updates.** `copilot plugin update openvidu`.

=== ":fontawesome-brands-openai:{.icon .lg-icon .tab-icon} Codex"

    ```bash
    codex plugin marketplace add OpenVidu/openvidu-agent-plugin
    codex plugin add openvidu@openvidu
    ```

    The Codex IDE extension doesn't load plugins: there, [add the MCP server](mcp-servers.md#add-it-to-your-client).

    **Updates.** `codex plugin marketplace upgrade openvidu`.

=== ":material-ghost-outline:{.icon .lg-icon .tab-icon} Kiro"

    Kiro installs plugins as powers. In the **Powers** panel, choose **Add Custom Power → Import power from GitHub**, paste the repository URL and select **Install**:

    ```
    https://github.com/OpenVidu/openvidu-agent-plugin
    ```

    **Updates.** Select the power, then **Check for updates**.

=== ":material-puzzle-outline:{.icon .lg-icon .tab-icon} Other clients"

    Any client that implements Agent Plugins installs it from `https://github.com/OpenVidu/openvidu-agent-plugin`: the [compatible clients list :fontawesome-solid-external-link:{.external-link-icon}](https://agent-plugins.org/compatible-clients){:target="_blank"} links each one's instructions. Clients that read Claude Code plugins can install it too, such as Devin Desktop with `devin plugins install OpenVidu/openvidu-agent-plugin`.

    **Updates.** Use the client's own update command.

Your client doesn't load plugins, or you would rather not install one? Add the [MCP server](mcp-servers.md#add-it-to-your-client) and the [skills](skills.md#install) on their own.

## Tell your agent which OpenVidu you run

Many answers depend on three facts about the deployment your project talks to: its **version**, its **edition** (COMMUNITY or PRO) and the **product** your app uses, [OpenVidu Platform](../index.md) or [OpenVidu Meet](../../meet/index.md). When an answer needs them, your agent works them out with the [`openvidu-version-edition-product`](skills.md#available-skills) skill and offers to write them into `AGENTS.md`, so later sessions start from them. You can also write them yourself:

```markdown title="AGENTS.md"
This project connects to an OpenVidu 3.9.0 pro deployment, using OpenVidu Meet.
When querying the OpenVidu documentation MCP, always pass version="3.9.0",
and read the answers for that edition and product.
```

The same lines work in `CLAUDE.md`. Write facts only, never a credential, and don't take the version from your dependencies: `livekit-client`, `livekit-server-sdk` and the OpenVidu Meet web component are versioned independently of OpenVidu.

## Try it

Ask as you would about any other code, and your agent reads the documentation when the task needs it:

- "How do I record a room with individual tracks in OpenVidu?"
- "We're on OpenVidu 3.9.0. How do I deploy it with fault tolerance?"
- "Does the OpenVidu Egress service need S3 credentials, and how are they configured?"
- "In our OpenVidu app, how do I send a data message to a single participant with livekit-client?"
- "Our LiveKit server reports 1.9.8. Which OpenVidu version is that?"
- "Work out which OpenVidu version, edition and product this project uses, and write them into AGENTS.md."

## Privacy

The plugin collects nothing itself. The documentation server it connects to records each request your agent makes, never your code or your conversation: see [what it records and for how long](mcp-servers.md#privacy).

## Troubleshooting

??? question "No OpenVidu tools appear after installing"

    Reload or restart the client, and check that the plugin is enabled. In Claude Code, `/plugin` lists it, and its **Errors** tab shows a failed MCP connection. If your client is up to date and still shows no tools, [add the server by hand](mcp-servers.md#add-it-to-your-client).

??? question "The answers are for the wrong version"

    Pin the version in `AGENTS.md`, as in [Tell your agent which OpenVidu you run](#tell-your-agent-which-openvidu-you-run), or name it in your prompt.

More in the troubleshooting of the [MCP server](mcp-servers.md#troubleshooting) and the [skills](skills.md#troubleshooting). Problems with the plugin itself can be reported in the [openvidu-agent-plugin repository :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin/issues){:target="_blank"}.
