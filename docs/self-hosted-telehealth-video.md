---
title: "Self-Hosted Telehealth Video: Where Your Data Lives"
description: "What self-hosting changes for telehealth video: data residency, HIPAA and GDPR duties, recording retention, roles and audit trails — and what stays yours."
# Structured Q&A metadata for this page's FAQ section. It feeds the JSON-LD
# (schema.org FAQPage) emitted by overrides/partials/json-ld.html. Keep in
# sync with the page content below: 'anchor' must match the heading id, and
# each answer must summarize the visible content of its section.
#
# COMPLIANCE NOTE FOR REVIEWERS: every answer here is about what self-hosting
# lets the operator do, never a claim that OpenVidu is certified or compliant.
# Any edit to these answers needs the same care as the page body.
faq:
  - anchor: is-openvidu-hipaa-compliant
    question: "Is OpenVidu HIPAA compliant?"
    answer: >-
      No software is HIPAA compliant on its own — HIPAA applies to organizations and to the systems
      they operate, not to a product in the abstract, and there is no official certification a video
      product can hold. OpenVidu is software you deploy and run yourself, so the question that
      matters is whether the environment you build around it meets your obligations. Self-hosting
      means no OpenVidu-operated service sits in the media path, so the controls, the logs and the
      recordings are yours to configure and to audit.
  - anchor: where-does-the-video-go
    question: "Where does telehealth video actually go in a self-hosted deployment?"
    answer: >-
      Between the participants' browsers and the servers you run, in the region you chose. OpenVidu
      deploys on-premises or on AWS, Azure, GCP, DigitalOcean and Oracle Cloud, the bundled TURN
      server only relays to your own deployment's nodes, and analytics are written to a MongoDB
      inside your deployment. One exception to know about: an OpenVidu PRO cluster reports its usage
      to accounts.openvidu.io on port 443 for billing, which is cluster usage data, not meeting
      content. OpenVidu COMMUNITY has no licence and makes no such call.
  - anchor: do-i-need-a-baa-with-openvidu
    question: "Do I need a Business Associate Agreement with OpenVidu?"
    answer: >-
      A BAA exists because a vendor creates, receives, maintains or transmits protected health
      information on your behalf. When you self-host, no OpenVidu-operated service touches your
      meeting media or your recordings, so there is normally nothing for a BAA to cover. The BAAs
      that do matter are with the parties that actually host or process data for you: your cloud
      provider, your storage, any transcription or AI service you add. Ask your own counsel, and ask
      us in writing before any engagement where our staff would access your systems.
  - anchor: can-consultations-be-end-to-end-encrypted
    question: "Can telehealth consultations be end-to-end encrypted?"
    answer: >-
      Yes, per room. With end-to-end encryption on, audio, video, chat and participant names are
      encrypted on each device with a key derived from a shared passphrase and the server only
      relays ciphertext. The trade-off is absolute: an encrypted room cannot be recorded, because
      the server has nothing it can decode. Rooms that must produce a recorded consultation run with
      transport encryption instead, and the recording lands in storage you control.
  - anchor: how-long-are-recordings-kept
    question: "How long are telehealth recordings kept?"
    answer: >-
      For as long as you keep them. Recordings are written to S3-compatible storage in your own
      deployment, so lifecycle rules, encryption at rest and legal holds are configured where that
      storage lives. OpenVidu Meet itself has no "delete recordings after N days" setting today: what
      it offers is an auto-deletion date on a room, with a policy that either deletes the room's
      recordings with it or keeps them. Retention against a records-retention rule is something you
      implement in your storage layer.
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

# Self-hosted telehealth video

**Self-hosted telehealth video** is videoconferencing for clinical consultations that runs on
infrastructure the care provider controls, rather than on a vendor's cloud — which changes who holds
the media, who holds the recordings, and who has to answer for them. This page goes through the
questions telehealth buyers actually ask: where the video goes, what HIPAA and GDPR do and do not
require of a video component, how recordings are stored and retained, how access is controlled, and
what an audit trail can be built from.

<div class="centered-section" markdown>

[Deploy OpenVidu Meet](meet/getting-started.md){ .md-button .md-button--primary }
[Meet or Platform?](openvidu-meet-vs-openvidu-platform.md){ .md-button }

</div>

!!! warning "This page is not legal advice"

    Nothing here is legal advice, and nothing here is a certification. Regulatory obligations depend
    on your organization, your jurisdiction, your data and your whole system — not on one component
    of it. Everything below describes what the software does and what self-hosting puts under your
    control; deciding whether that satisfies a specific rule is a conversation for your own counsel
    and your compliance team.

## Where does the video actually go?

This is the first question, and for a self-hosted deployment it has a short answer: **between your
users' browsers and the servers you run, in the region you chose**. The concrete facts behind that:

| | What happens |
|---|---|
| Media path | Browsers connect to the media server in your deployment. OpenVidu runs on-premises or on AWS, Azure, GCP, DigitalOcean and Oracle Cloud — you pick the region |
| Relay (TURN) | A TURN server is bundled, and it only relays to a restricted set of peers: the node's own interfaces and your own registered cluster nodes. It cannot be used to reach anything outside your deployment ([details](docs/self-hosting/how-to-guides/turn-security.md)) |
| Recordings | Written to S3-compatible storage in your deployment (a store is bundled), or to storage you point it at |
| Operational analytics | Written to a MongoDB **inside your deployment**, with a configurable retention window, and used by your own dashboard. Nothing is sent to OpenVidu |
| Licence and billing | An **OpenVidu PRO** cluster reports its usage to `accounts.openvidu.io` on port 443, because PRO is billed per core per minute. This is cluster usage, not meeting content. **OpenVidu COMMUNITY** needs no licence and makes no such call ([pricing](pricing.md)) |

For a data-residency requirement — "records of EU patients stay in the EU", "this never leaves our
datacentre" — that last column is the whole argument: there is no vendor cloud in the path to
reason about, so the question collapses into where *you* run servers and where *you* put storage.

## What does HIPAA actually require of a video vendor?

Less than most vendor pages imply, and more of it falls on you than on the software.

HIPAA is a set of obligations on **covered entities** and their **business associates** — hospitals,
clinics, insurers and the companies that handle protected health information on their behalf. It
regulates organizations and the safeguards they implement, not products. There is **no official
HIPAA certification** a piece of software can be awarded; a vendor claiming "HIPAA compliant" is
describing either their own operational practices as a business associate, or an environment they
believe supports your compliance. Neither is a property of the code.

So a video component cannot make you compliant, and cannot make you non-compliant on its own. What
it can do is make the required safeguards possible to implement — access control, encryption in
transit and at rest, logging, the ability to delete — and stay out of the way of the ones that are
organizational.

The practical consequence of self-hosting: **the video component stops being a business associate
question at all**, because no third party is receiving the media. The business-associate
relationships you still have to paper are with whoever hosts the servers and the storage.

## And GDPR?

GDPR turns on roles. When you self-host, you are the **controller** of the consultation data, and
because no OpenVidu-operated service processes it, there is normally no processor relationship with
us to document for the video itself — the processors are your hosting and storage providers. That
also removes the international-transfer problem for the media path: if your servers and your
recordings are in the EU, the media and the recordings are in the EU, and there is no transfer to
assess.

What GDPR still asks of you is not solved by hosting: a lawful basis for recording a consultation,
information given to the patient, a retention period you can justify and enforce, the ability to
satisfy access and erasure requests over recordings, and a DPIA where the processing warrants one.
Self-hosting makes those *implementable*; it does not make them done.

!!! note "One detail to raise in a DPIA"

    If you deploy **OpenVidu PRO**, note the licence-usage reporting described above and confirm its
    exact payload with us in writing before you document it. **OpenVidu COMMUNITY** removes the
    question entirely, since it has no licence and makes no outbound call.

## Do I need a BAA with OpenVidu?

A Business Associate Agreement exists because a vendor creates, receives, maintains or transmits
protected health information on your behalf. Self-hosted, no OpenVidu-operated service touches your
meeting media or your recordings, so there is normally nothing for such an agreement to cover.

The agreements that do matter are with the parties that genuinely process data for you — your cloud
provider, your storage provider, and any transcription, captioning or AI service you add to the
pipeline. Two situations are worth raising with us explicitly: a support or consultancy engagement
where our engineers would access your systems, and any future OpenVidu service that would process
data on your side of the line. [Talk to us](support/index.md) and get the answer in writing rather than
inferring it from a marketing page — including this one.

## Can consultations be end to end encrypted?

Yes, and the trade-off is worth understanding before you promise it to a clinical team.

[End-to-end encryption](meet/features/meetings/e2e-encryption.md) is enabled per room. Audio, video,
chat messages and participant names are encrypted on each device with a key derived locally from a
shared passphrase; the server relays ciphertext and never holds the key. Everyone in the room uses
the same passphrase — there is no partial or per-role access — and OpenVidu Meet does not distribute
it for you, so you deliver it through a channel you trust.

| | End-to-end encrypted room | Standard room |
|---|---|---|
| Who can read the media | Only participants with the passphrase | Participants; the server handles decoded media |
| Recording | **Not possible** — the server cannot decode what it relays | Available, stored in your own storage |
| Live captions and server-side AI | Not possible, same reason | Available |
| Typical fit | A consultation that must never be recorded | A consultation that must be recorded for the medical record |

That first row of the "Recording" line is the decision most telehealth deployments actually have to
make, and it is not an OpenVidu limitation so much as arithmetic: a server that cannot read the
media cannot write a recording of it. Teams generally split it by room type — encrypted rooms for
consultations that stay unrecorded, standard rooms where a recorded consultation is part of the
record and the recording is protected by storage controls instead.

## How do I control who joins a consultation?

A telehealth room has an obvious requirement: exactly one patient gets in, and no one else. OpenVidu
Meet's [room access model](meet/features/rooms/access.md) covers it with **identified guests** — a
named person, with no account, who receives their **own unique private link**. That is the model our
[video conferencing permissions](blog/posts/2026/07/video-conferencing-permissions.md) post
recommends for exactly this case: invite one specific patient to one specific consultation.

The other two ways in are **users** (registered accounts, logging in) for clinicians, and
**anonymous guests** through a shared link, which is the one a telehealth deployment usually turns
off.

On top of that sit roles and permissions: the built-in **Moderator** and **Speaker** roles, whose
defaults can be customized per room or per member, and which govern who may start and stop a
recording, who may retrieve or delete one, who may admit, promote or remove a participant, and who
may share access links. A clinician is typically a Moderator; a patient is a Speaker with recording
permissions removed.

## What can I build an audit trail from?

OpenVidu Meet emits [webhooks](meet/embedded/reference/webhooks.md) for five events —
`meetingStarted`, `meetingEnded`, `recordingStarted`, `recordingUpdated` and `recordingEnded` — each
signed with an HMAC-SHA256 `x-signature` over a timestamp and body using your API key, and retried
with exponential backoff if your endpoint does not acknowledge them.

Be clear-eyed about what that is: **a reliable feed of meeting and recording lifecycle events that
your system can persist into its own audit log**, not a ready-made audit log. Who accessed which
recording, and when, is recorded where the access happens — your application, your storage, your
identity provider. If an auditor is going to ask "who watched this consultation", design that log on
your side from the start.

## Checklist: what to ask any telehealth video vendor

Useful whoever you end up choosing, us included.

| Question | Why it matters | Self-hosted answer |
|---|---|---|
| Where is media processed, and in which region? | Data residency, transfer assessments | Your servers, your region |
| Does any third party sit in the media path? | Business-associate and processor relationships | No, when self-hosted |
| Where do recordings land, and who can download them? | The highest-risk artifact in telehealth | Your storage; permissions control retrieval and deletion |
| Can I set a retention period and enforce erasure? | GDPR erasure, records-retention rules | In your storage layer; the product has room-level auto-deletion, not per-recording retention |
| Is end-to-end encryption available, and what breaks with it on? | Vendors rarely volunteer the trade-off | Available per room; recording and server-side AI are not |
| What events can I log, and what is missing? | Audit trails | Five lifecycle webhooks, signed; access logging is yours to build |
| What does the product phone home, if anything? | DPIAs and network policy | Nothing in COMMUNITY; licence-usage reporting in PRO |
| Is there a certification, or a description of practices? | "HIPAA compliant" is usually the latter | Ask for the distinction in writing |
| What is not shipped yet? | The gap between the demo and the roadmap | See below |

## What OpenVidu Meet does not do yet

Stated plainly, because a telehealth evaluation will find these anyway:

- **No SSO.** OpenVidu Meet accounts are password-based; there is no SAML or OIDC login for
  clinician accounts today. Deployments that need SSO put OpenVidu Meet behind their own application
  and use [embedding](meet/embedded/intro.md), where your app owns identity.
- **No per-recording retention policy.** Rooms can carry an auto-deletion date and a policy that
  deletes or keeps their recordings; "erase every recording after N days" is a storage lifecycle
  rule you configure, not a product setting.
- **Locked rooms, file sharing and medical-vocabulary captions are on the roadmap**, not shipped.
  Treat the roadmap as a roadmap.
- **Recording and end-to-end encryption are mutually exclusive**, as above.

## Who runs OpenVidu in production

The published customer stories closest to this profile are in e-learning rather than telehealth —
[DynDevice](blog/posts/2026/07/dyndevice-virtual-classrooms-openvidu.md), which built virtual
classrooms into its LMS, and [Novakid](blog/posts/2026/09/novakid-live-english-lessons.md), which
runs live English lessons at scale. They are useful as evidence of the deployment model and the
scale, not as a clinical reference.

<!--
  PLACEHOLDER (deliberate, do not remove silently): a named telehealth customer quote belongs here.
  Nothing has been written in because no telehealth customer approval is recorded. Tracker row #26
  (openvidu-marketing/critical-issues.md) covers testimonial approvals; the interview pipeline lives
  in openvidu-brain under "Operaciones/03 - Operaciones de marketing/Interviews/". Do not add a
  quote, a logo or a named deployment here until written approval exists for that specific use.
-->

## Frequently asked questions

### Is OpenVidu HIPAA compliant?

No software is HIPAA compliant on its own — HIPAA applies to organizations and to the systems they
operate, not to a product in the abstract, and there is no official certification a video product
can hold. OpenVidu is software you deploy and run yourself, so the question that matters is whether
the environment you build around it meets your obligations. Self-hosting means no OpenVidu-operated
service sits in the media path, so the controls, the logs and the recordings are yours to configure
and to audit.

### Where does telehealth video actually go in a self-hosted deployment?

Between the participants' browsers and the servers you run, in the region you chose. OpenVidu
deploys on-premises or on AWS, Azure, GCP, DigitalOcean and Oracle Cloud, the bundled TURN server
only relays to your own deployment's nodes, and analytics are written to a MongoDB inside your
deployment. One exception to know about: an OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }
cluster reports its usage to `accounts.openvidu.io` on port 443 for billing, which is cluster usage
data, not meeting content. OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } has no
licence and makes no such call.

### Do I need a Business Associate Agreement with OpenVidu?

A BAA exists because a vendor creates, receives, maintains or transmits protected health information
on your behalf. When you self-host, no OpenVidu-operated service touches your meeting media or your
recordings, so there is normally nothing for a BAA to cover. The BAAs that do matter are with the
parties that actually host or process data for you: your cloud provider, your storage, any
transcription or AI service you add. Ask your own counsel, and ask us in writing before any
engagement where our staff would access your systems.

### Can telehealth consultations be end-to-end encrypted?

Yes, per room. With end-to-end encryption on, audio, video, chat and participant names are encrypted
on each device with a key derived from a shared passphrase and the server only relays ciphertext.
The trade-off is absolute: an encrypted room cannot be recorded, because the server has nothing it
can decode. Rooms that must produce a recorded consultation run with transport encryption instead,
and the recording lands in storage you control.

### How long are telehealth recordings kept?

For as long as you keep them. Recordings are written to S3-compatible storage in your own
deployment, so lifecycle rules, encryption at rest and legal holds are configured where that storage
lives. OpenVidu Meet itself has no "delete recordings after N days" setting today: what it offers is
an auto-deletion date on a room, with a policy that either deletes the room's recordings with it or
keeps them. Retention against a records-retention rule is something you implement in your storage
layer.

<div class="centered-section" markdown>

[Deploy OpenVidu Meet](meet/getting-started.md){ .md-button .md-button--primary }
[Embed it in your own app](meet/embedded/intro.md){ .md-button }

</div>

<div class="second-slogan cta-section" data-sal="slide-up">
  <h2 class="cta-title">Evaluating OpenVidu for a telehealth deployment?</h2>
  <p class="cta-lead">Tell us about your data-residency, recording and audit requirements and we will tell you plainly what the product does and does not cover.</p>
  <div class="home-buttons">
    <a href="/support/#talk-to-an-expert" class="md-button home-secondary-button">Talk to an expert</a>
  </div>
</div>
