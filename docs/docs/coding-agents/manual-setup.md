---
title: "Set up the OpenVidu docs MCP and skills by hand"
description: "Configure the OpenVidu documentation MCP server and the agent skills by hand in any MCP client, and keep that setup current without the plugin."
---

# Manual setup

Everything the [OpenVidu Agent Plugin](./agent-plugin.md) installs can be configured by hand instead. Use this page when your client doesn't load plugins yet, or when you would rather not install one.

The two kinds of component are independent here: the **MCP servers**, where the documentation comes from, and the **skills**, instructions the agent follows. Set up either, or both.

## MCP servers

| Name | Endpoint | Operated by |
| --- | --- | --- |
| `openvidu-docs` | `https://docs-mcp.openvidu.io/mcp` | OpenVidu |
| `livekit-docs` | `https://docs.livekit.io/mcp` | LiveKit |

Neither needs an account or an API key, and both speak Streamable HTTP. The examples below add `openvidu-docs`; to add `livekit-docs` too, repeat them with its name and URL.

!!! warning "Adding `livekit-docs`? Add the `openvidu-livekit-sdk-docs` skill too"

    It is what stops your agent answering deployment, configuration, edition or pricing questions from LiveKit's documentation, which is wrong about all of them for a self-hosted OpenVidu. Both servers have a `get_pricing_info` tool, and LiveKit's returns LiveKit Cloud plans. See [Why LiveKit's documentation is in the package](./agent-plugin.md#skills).

=== ":simple-claude:{.icon .lg-icon .tab-icon} Claude Code"

    ```bash
    claude mcp add --transport http openvidu-docs https://docs-mcp.openvidu.io/mcp
    ```

    Add `--scope project` to share it with your team through the repository's `.mcp.json`, or `--scope user` to have it in every project. `claude mcp list` shows whether it connected.

=== ":simple-claude:{.icon .lg-icon .tab-icon} Claude Desktop and claude.ai"

    In **Customize → Connectors**, select **+**, then **Add custom connector**, and paste the server URL:

    ```
    https://docs-mcp.openvidu.io/mcp
    ```

    On Team and Enterprise plans, an owner adds it for the whole organization, from **Organization settings → Connectors**.

=== ":simple-cursor:{.icon .lg-icon .tab-icon} Cursor"

    [Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=openvidu-docs&config=eyJ1cmwiOiJodHRwczovL2RvY3MtbWNwLm9wZW52aWR1LmlvL21jcCJ9){ .md-button }

    Or add it to `~/.cursor/mcp.json` (every project) or `.cursor/mcp.json` (this project):

    ```json
    {
      "mcpServers": {
        "openvidu-docs": {
          "url": "https://docs-mcp.openvidu.io/mcp"
        }
      }
    }
    ```

=== ":material-microsoft-visual-studio-code:{.icon .lg-icon .tab-icon} VS Code"

    ```bash
    code --add-mcp '{"name":"openvidu-docs","type":"http","url":"https://docs-mcp.openvidu.io/mcp"}'
    ```

    Or, for this workspace only, in `.vscode/mcp.json`:

    ```json
    {
      "servers": {
        "openvidu-docs": {
          "type": "http",
          "url": "https://docs-mcp.openvidu.io/mcp"
        }
      }
    }
    ```

=== ":simple-githubcopilot:{.icon .lg-icon .tab-icon} GitHub Copilot CLI"

    ```bash
    copilot mcp add --transport http openvidu-docs https://docs-mcp.openvidu.io/mcp
    ```

    It is saved in `~/.copilot/mcp-config.json`. A project can carry it instead in `.mcp.json` or `.github/mcp.json`.

=== ":fontawesome-brands-openai:{.icon .lg-icon .tab-icon} Codex"

    ```bash
    codex mcp add openvidu-docs --url https://docs-mcp.openvidu.io/mcp
    ```

    Or in `~/.codex/config.toml`:

    ```toml
    [mcp_servers.openvidu-docs]
    url = "https://docs-mcp.openvidu.io/mcp"
    ```

    In the IDE extension: the gear menu, **MCP servers → Add server**, with the **Streamable HTTP** type.

=== ":simple-googlegemini:{.icon .lg-icon .tab-icon} Gemini CLI"

    ```bash
    gemini mcp add --transport http -s user openvidu-docs https://docs-mcp.openvidu.io/mcp
    ```

    Leave out `-s user` to add it to the current project only. When editing `settings.json` by hand, the key is `httpUrl`: `url` means an SSE server there.

=== ":material-ghost-outline:{.icon .lg-icon .tab-icon} Kiro"

    [Add to Kiro :fontawesome-solid-external-link:{.external-link-icon}](https://kiro.dev/launch/mcp/add?name=openvidu-docs&config=%7B%22url%22%3A%22https%3A%2F%2Fdocs-mcp.openvidu.io%2Fmcp%22%7D){ .md-button target="_blank" }

    Or add it to `~/.kiro/settings/mcp.json` (every project) or `.kiro/settings/mcp.json` (this project):

    ```json
    {
      "mcpServers": {
        "openvidu-docs": {
          "url": "https://docs-mcp.openvidu.io/mcp"
        }
      }
    }
    ```

=== ":material-puzzle-outline:{.icon .lg-icon .tab-icon} Other clients"

    Any client that speaks MCP over Streamable HTTP works: it only needs the URL. The usual shape of the configuration file is:

    ```json
    {
      "mcpServers": {
        "openvidu-docs": {
          "type": "http",
          "url": "https://docs-mcp.openvidu.io/mcp"
        }
      }
    }
    ```

    Check your client's documentation for where that file lives, and whether it names the field `type`, `transport` or nothing at all. In Devin Desktop, for example, the command is `devin mcp add -s user openvidu-docs https://docs-mcp.openvidu.io/mcp`.

## Skills

A skill is a **directory**, with a `SKILL.md` and whatever it bundles, so installing one by hand means copying the whole directory, not just the file. The [`skills/` folder :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin/tree/main/skills){:target="_blank"} of the plugin repository holds one per skill: take all of them, or the ones you want.

Two rules, and they are the two things that go wrong:

- **Keep the directory name.** It must match the `name` in the skill's frontmatter, and clients skip a skill whose names differ without saying so.
- **Use a location your client scans.**

| Client | One project | Every project |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/`, `.cursor/skills/`, `.claude/skills/` | `~/.agents/skills/`, `~/.cursor/skills/`, `~/.claude/skills/` |
| VS Code and GitHub Copilot | `.github/skills/`, `.agents/skills/`, `.claude/skills/` | `~/.copilot/skills/`, `~/.agents/skills/`, `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/`, `.agents/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` |

Two locations stand out. `.claude/skills/` is the one project directory that Claude Code, Cursor and VS Code all read, which makes it the practical choice for a repository shared across a team. `.agents/skills/` is the vendor-neutral location the ecosystem is converging on: Cursor, VS Code, Codex and Gemini CLI read it, Claude Code and Kiro don't.

Claude Desktop and claude.ai don't read a folder on your disk: skills are enabled for your account, in their settings.

### Install them with the skills CLI

The [skills CLI :fontawesome-solid-external-link:{.external-link-icon}](https://skills.sh/){:target="_blank"} detects the coding agents on your machine and copies each skill to where that agent looks for it:

```bash
npx skills add OpenVidu/openvidu-agent-plugin
```

Add `-g` to install them for every project instead of the current one. `npx skills update` refreshes them later.

### Or copy them in

Clone the repository once:

```bash
git clone --depth 1 https://github.com/OpenVidu/openvidu-agent-plugin /tmp/openvidu-agent-plugin
```

Then copy the skills to a location from the table. For every project, in Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r /tmp/openvidu-agent-plugin/skills/. ~/.claude/skills/
```

For one project, shared with your team, copy them to the project-level location instead and commit the result, so every checkout brings the skills with it:

```bash
mkdir -p .claude/skills
cp -r /tmp/openvidu-agent-plugin/skills/. .claude/skills/
```

To take a single skill, copy its directory alone: `cp -r /tmp/openvidu-agent-plugin/skills/<skill-name> ~/.claude/skills/`. Delete the clone once you are done with it: `rm -rf /tmp/openvidu-agent-plugin`.

### Check they loaded

Claude Code lists them in `/skills`. In VS Code, type `/` in the chat, or run **Chat: Open Customizations** from the Command Palette. Elsewhere, each skill's name appears wherever your client lists what it has loaded.

### Clients without skills

A skill is only instructions, so you can do by hand what it would have done. For the version, edition and product, that means [writing them into your AGENTS.md](./agent-plugin.md#tell-your-agent-which-openvidu-you-run) once: your agent reads them in every session that follows.

## Keep a manual setup current

- **The MCP servers** need nothing from you. The endpoints are stable, and the documentation behind `openvidu-docs` is versioned per OpenVidu release, so there is no local copy to refresh.
- **The skills** are copies, and nothing tells you when the originals change. Run `npx skills update` if you installed them with the skills CLI, or repeat the copy. Or [install the plugin](./agent-plugin.md#install), and let your client keep them current.

## Markdown and llms.txt

For an assistant with no MCP support at all, every page of this site is also published as Markdown: add `index.md` to a page's URL, as in `https://openvidu.io/latest/docs/getting-started/index.md`. [`https://openvidu.io/llms.txt` :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/llms.txt){:target="_blank"} indexes them for the newest release, and each version has its own index at `https://openvidu.io/<version>/llms.txt`, following the [llms.txt :fontawesome-solid-external-link:{.external-link-icon}](https://llmstxt.org/){:target="_blank"} convention. Wherever it is available, the MCP server is still the better option: it searches, and it answers for the version you ask for.
