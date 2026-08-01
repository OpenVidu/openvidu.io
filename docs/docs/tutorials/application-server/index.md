---
title: "OpenVidu application server tutorials"
description: "Build the backend of an OpenVidu app in Node.js, Java, Python, Go, .NET, PHP, Ruby or Rust: issue access tokens and receive webhook events."
---

# Application Server Tutorials

Every application server below has two specific purposes: 

- Generate LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receive LiveKit [webhook events](../../reference/webhooks.md).

To do so they all define two REST endpoints:

- `/token`: takes a room and participant name and returns a token.
- `/webhook`: for receiving webhook events from LiveKit Server.

They use the proper [LiveKit Server SDK :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/reference/){target=\_blank} for their language, if available.

<div class="tutorials-container" markdown>

[:simple-nodedotjs:{.icon .lg-icon .tab-icon} **Node.js**](./node.md){ .md-button .md-button--primary .tutorial-link }

[:simple-goland:{.icon .lg-icon .tab-icon} **Go**](./go.md){ .md-button .md-button--primary .tutorial-link}

[:simple-ruby:{.icon .lg-icon .tab-icon} **Ruby**](./ruby.md){ .md-button .md-button--primary .tutorial-link}

[:fontawesome-brands-java:{.icon .lg-icon .tab-icon} **Java**](./java.md){ .md-button .md-button--primary .tutorial-link}

</div>

<div class="tutorials-container" markdown>

[:simple-python:{.icon .lg-icon .tab-icon} **Python**](./python.md){ .md-button .md-button--primary .tutorial-link}

[:simple-rust:{.icon .lg-icon .tab-icon} **Rust**](./rust.md){ .md-button .md-button--primary .tutorial-link}

[:simple-php:{.icon .lg-icon .tab-icon} **PHP**](./php.md){ .md-button .md-button--primary .tutorial-link}

[:simple-dotnet:{.icon .lg-icon .tab-icon} **.NET**](./dotnet.md){ .md-button .md-button--primary .tutorial-link}

</div>
