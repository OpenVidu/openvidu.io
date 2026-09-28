---
title: "OpenVidu Meet vs OpenVidu Platform"
description: "OpenVidu Meet is a finished video conferencing app you deploy; OpenVidu Platform is the SDK layer you build on. Compare both and pick one."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
# faq_about_products adds both product SoftwareApplication nodes to the graph
# and points the FAQPage's `about` at them: this page is the routing decision
# between those two entities.
faq_about_products: true
faq:
  - anchor: should-i-choose-openvidu-meet-or-openvidu-platform
    question: "Should I choose OpenVidu Meet or OpenVidu Platform?"
    answer: >-
      Choose OpenVidu Meet if your use case falls under the category of "video
      conferencing application" — e-learning, telehealth, team collaboration, customer support — and you
      want a complete, ready-to-use video calling service running on your own servers. OpenVidu Meet can be embedded into an existing application 
      through a web component or an iframe, and comes with moderation controls, fine-grained customizable permission roles, live captions, recording management, 
      virtual backgrounds, E2E encryption and branding customizations out of the box. 
      Choose OpenVidu Platform if you need total control and flexibility to build your own custom
      real-time application, from scratch or inside an existing app: it provides low-level WebRTC SDKs
      for any language and full control over audio, video and data streaming, media ingestion,
      telephony and AI integrations.
  - anchor: can-i-use-openvidu-meet-and-openvidu-platform-together
    question: "Can I use OpenVidu Meet and OpenVidu Platform together?"
    answer: >-
      Yes. OpenVidu Meet runs as one of the services of an OpenVidu deployment, so the same
      self-hosted deployment can serve OpenVidu Meet rooms and the OpenVidu Platform SDKs at the same
      time. OpenVidu Meet can also be embedded into an existing application through a web component
      or an iframe, which is often enough without dropping down to the low-level SDKs. If you are not
      sure, the OpenVidu team can help you size a deployment that uses both.
  - anchor: do-both-products-offer-the-same-self-hosting-performance-and-scalability
    question: "Do both products offer the same self-hosting, performance and scalability?"
    answer: >-
      Yes. OpenVidu Meet and OpenVidu Platform are both self-hosted, both provide production-grade
      performance, scalability, fault tolerance and observability, and both come with cloud deployment
      templates, tutorials and customer support. The differences are in what you build with: OpenVidu
      Meet is a ready-to-use application with no-code and low-code options, and OpenVidu Platform is a
      set of low-level SDKs with high control over real-time features.
  - anchor: does-choosing-openvidu-meet-or-openvidu-platform-affect-pricing
    question: "Does choosing OpenVidu Meet or OpenVidu Platform affect pricing?"
    answer: >-
      No. Pricing depends on the OpenVidu edition and the deployment you run, not on which product you
      build with. OpenVidu COMMUNITY is open source and free to self-host for both, and OpenVidu PRO
      is billed the same way for both: per core per minute of the cluster you run.
hide:
  - feedback
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
tags: []
page_features:
  - revealonscroll
---

# OpenVidu Meet vs OpenVidu Platform

OpenVidu offers two different products:

- **OpenVidu Meet**: a complete, high-quality video calling service designed to be self-hosted. Ideal for teams, businesses and organizations that need a reliable, secure and customizable video conferencing solution running on their servers.
- **OpenVidu Platform**: a solution comprised of a self-hosted deployment and a set of SDKs and APIs that greatly simplifies the development of any type of real-time application.

![OpenVidu Meet vs OpenVidu Platform](assets/images/openvidu-meet-vs-openvidu-platform/meet-vs-platform-light.svg#only-light){ .skip-gallery loading=lazy }
![OpenVidu Meet vs OpenVidu Platform](assets/images/openvidu-meet-vs-openvidu-platform/meet-vs-platform-dark.svg#only-dark){ .skip-gallery loading=lazy }
/// caption
///

Both OpenVidu Meet and OpenVidu Platform provide **production-grade performance, scalability, fault-tolerance and observability**. What product should you choose?

- Give [**OpenVidu Meet**](meet/index.md) a try if your use case falls under the category of "video conferencing application": e-learning, telehealth, team collaboration, customer support, etc. Don't mistake the simplicity for a lack of possibilities: OpenVidu Meet offers branding customizations and many features out-of-the-box, such as screen-sharing, recording, chat, virtual backgrounds, E2E encryption, and more coming soon: broadcasting, AI agents...
- Choose [**OpenVidu Platform**](docs/index.md) if you really need total control and flexibility to build your own custom real-time app, either from scratch or integrating OpenVidu Platform into your existing app. OpenVidu Platform provides low-level WebRTC SDKs for any language, and full control over features like audio/video/data streaming, media ingestion, telephony and AI integrations.

<br>

<div class="text-center" markdown>

--8<-- "meet-vs-platform-table.md"

</div>

## Frequently asked questions

### Should I choose OpenVidu Meet or OpenVidu Platform?

Choose [**OpenVidu Meet**](meet/index.md) if your use case falls under the category of "video
conferencing application" — e-learning, telehealth, team collaboration, customer support — and you
want a complete, ready-to-use video calling service running on your own servers. OpenVidu Meet can be embedded into an existing application 
through a web component or an iframe, and comes with moderation controls, fine-grained customizable permission roles, live captions, recording management, 
virtual backgrounds, E2E encryption and branding customizations out of the box. 

Choose [**OpenVidu Platform**](docs/index.md) if you need total control and flexibility to build
your own custom real-time application, from scratch or inside an existing app: it provides low-level
WebRTC SDKs for any language and full control over audio, video and data streaming, media ingestion,
telephony and AI integrations.

### Can I use OpenVidu Meet and OpenVidu Platform together?

Yes. OpenVidu Meet runs as one of the [services of an OpenVidu deployment](docs/self-hosting/deployment-types.md#node-services),
so the same self-hosted deployment can serve OpenVidu Meet rooms and the OpenVidu Platform SDKs at
the same time. OpenVidu Meet can also be embedded into an existing application through a web
component or an iframe, which is often enough without dropping down to the low-level SDKs. If you
are not sure, the OpenVidu team can help you size a deployment that uses both.

### Do both products offer the same self-hosting, performance and scalability?

Yes. OpenVidu Meet and OpenVidu Platform are both self-hosted, both provide production-grade
performance, scalability, fault tolerance and observability, and both come with cloud deployment
templates, tutorials and customer support. The differences are in what you build with: OpenVidu Meet
is a ready-to-use application with no-code and low-code options, and OpenVidu Platform is a set of
low-level SDKs with high control over real-time features.

### Does choosing OpenVidu Meet or OpenVidu Platform affect pricing?

No. [Pricing](pricing.md) depends on the OpenVidu edition and the deployment you run, not on which
product you build with. OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } is open
source and free to self-host for both, and OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } is
billed the same way for both: per core per minute of the cluster you run.

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Still not sure which one fits?</h2>
  <p class="cta-lead">Tell us about your use case and we will help you pick — or size a deployment that uses both.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
