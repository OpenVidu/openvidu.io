---
title: "OpenVidu Agent Plugin for AI coding agents"
description: "Give Claude Code, Cursor, VS Code, Codex and other coding agents the official OpenVidu docs for the version, edition and product you actually run."
---

# OpenVidu Agent Plugin

A coding agent writes OpenVidu code from whatever it memorised during training: an older release, an edition you don't have, sometimes LiveKit Cloud. The **OpenVidu Agent Plugin** replaces the guessing with the documentation itself. Install it once, and Claude Code, Cursor, VS Code, GitHub Copilot, Codex or Kiro search and read the official OpenVidu docs **for the deployment your project talks to**: the right version, edition and product.

<div class="grid cards" markdown>

-   :material-book-search-outline:{ .lg .middle } **OpenVidu documentation**

    ---

    This documentation, for every OpenVidu release from 3.4, searched and read page by page through an MCP server.

-   :material-code-braces:{ .lg .middle } **LiveKit SDK reference**

    ---

    LiveKit's own documentation server, for the depth of the client and server SDKs an OpenVidu Platform app imports.

-   :material-script-text-outline:{ .lg .middle } **Skills**

    ---

    Procedures your agent follows: find out which OpenVidu you run before answering, and know which documentation to trust for what.

</div>

The plugin is about building *with* OpenVidu. For the AI agents that join your rooms to transcribe or caption them, see [AI Services](../ai/overview.md).

## What is an agent plugin?

An agent plugin is a package that a coding agent installs in one step, bundling the pieces that extend it: **MCP servers**, which give it tools to call, and **skills**, instructions it loads when a task calls for them. The package format is the [Agent Plugins 1.0 specification :fontawesome-solid-external-link:{.external-link-icon}](https://agent-plugins.org/specification){:target="_blank"}, an open, vendor-neutral standard implemented by VS Code, Cursor, GitHub Copilot, Codex, Kiro and other clients. Claude Code has a plugin format of its own, and the OpenVidu Agent Plugin ships in both from the same repository, [OpenVidu/openvidu-agent-plugin :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin){:target="_blank"}.

## What's inside

### MCP servers

| Server | Endpoint | What it serves |
| --- | --- | --- |
| `openvidu-docs` | `https://docs-mcp.openvidu.io/mcp` | The OpenVidu Meet and OpenVidu Platform documentation, for every release from 3.4. Operated by OpenVidu. |
| `livekit-docs` | `https://docs.livekit.io/mcp` | LiveKit's documentation: the SDK reference, the Agents framework, SIP. Operated by LiveKit. |

Both speak Streamable HTTP and need no account or API key. You don't call their tools yourself: your agent does, when the conversation needs them. `openvidu-docs` has seven:

| Tool | What it does |
| --- | --- |
| `search_docs` | Searches the documentation. Handles word variants (*record* finds *recording*) and OpenVidu vocabulary (*auth* finds *authentication*). Up to five searches in one call, with results page by page. |
| `get_doc_page` | Returns the full content of a page, or of up to ten pages in one call. |
| `list_doc_sections` | The table of contents: an overview of the sections and how many pages each holds, then the pages of the one asked for. |
| `list_versions` | The documentation versions the server carries, and the one it uses by default. |
| `resolve_openvidu_version_edition_product` | How to find out which deployment a project talks to: version, edition and product. Also maps a LiveKit Server version to OpenVidu versions. |
| `get_changelog` | The release notes of a version, for OpenVidu Meet, OpenVidu Platform or both. |
| `get_pricing_info` | The [pricing](../../pricing.md) page: editions, plans and the cost model. |

Every tool takes an optional `version`. Documentation is published per minor release, so the version your deployment reports (`3.8.1`) is answered from that minor's documentation (`3.8`), and the answer says so; without a version, the server uses the newest it carries. A version it doesn't carry is an error that lists the ones it does, never a quiet answer for a different release.

### Skills

| Skill | What it does |
| --- | --- |
| `openvidu-version-edition-product` | Establishes which OpenVidu the project targets (version, edition and product) and writes it into `AGENTS.md` or `CLAUDE.md`, so it is settled once instead of every session. See [Tell your agent which OpenVidu you run](#tell-your-agent-which-openvidu-you-run). |
| `openvidu-livekit-sdk-docs` | Decides which server answers a question: LiveKit's for SDK surface, OpenVidu's for everything else, from deployment and configuration to editions, OpenVidu Meet and pricing. |

??? info "Why LiveKit's documentation is in the package"

    OpenVidu Platform is a fork of LiveKit, and your application imports the LiveKit client and server SDKs directly. LiveKit's documentation covers that SDK surface in far more depth than this one: the full API reference, the Agents framework, the WebRTC transport details. So the plugin configures **LiveKit's own public MCP server**, the same one LiveKit documents in [Coding agent support :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/intro/coding-agents/){:target="_blank"}. Your agent talks to LiveKit directly: nothing of LiveKit's is copied or served by OpenVidu, and the server's availability and terms are LiveKit's.

    Two caveats, both enforced by the `openvidu-livekit-sdk-docs` skill:

    - **OpenVidu's documentation wins on anything that is not SDK surface.** Deployment, configuration, editions, OpenVidu Meet, recording as OpenVidu ships it, observability and pricing come from `openvidu-docs`. Both servers have a `get_pricing_info` tool, and LiveKit's returns LiveKit Cloud plans, which have nothing to do with a self-hosted OpenVidu.
    - **LiveKit's documentation is not versioned.** It describes LiveKit's latest release, while your deployment runs the LiveKit version its OpenVidu release bundles. Client SDK surface generally applies as written; server behaviour, such as new configuration flags or webhook fields, may not exist in your version yet.

    If you would rather not use it, remove `livekit-docs` from your client's MCP configuration. Nothing else in the plugin depends on it.

## Install

!!! info "Update your client first"

    The Agent Plugins specification was published in August 2026, so support for it is recent in every client. If a step below does nothing, update your client before assuming something is broken.

=== ":simple-claude:{.icon .lg-icon .tab-icon} Claude Code"

    Add the OpenVidu marketplace and install the plugin from it:

    ```
    /plugin marketplace add OpenVidu/openvidu-agent-plugin
    /plugin install openvidu@openvidu
    ```

    From a shell, the same two steps are `claude plugin marketplace add OpenVidu/openvidu-agent-plugin` and `claude plugin install openvidu@openvidu`. Add `--scope project` to the second one to share the plugin with your team through the repository.

    `/plugin` lists the plugin as enabled, and its **Errors** tab is where a failed MCP connection shows up.

    **Updates.** Claude Code updates plugins automatically only from Anthropic's own marketplaces. Turn automatic updates on for this one in `/plugin` → **Marketplaces** → `openvidu` → **Enable auto-update**, and Claude Code looks for a new version shortly after each session starts; `/reload-plugins` applies it to a running session. Otherwise, update by hand with `claude plugin update openvidu@openvidu`, or **Update now** in `/plugin` → **Installed**.

=== ":material-microsoft-visual-studio-code:{.icon .lg-icon .tab-icon} VS Code"

    Run **Chat: Install Plugin From Source** from the Command Palette, and paste the repository URL:

    ```
    https://github.com/OpenVidu/openvidu-agent-plugin
    ```

    Agent plugins are enabled by default (the `chat.plugins.enabled` setting), but an organization policy can turn them off.

    **Updates.** Run **Extensions: Check for Extension Updates** from the Command Palette, or let VS Code check every 24 hours by enabling `extensions.autoUpdate`, the same setting that governs extension updates.

=== ":simple-cursor:{.icon .lg-icon .tab-icon} Cursor"

    Clone the repository into Cursor's local plugin folder, then restart Cursor or run **Developer: Reload Window**:

    ```bash
    git clone https://github.com/OpenVidu/openvidu-agent-plugin ~/.cursor/plugins/local/openvidu
    ```

    On Teams and Enterprise plans, an admin can import the repository as a team marketplace instead, from **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo**. Members then install it from **Customize** in the sidebar.

    **Updates.** A local clone never updates on its own: `git pull` it and reload the window. A team marketplace updates on its own only if an admin turned on **Enable Auto Refresh** in its settings, which picks up a new version within about ten minutes; otherwise an admin selects **Refresh**.

=== ":simple-githubcopilot:{.icon .lg-icon .tab-icon} GitHub Copilot CLI"

    ```bash
    copilot plugin install OpenVidu/openvidu-agent-plugin
    ```

    Inside a session, `/plugin install OpenVidu/openvidu-agent-plugin` does the same.

    **Updates.** `copilot plugin update openvidu`, or `copilot plugin update --all` for every plugin installed.

=== ":fontawesome-brands-openai:{.icon .lg-icon .tab-icon} Codex"

    In the Codex CLI, add the repository as a marketplace and install the plugin from it:

    ```bash
    codex plugin marketplace add OpenVidu/openvidu-agent-plugin
    codex plugin add openvidu@openvidu
    ```

    Or find it with `/plugins` inside a session. The Codex IDE extension doesn't load plugins: there, [configure the server by hand](./manual-setup.md#mcp-servers).

    **Updates.** `codex plugin marketplace upgrade openvidu` fetches the latest version and reinstalls the plugin.

=== ":material-ghost-outline:{.icon .lg-icon .tab-icon} Kiro"

    Kiro installs plugins as powers. In the **Powers** panel, choose **Add Custom Power → Import power from GitHub**, paste the repository URL and select **Install**:

    ```
    https://github.com/OpenVidu/openvidu-agent-plugin
    ```

    **Updates.** Select the power in the **Powers** panel, then **Check for updates** and **Install updates**.

=== ":material-puzzle-outline:{.icon .lg-icon .tab-icon} Other clients"

    Any client that implements Agent Plugins can install the plugin from the repository, `https://github.com/OpenVidu/openvidu-agent-plugin`, or from a local clone of it: the [compatible clients list :fontawesome-solid-external-link:{.external-link-icon}](https://agent-plugins.org/compatible-clients){:target="_blank"} links each one's instructions. Clients that read Claude Code plugins can install it too, such as Devin Desktop with `devin plugins install OpenVidu/openvidu-agent-plugin`.

    **Updates.** Use the client's own update command, or pull the repository again and reload the client.

Your client isn't here, or you would rather not install a plugin? The same MCP servers and skills can be [configured by hand](./manual-setup.md).

## Tell your agent which OpenVidu you run

Every answer depends on three facts that nothing outside your project can see:

- **Version**: the documentation differs between releases.
- **Edition**: COMMUNITY or PRO. PRO has features that COMMUNITY does not.
- **Product**: [OpenVidu Platform](../index.md), where your app uses the LiveKit SDKs, or [OpenVidu Meet](../../meet/index.md), where it uses Meet's REST API and the `<openvidu-meet>` web component. Two different APIs.

Ask your agent to work them out. The `openvidu-version-edition-product` skill follows the procedure the documentation server gives it: read them from the deployment itself, ask you before contacting a remote host, and never read a credential's value. Then it offers to write them down, so no later session repeats the work:

```markdown title="AGENTS.md"
This project connects to an OpenVidu 3.8.0 PRO deployment, using OpenVidu Meet.
When querying the OpenVidu documentation MCP, always pass version="3.8.0",
and read the answers for that edition and product.
```

The same lines work in `CLAUDE.md`, and without the skill installed you can write them yourself. Facts only: never put a credential in that file.

!!! warning "Don't read the version off your dependencies"

    `livekit-client`, `livekit-server-sdk` and the OpenVidu Meet web component are client SDKs. Their version numbers bear no relation to your OpenVidu deployment's, and say nothing about its edition.

## Try it

- "Using the OpenVidu docs, how do I record a room with individual tracks?"
- "What does the OpenVidu documentation say about deploying with fault tolerance? We're on 3.8.0."
- "Check the OpenVidu docs before answering: does the Egress service need S3 credentials, and how are they configured?"
- "Work out which OpenVidu version, edition and product this project uses, and write them into AGENTS.md."
- "Our LiveKit server reports 1.9.8. Which OpenVidu version is that?"

To check that the documentation server answers, ask your agent to list the OpenVidu documentation versions, or call it yourself. You should get the seven tools above:

```bash
curl -s -X POST https://docs-mcp.openvidu.io/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Troubleshooting

??? question "The plugin installed, but no OpenVidu tools appear"

    Reload or restart the client, and check that the plugin is enabled. In Claude Code, `/plugin` lists it, and its **Errors** tab shows a failed MCP connection. If your client is up to date and still shows no tools, [add the server by hand](./manual-setup.md#mcp-servers).

??? question "A skill never activates"

    A skill loads when your request matches its description, so name OpenVidu in the request. If you copied the skills by hand, the directory name must equal the `name` in the skill's frontmatter, and the directory must be in a location your client scans: see [Skills](./manual-setup.md#skills). A skill whose work is already done, such as a version already pinned in `AGENTS.md`, also stays quiet.

??? question "The client shows the server as failed or offline"

    The transport must be HTTP (Streamable HTTP), not `sse` or `stdio`, and the URL must end in `/mcp`.

??? question "Opening the server URL in a browser gives an error"

    That is expected: the server only accepts `POST` requests and answers `405` to anything else. It is not a web page, and for the same reason a browser-based MCP client cannot use it.

??? question "The answers are for the wrong version"

    Pin the version in `AGENTS.md` or `CLAUDE.md` as shown in [Tell your agent which OpenVidu you run](#tell-your-agent-which-openvidu-you-run), or name it in your prompt. Ask your agent to list the documentation versions to see which ones the server carries.

??? question "A page you know exists isn't found"

    The server is rebuilt when this documentation is published, not continuously, so a page published minutes ago may not be there yet.

Problems with the plugin itself can be reported in the [openvidu-agent-plugin repository :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin/issues){:target="_blank"}.
