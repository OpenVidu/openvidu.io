---
title: Introducing the OpenVidu Agent Plugin for coding agents
draft: false
date: 2026-10-06
slug: openvidu-agent-plugin
description: Meet the OpenVidu Agent Plugin, which gives your coding agent the official OpenVidu documentation for the version, edition and product you run.
cover_image: poster-light.webp
categories:
  - AI
  - OpenVidu
tags:
  - AI agents
  - Coding agents
  - MCP
  - Agent skills
  - Agent plugins
  - Claude Code
authors:
  - juanCarlos
---

# Introducing the OpenVidu Agent Plugin for coding agents

![The OpenVidu Agent Plugin: the OpenVidu documentation server and the version, edition and product skill, installed in one step in Claude Code, VS Code, GitHub Copilot, Codex, Cursor and Kiro](/assets/images/blog/2026/10/openvidu-agent-plugin/poster-light.webp#only-light "The OpenVidu Agent Plugin"){ .round-corners }
![The OpenVidu Agent Plugin: the OpenVidu documentation server and the version, edition and product skill, installed in one step in Claude Code, VS Code, GitHub Copilot, Codex, Cursor and Kiro](/assets/images/blog/2026/10/openvidu-agent-plugin/poster-dark.webp#only-dark "The OpenVidu Agent Plugin"){ .round-corners }

Is your coding agent writing the code that creates your OpenVidu Meet rooms, generates your access tokens or configures your deployment? Then it should read the same documentation you would. Today we're releasing the **OpenVidu Agent Plugin**: install it once in Claude Code, VS Code, GitHub Copilot, Codex, Cursor or Kiro, and your agent reads the official OpenVidu documentation for the version you run, so the code it writes is up to date and accurate.

The plugin bundles a documentation server with the <a href="/meet/">OpenVidu Meet</a> and <a href="/docs/">OpenVidu Platform</a> docs of every release from 3.4, and a skill that works out which OpenVidu your project uses. The <a href="/docs/building-with-ai/agent-plugin/">OpenVidu Agent Plugin</a> page has the whole story. This post is the short tour, plus how well it answers.

<!-- more -->

## What's in the OpenVidu Agent Plugin

An agent plugin is a package your coding agent installs in one step, bundling MCP servers and skills. Its format is the open [Agent Plugins specification :fontawesome-solid-external-link:{.external-link-icon}](https://agent-plugins.org/specification){:target="_blank"}, implemented by VS Code, Cursor, GitHub Copilot, Codex, Kiro and other clients. Claude Code has a format of its own, and the OpenVidu Agent Plugin ships in both.

Inside, there are two pieces:

- **The OpenVidu documentation server.** An MCP server that searches and reads the OpenVidu Meet and OpenVidu Platform documentation of every release from 3.4, along with its release notes and pricing. When your agent needs more, such as the client SDK references, the server points it to LiveKit's documentation. No account, no API key: [OpenVidu MCP servers](/docs/building-with-ai/mcp-servers.md) lists its tools.
- **The `openvidu-version-edition-product` skill.** A procedure your agent follows when an answer depends on which OpenVidu you run. More on it below, and in [OpenVidu skills](/docs/building-with-ai/skills.md).

The plugin helps you build *with* OpenVidu. If what you're after is AI agents inside your rooms, that's [AI Services](/docs/ai/overview.md).

## Answers for the OpenVidu you run

OpenVidu publishes one documentation set per release, and the APIs grow from one to the next: the OpenVidu Meet room members API, for instance, arrived in 3.8. The documentation server answers from the documentation of the version your deployment reports, so `3.9.1` gets the 3.9 docs. A version it doesn't carry is an error, never an answer for another release. Without a version, it uses the latest.

Many answers also depend on the **edition**, COMMUNITY or PRO, and on the **product** your app uses, OpenVidu Meet or OpenVidu Platform. Your dependencies don't give the version away: `livekit-client`, `livekit-server-sdk` and the OpenVidu Meet web component are versioned independently of OpenVidu. So when an answer needs these facts, the skill has your agent find them out from the project and the deployment itself. It asks before contacting a remote host, never reads a credential, and offers to write what it found into `AGENTS.md`, so later sessions start from there.

You can also write them yourself, in `AGENTS.md` or `CLAUDE.md`:

```markdown title="AGENTS.md"
This project connects to an OpenVidu 3.9.0 pro deployment, using OpenVidu Meet.
When querying the OpenVidu documentation MCP, always pass version="3.9.0",
and read the answers for that edition and product.
```

[Tell your agent which OpenVidu you run](/docs/building-with-ai/agent-plugin.md#tell-your-agent-which-openvidu-you-run) has the details.

## Install it

In Claude Code, it takes two commands:

```text
/plugin marketplace add OpenVidu/openvidu-agent-plugin
/plugin install openvidu@openvidu
```

VS Code, GitHub Copilot CLI, Codex, Cursor and Kiro install it from the same repository, [OpenVidu/openvidu-agent-plugin :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin){:target="_blank"}. The [Install](/docs/building-with-ai/agent-plugin.md#install) section has the steps for each client, and how to keep the plugin updated.

Your client doesn't load plugins? Add the [documentation server](/docs/building-with-ai/mcp-servers.md#add-it-to-your-client) and the [skills](/docs/building-with-ai/skills.md#install) on their own. The server works in any MCP client with its URL alone, `https://docs-mcp.openvidu.io/mcp`, and `npx skills add OpenVidu/openvidu-agent-plugin` copies the skill to the coding agents it finds on your machine. You'll also find the server in the official MCP Registry, as `io.openvidu/docs`, and the skill on [skills.sh :fontawesome-solid-external-link:{.external-link-icon}](https://skills.sh/){:target="_blank"}.

Then ask as you would about any other code, and your agent reads the documentation when the task needs it:

- "How do I record a room with individual tracks in OpenVidu?"
- "We're on OpenVidu 3.9.0. How do I deploy it with fault tolerance?"
- "Work out which OpenVidu version, edition and product this project uses, and write them into AGENTS.md."

## How well does it answer?

We measured it before the launch. We wrote 47 questions about OpenVidu, had Claude Code answer each one three times from memory, with web search, and with web search plus the plugin, and had Claude Opus grade every answer against the published documentation. An answer counts as correct when it covers at least three quarters of the facts the question calls for and makes no false claim.

| | From memory | With web search | With the plugin |
|---|---|---|---|
| Correct answers, Claude Sonnet 5.5 | 24% | 91% | **99%** |
| Correct answers, Claude Haiku 4.5 | 9% | 60% | **77%** |
| Answers with a false claim, Claude Sonnet 5.5 | 20% | 5% | **1%** |
| Answers with a false claim, Claude Haiku 4.5 | 43% | 26% | **6%** |

Web search is the configuration to compare with, since it's what a coding agent reaches for on its own; answering from memory is there as a reference. The plugin makes the most difference on the questions the OpenVidu documentation answers, about how to do something: with it, Claude Sonnet 5.5 answered all of them correctly, against 83% with web search, and Claude Haiku 4.5 went from 37% to 83%, with no false claims at all. And 99% of Sonnet's answers linked the documentation page that answers the question, so you can check them.

On cost, with Haiku the plugin came out cheaper per question than searching the web ($0.041 against $0.052). With Sonnet it cost a little more ($0.127 against $0.112).

## Embedding OpenVidu Meet with an agent

If you embed OpenVidu Meet in your app, start from [Embed OpenVidu Meet with an AI coding agent](/meet/embedded/building-with-ai.md). The plugin gives your agent the REST API, web component and webhooks references for the version and edition you run, and the page has prompts to try.

We've built a whole application with an agent before. In [Building a video-enabled CRM with an AI agent](/blog/posts/2026/07/building-a-video-enabled-crm-with-an-ai-agent.md), an agent went from an empty folder to a CRM with embedded OpenVidu Meet meetings in seven prompts, and we pointed it at three documentation pages by hand. With the plugin, your agent finds the pages it needs on its own, for your version.

## Privacy

The plugin itself collects nothing. The documentation server logs each request your agent makes, with details such as the tool it called, what it searched for and the documentation version, but never your code, your prompts or your conversation. Your IP address is used only to group requests into a visit and is never stored. The [privacy section](/docs/building-with-ai/mcp-servers.md#privacy) has what is recorded and for how long.

## What we're working on next

Coding agents are becoming part of how applications get built, so this is only the first step. On the way:

- **A Grafana and observability skill.** In [Debugging WebRTC with an AI agent and Grafana MCP](/blog/posts/2026/08/debugging-webrtc-with-ai-and-grafana-mcp.md), an agent with nothing but read-only Grafana tracked down what was wrong with a broken OpenVidu deployment, and we said we were preparing MCPs and skills so coding agents can manage and operate OpenVidu stacks. The plugin is the first of them, and this skill is the next.
- **Skills to migrate from OpenVidu 2 to OpenVidu 3**, for applications still on the previous generation.
- **Skills to migrate to OpenVidu Meet from other technologies**, for apps that run their video calls on something else today.

## Try it and tell us what you think

Install the plugin, ask your agent about the OpenVidu you run, and see what comes back.

[Install the OpenVidu Agent Plugin :fontawesome-solid-arrow-right:](/docs/building-with-ai/agent-plugin.md#install){ .md-button .md-button--primary }

Then tell us how it went: a wrong answer, a page it couldn't find, a client where it doesn't install. Open an issue in [OpenVidu/openvidu-agent-plugin :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-agent-plugin/issues){:target="_blank"}. Every question your agent can't answer tells us what to improve, in the plugin or in the documentation itself.
