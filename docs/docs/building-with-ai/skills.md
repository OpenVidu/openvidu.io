---
title: "OpenVidu skills for AI coding agents"
description: "Install the OpenVidu agent skills in Claude Code, Cursor, VS Code, Codex, Gemini CLI or Kiro: with the Agent Plugin, the skills CLI or by copying them."
---

# OpenVidu skills

A skill is a set of instructions that a coding agent loads when a task calls for it, defined by the [Agent Skills specification :fontawesome-solid-external-link:{.external-link-icon}](https://agentskills.io/specification){:target="_blank"}. OpenVidu's skills are included in the [OpenVidu Agent Plugin](agent-plugin.md), and can also be installed on their own.

## Available skills

| Skill | What it does |
| --- | --- |
| `openvidu-version-edition-product` | Finds out which OpenVidu version, edition and product your project uses when an answer depends on them. It reads them from the deployment itself, asks before contacting a remote host and never reads a credential. Then it offers to write them into `AGENTS.md` or `CLAUDE.md`, [like this](agent-plugin.md#tell-your-agent-which-openvidu-you-run). It needs the [documentation server](mcp-servers.md). |

## Install

With the plugin installed, there is nothing else to do. Without it, use the skills CLI or copy the skills by hand.

### With the skills CLI

The [skills CLI :fontawesome-solid-external-link:{.external-link-icon}](https://skills.sh/){:target="_blank"} detects the coding agents on your machine and copies each skill to where that agent looks for it:

```bash
npx skills add OpenVidu/openvidu-agent-plugin
```

Add `-g` to install them for every project instead of the current one.

### By hand

A skill is a directory, not just its `SKILL.md`. Copy each one from the [`skills/` folder :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin/tree/main/skills){:target="_blank"} of the plugin repository to a location your client scans, and keep the directory's name: it must match the `name` in its `SKILL.md`.

| Client | One project | Every project |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/`, `.cursor/skills/`, `.claude/skills/` | `~/.agents/skills/`, `~/.cursor/skills/`, `~/.claude/skills/` |
| VS Code and GitHub Copilot | `.github/skills/`, `.agents/skills/`, `.claude/skills/` | `~/.copilot/skills/`, `~/.agents/skills/`, `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/`, `.agents/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` |

For example, for every project in Claude Code:

```bash
git clone --depth 1 https://github.com/OpenVidu/openvidu-agent-plugin /tmp/openvidu-agent-plugin
mkdir -p ~/.claude/skills
cp -r /tmp/openvidu-agent-plugin/skills/. ~/.claude/skills/
rm -rf /tmp/openvidu-agent-plugin
```

To share them with your team, copy them to `.claude/skills/` in your repository and commit them: Claude Code, Cursor and VS Code all read that directory. Claude Desktop and claude.ai don't read a folder on your disk: skills are enabled in their settings.

### Check they loaded

Claude Code lists them in `/skills`. In VS Code, type `/` in the chat. Elsewhere, look wherever your client lists what it has loaded.

## Keep them current

- **With the plugin**, they update with it: see the **Updates** line of your client in [Install](agent-plugin.md#install).
- **With the skills CLI**, run `npx skills update`.
- **Copied by hand**, copy them again.

A client without skills can still get what the `openvidu-version-edition-product` skill would establish: [write it into `AGENTS.md`](agent-plugin.md#tell-your-agent-which-openvidu-you-run) yourself.

## Troubleshooting

??? question "A skill never activates"

    A skill loads when your request matches its description, so name OpenVidu in the request. If you copied it by hand, check that the directory keeps the skill's name and sits in a location your client scans. A skill whose work is already done, such as a version already pinned in `AGENTS.md`, also stays quiet.
