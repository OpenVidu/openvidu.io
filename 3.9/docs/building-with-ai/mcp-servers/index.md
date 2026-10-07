# OpenVidu MCP servers

An MCP server gives a coding agent tools it can call. OpenVidu provides the documentation server below, included in the [OpenVidu Agent Plugin](https://openvidu.io/3.9/docs/building-with-ai/agent-plugin/index.md). Add it on its own when your client doesn't load plugins, or when you would rather not install one.

## OpenVidu documentation server

- **Name**: `openvidu-docs`
- **URL**: `https://docs-mcp.openvidu.io/mcp`
- **Transport**: Streamable HTTP, with no account or API key

It searches and reads the OpenVidu Meet and OpenVidu Platform documentation of every release from 3.4, and points your agent to LiveKit's documentation when it needs more, such as the SDK references. Your agent calls its tools when a task needs them:

| Tool                                       | What it does                                                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `search_docs`                              | Searches the documentation, linking each result to the section that matched.                                               |
| `get_doc_page`                             | Reads one or more pages, whole or a section at a time.                                                                     |
| `list_doc_sections`                        | Lists the documentation's sections and their pages.                                                                        |
| `list_versions`                            | Lists the documentation versions, and the one used by default.                                                             |
| `resolve_openvidu_version_edition_product` | Explains how to find out the version, edition and product a project uses, and maps a LiveKit Server version to OpenVidu's. |
| `get_changelog`                            | Returns the release notes of a version.                                                                                    |
| `get_pricing_info`                         | Returns the editions, plans and [pricing](https://openvidu.io/3.9/pricing/index.md).                                       |

The tools that read the documentation take the version your deployment reports (`3.9.1`) and answer from that release's documentation (`3.9`); without one, they use the latest. A version the server doesn't carry is an error, never an answer for another release. There is nothing to update on your side: the server is rebuilt each time this documentation is published.

### Add it to your client

**Claude Code**

```bash
claude mcp add --transport http openvidu-docs https://docs-mcp.openvidu.io/mcp
```

Add `--scope project` to share it with your team through the repository's `.mcp.json`, or `--scope user` to have it in every project.

**Claude Desktop and claude.ai**

In **Customize → Connectors**, select **+**, then **Add custom connector**, and paste the server URL:

```text
https://docs-mcp.openvidu.io/mcp
```

On Team and Enterprise plans, an owner adds it for the whole organization, from **Organization settings → Connectors**.

**Cursor**

[Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=openvidu-docs&config=eyJ1cmwiOiJodHRwczovL2RvY3MtbWNwLm9wZW52aWR1LmlvL21jcCJ9)

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

**VS Code**

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

**GitHub Copilot CLI**

```bash
copilot mcp add --transport http openvidu-docs https://docs-mcp.openvidu.io/mcp
```

**Codex**

```bash
codex mcp add openvidu-docs --url https://docs-mcp.openvidu.io/mcp
```

In the IDE extension: the gear menu, **MCP servers → Add server**, with the **Streamable HTTP** type.

**Gemini CLI**

```bash
gemini mcp add --transport http -s user openvidu-docs https://docs-mcp.openvidu.io/mcp
```

Leave out `-s user` to add it to the current project only.

**Kiro**

[Add to Kiro](https://kiro.dev/launch/mcp/add?name=openvidu-docs&config=%7B%22url%22%3A%22https%3A%2F%2Fdocs-mcp.openvidu.io%2Fmcp%22%7D)

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

**Other clients**

Any client that speaks MCP over Streamable HTTP works with the URL alone. The usual configuration is:

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

Check your client's documentation for where that file lives, and whether it names the field `type`, `transport` or nothing at all.

To check that it answers, ask your agent which OpenVidu documentation versions it can read.

### Privacy

Each request your coding agent makes to `docs-mcp.openvidu.io` is logged as one line: the tool it called, what it asked for (for a search, the search terms), the documentation version, whether it worked, how long it took, and the agent's name and version when it sends them. What was asked is kept to learn what developers look for and what the documentation is missing. Your conversation, your prompts and your code are never sent to us or stored.

Your IP address is used only to group one client's requests into a visit, and is discarded before anything is written to storage: visits are labelled with a random identifier that cannot be traced back to an address or linked to a later visit. Request logs are deleted after 7 days. The archive, which contains no addresses, is deleted after 395 days so a year-over-year comparison is possible. Aggregate counts are kept. Nothing is shared with third parties.

When your agent reads LiveKit's documentation, it fetches those pages from docs.livekit.io itself: that request never passes through OpenVidu, and LiveKit's own policies apply to it. The rest of what openvidu.io collects is in the [privacy policy](https://openvidu.io/3.9/conditions/privacy-policy/index.md).

### Troubleshooting

> **The client shows the server as failed or offline**
>
> The transport must be HTTP (Streamable HTTP), not `sse` or `stdio`, and the URL must end in `/mcp`. To check the server from a shell, list its tools:
>
> ```bash
> curl -s -X POST https://docs-mcp.openvidu.io/mcp \
>   -H 'content-type: application/json' \
>   -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
> ```

> **Opening the server URL in a browser gives an error**
>
> That is expected: the server only accepts `POST` requests. It is not a web page, and for the same reason a browser-based MCP client cannot use it.

> **A page you know exists isn't found**
>
> The server is rebuilt when this documentation is published, so a page published minutes ago may not be there yet.

## Without MCP

Every page of this site is also published as Markdown: add `index.md` to a page's URL, as in `https://openvidu.io/latest/docs/getting-started/index.md`. [`https://openvidu.io/llms.txt`](https://openvidu.io/llms.txt) indexes them for the latest release, and `https://openvidu.io/<version>/llms.txt` for each version, following the [llms.txt](https://llmstxt.org/) convention. Where your agent supports MCP, the server is the better option: it searches, and it answers for the version you ask for.
