---
title: "Embed OpenVidu Meet with an AI coding agent"
description: "Let your coding agent read the OpenVidu Meet REST API, web component and webhook docs for your own deployment while it embeds Meet in your app."
---

# Embed OpenVidu Meet with an AI coding agent

A coding agent can do most of the work of embedding OpenVidu Meet: creating rooms from your backend, placing the `<openvidu-meet>` web component in your frontend, reacting to webhooks. What it cannot do is guess the API right. Left to its training data, it writes code for an older release, for an edition you don't have, or for the LiveKit SDKs of [OpenVidu Platform](../../docs/index.md) instead of Meet's own API.

The **OpenVidu Agent Plugin** fixes that. It gives Claude Code, Cursor, VS Code, GitHub Copilot, Codex and other coding agents the official OpenVidu documentation, matched to the version and edition of your deployment, and has them establish that your project uses OpenVidu Meet before they answer.

[Install the OpenVidu Agent Plugin](../../docs/coding-agents/agent-plugin.md){ .md-button .md-button--primary }

## What your agent does with it

- Reads the [REST API](reference/rest-api.md), [web component](reference/webcomponent.md) and [webhooks](reference/webhooks.md) references for the OpenVidu release you run, instead of recalling them.
- Works out your deployment's version and edition from the deployment itself, and writes them into your project's `AGENTS.md` or `CLAUDE.md`, so every later session starts from them.
- Keeps to OpenVidu Meet's API when the question could also be answered with OpenVidu Platform's.

## Example prompts

- "Using the OpenVidu docs, add a backend endpoint that creates an OpenVidu Meet room and returns the URL our frontend passes to the web component."
- "Embed the `<openvidu-meet>` web component in our React page, and show our own screen when the participant leaves the meeting."
- "Which OpenVidu Meet webhook tells us a recording is ready, and what does its payload carry? Check the docs for our version."
- "Work out which OpenVidu version and edition this project connects to, and write them into AGENTS.md."

For a complete application built this way, see [Building a video-enabled CRM with an AI agent](../../blog/posts/2026/07/building-a-video-enabled-crm-with-an-ai-agent.md): a CRM with embedded OpenVidu Meet meetings, from an empty folder to per-guest room permissions in seven prompts.

## Installation and setup

The same plugin covers OpenVidu Meet and OpenVidu Platform, so it is documented once, in the OpenVidu Platform section:

- [OpenVidu Agent Plugin](../../docs/coding-agents/agent-plugin.md): what it contains, how to install it in each coding agent and how to keep it updated.
- [Manual setup](../../docs/coding-agents/manual-setup.md): the same MCP server and skill configured by hand, for clients that don't load plugins.
