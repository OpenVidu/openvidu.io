---
draft: false
date: 2026-07-10
slug: video-conferencing-permissions
description: Compare the three access models for managing permissions in video conferencing apps — anonymous role links, identified guests and registered users — with pros, cons and when to use each.
cover_image: poster.png
categories:
    - OpenVidu Meet
    - Technology
tags:
    - WebRTC
    - Access Control
    - Permissions
    - Security
    - RBAC
    - Video Conferencing
authors:
    - juanCarlos
hide:
    - navigation
    - search-bar
    - version-selector
---

# Managing Permissions in Video Conferencing Apps: 3 Access Models

![Three access models for video conferencing permissions](/assets/images/blog/video-conferencing-permissions/poster-light.png#only-light "Managing permissions in video conferencing apps")
![Three access models for video conferencing permissions](/assets/images/blog/video-conferencing-permissions/poster-dark.png#only-dark "Managing permissions in video conferencing apps")

Everyone benchmarks video conferencing on the things you can see: resolution, latency, how many people fit in a grid. But the failures that actually hurt in production are rarely about a dropped frame — they're about the wrong person joining a room they shouldn't be in, or a private recording ending up somewhere public. **Permissions are the invisible half of a video app**, and they're the half most teams underestimate until something goes wrong.

<!-- more -->

Here's the uncomfortable part. At the media layer that low-level WebRTC SDKs expose, the *only* permissions you get are "can this token publish audio, video or screen." There's no notion of *who* a person is, whether they belong in the room at all, or who's allowed to watch the recording afterwards. That's a media grant, not an access-control system. You either build the missing layer yourself or embed a product that already has it.

This post lays out the three access models the industry keeps converging on — **anonymous role links**, **identified guests** and **registered users** — with concrete trade-offs and "use this when…" triggers. Then it shows how OpenVidu maps onto them: build-your-own on **OpenVidu Platform**, or the batteries-included model that **OpenVidu Meet** formalized in its 3.8.0 release.

## The two layers of permissions: media control vs access control

Before comparing models, you need to separate two things that get lumped together as "permissions."

- **Media / publishing permissions.** Can I turn on my camera? My microphone? Share my screen? Send data? This is what a raw WebRTC token carries, and it's genuinely low-level — it's about *tracks*, not people.
- **Access permissions.** Is this person allowed *into* the room in the first place? Who can end the meeting, kick participants, or promote someone to moderator? Who can list, play or delete the recording after everyone's gone home?

Low-level SDKs give you the first layer and stop there. In OpenVidu Platform (as in any LiveKit-based stack), you mint a token on your server with a set of *video grants*:

```javascript
const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity: participantName, // just a label you choose
});
at.addGrant({
    roomJoin: true,
    room: roomName,
    canPublish: true,
    canSubscribe: true,
});
```

Notice what's missing. There's no user, no account, no role, no ownership. The `identity` is just a string you invented. The grant says what tracks this token may publish — nothing about *whether this human should have been handed the token at all*. That decision lives in your application, and the SDK can't make it for you.

The access layer is where identity, roles, resource ownership and audit trails live. If you own the real-time logic, that layer is yours to design.

### Build it yourself, or embed a product that already has it

This is the pivotal fork in the road, and it's worth being honest about the cost of each path.

- **Build your own.** You get total control, but you're now on the hook for user accounts, link generation and expiry, role-to-grant mapping, per-person revocation, and recording ACLs. Every one of those is security-sensitive, and "we'll add real permissions later" is how leaks happen. This is the natural path with **OpenVidu Platform**, where you already own the business logic and just need the media plumbing.
- **Embed a product that already solved it.** Instead of reinventing access control, you inherit a battle-tested model and drive it from your app. This is **[OpenVidu Meet Embedded](../../meet/embedded/intro.md)** — the same users, room members, roles and permissions, exposed through a REST API and a Web Component you drop into your own UI.

Either way, you converge on one (or a mix) of the three models below. Let's compare them.

## Model 1: Predefined roles + shared anonymous links

The lowest-friction model there is. You define a fixed set of roles — say **Moderator** and **Speaker** — and generate one shareable link per role. Anyone who opens the link joins with that role's permissions, usually after typing a display name. No account, no setup.

**Pros**

- **Zero friction.** No sign-up, no per-person provisioning. Paste the link in a calendar invite and you're done.
- **Trivial to distribute.** One link reaches a hundred people as easily as one.
- **Great for open or large audiences** where you genuinely don't know who's coming.

**Cons**

- **The link is a bearer token.** Whoever holds it gets in. Forward it, screenshot it, leak it in a public channel — it still works.
- **No per-person identity or audit.** Everyone on a link is indistinguishable and equal.
- **Revocation is all-or-nothing.** You can't remove one person without rotating the link for everyone.

**Use it when:** webinars, open community calls, quick ad-hoc meetings, or any low-sensitivity "just click to join" experience.

!!! note "How OpenVidu Meet implements it"
    Each room exposes two shared anonymous links — one per predefined role — as `access.anonymous.moderator.url` and `access.anonymous.speaker.url`. New in 3.8.0, you can **enable or disable each role's anonymous link per room**, so you might allow anonymous speakers but require an identity to moderate. Anonymous guests are asked to choose a name before joining. See [Room Access](../../meet/features/rooms/access.md).

## Model 2: Identified guests + custom permissions

A step up in control, without the weight of user accounts. Here you explicitly add each individual as a room member with a fixed name and a base role — and you can fine-tune their permissions. Each guest receives their **own unique personal access link**, delivered privately, with no login required.

The mental model shifts from "here's a link for the role" to "here's a link for *this specific person*."

**Pros**

- **Per-person links mean per-person revocation.** Remove one guest and only their link dies — everyone else is unaffected.
- **A real (if lightweight) audit trail.** You know Dr. Smith's link, not just "a moderator."
- **No login friction.** Perfect for external people who'll never create an account in your system.
- **Per-person permission tuning.** Invite a guest who can speak but not record, for example.

**Cons**

- **Still a bearer token if forwarded** — but, crucially, an *individually revocable* one.
- **You must provision each guest ahead of time**, which doesn't scale to open audiences.

**Use it when:** telehealth (invite one specific patient to one specific consultation), 1:1 interviews, onboarding an external client or partner — anywhere you invite named people who won't have accounts.

!!! note "How OpenVidu Meet implements it"
    You add a member of type `identified_guest` with a display name and a base role (`Moderator` or `Speaker`), then optionally override individual permissions. Meet generates a unique `accessUrl` for that member. Removing the member **instantly** invalidates their link and expels them if they're mid-meeting. See [Room Members](../../meet/features/room-members/overview.md).

## Model 3: Registered users + custom permissions

The strongest model, and the one built for recurring, higher-stakes use. Individuals have real accounts in your system. You add a user as a member of a room and assign a role and permissions — but here's the key difference: **everyone accesses through the same shared user link and authenticates**. The *identity*, not the link, determines what happens.

Log in as an admin and you get one set of permissions; log in as a regular member and you get another. The link carries no secret at all.

On top of per-room membership, this model unlocks **organization-wide rules**:

- **Admins** get full access to every room, always.
- **Room owners** always have full access to the rooms they create.
- A room can be marked **accessible to all users**, so any authenticated user can join even without being added explicitly.

**Pros**

- **Access tied to an authenticated identity**, not a forwardable link — the strongest guarantee of the three.
- **Centralized user management and a real audit trail.** Who did what is a first-class question you can answer.
- **Org-wide policies** (admin, owner, open rooms) instead of per-room bookkeeping.
- **One link for everyone.** No per-person link distribution to manage.

**Cons**

- **You need an identity/auth system**, and users pay a login step.
- **Poor fit for one-off external guests** who shouldn't have to register.
- **Heavier to operate** than dropping a link in a chat.

**Use it when:** internal tools, enterprise apps, e-learning platforms with enrolled students, or anything with a known, recurring user base and compliance requirements.

!!! note "How OpenVidu Meet implements it"
    Meet ships a built-in user system with three account roles: `admin` (full control), `room_manager` (manages their own rooms) and `room_member` (accesses rooms they belong to). Users join through `access.user.url`, which renders a login form and carries no secret — your app never handles the password. Admins and room owners are implicit full-access members, and a room can be opened to all users (joining as `Speaker`). See [Users](../../meet/features/users/overview.md).

<!-- Diagram suggestion: side-by-side of the three link types — one shared anonymous link → many anonymous guests; one unique link per identified guest; one shared user link + login → authenticated users. Alt: "The three access-link types compared" -->

## Beyond access: fine-grained, per-person permissions

Notice that all three models answer "how do you get *in*." A separate question is "what can you *do* once you're in" — and that layer is **orthogonal**. You can attach the same fine-grained permission set to an anonymous role, an identified guest, or a registered user.

Predefined roles cover maybe 80% of cases out of the box. Fine-grained permissions handle the exceptions: a speaker who's allowed to record this one session, or a moderator who can run the meeting but *not* delete recordings.

OpenVidu Meet 3.8.0 introduced 14 boolean permissions for exactly this. Grouped for readability:

- **Media:** `canPublishVideo`, `canPublishAudio`, `canShareScreen`
- **Communication:** `canReadChat`, `canWriteChat`, `canChangeVirtualBackground`
- **Meeting management:** `canJoinMeeting`, `canEndMeeting`, `canKickParticipants`, `canMakeModerator`, `canShareAccessLinks`
- **Recording:** `canRecord`, `canRetrieveRecordings`, `canDeleteRecordings`

A member's effective permissions start from their base role and get overridden individually:

```json
{
    "baseRole": "speaker",
    "customPermissions": {
        "canPublishVideo": true,
        "canPublishAudio": true,
        "canShareScreen": false,
        "canRecord": true,
        "canRetrieveRecordings": true,
        "canDeleteRecordings": false
    }
}
```

Permissions aren't even fixed for the duration of a meeting. A participant with `canMakeModerator` can **promote** another participant on the fly — a change that's temporary and scoped to that meeting only, reverting when they leave. It's the difference between a static config and a living session. See [Role Management](../../meet/features/meetings/role-management.md).

Compare this to the low-level SDK token from earlier: there, you'd only ever have the *media* subset, and you'd model everything else — chat rights, who can end the call, recording control — yourself.

Worth calling out: some of these permissions keep mattering long after the call ends. Access control doesn't stop when everyone hangs up, and a recording is often the most sensitive artifact a meeting produces — so `canRetrieveRecordings` (list, play, download) is deliberately separate from the more dangerous `canDeleteRecordings`, and each access model implies a different answer to "should this person still see the recording next week?" In OpenVidu Meet, admins and room owners always keep full recording access, and a separate `access.anonymous.recording.enabled` switch controls anonymous reach. See [Recordings](../../meet/features/recordings/overview.md).

## How OpenVidu maps to these models: Platform vs Meet

If you've followed along, the OpenVidu split falls out naturally.

- **OpenVidu Platform** is for when you own both the business logic *and* the real-time logic. Tokens carry media permissions only; there is no built-in user or member concept. The three access models above are yours to build on top. That's the right trade when you're constructing a specialized media experience and want total control — see the [application server tutorials](../../docs/tutorials/application-server/node.md) for how token grants work.
- **OpenVidu Meet** gives you all three models, the fine-grained permissions and recording ACLs **out of the box**. Its 3.8.0 release formalized this around three pillars — **users**, **room members**, and **three distinct access-link types** (anonymous, identified-guest, and user links). Those concepts exist precisely so you don't have to reinvent access control on top of raw media grants.
- **OpenVidu Meet Embedded** lets you pull that entire access layer *into your own application*, driven by a [REST API](../../meet/embedded/reference/rest-api.md) and a [Web Component](../../meet/embedded/reference/webcomponent.md). You provision members and generate links from your backend; Meet enforces the permissions. You get the control of "build your own" without actually building the security-critical parts.

That's the whole justification for the new concepts in one line: **users, room members and typed access links** are the vocabulary you need to answer **"who gets in and what can they do"** — and rebuilding that vocabulary yourself is rarely time well spent.

## Which model should you choose?

There's no single winner. Match the model to the situation — and most real applications end up mixing them:

- **Open or large audience, low sensitivity?** → Anonymous role links (Model 1).
- **Named external people without accounts?** → Identified guests (Model 2).
- **Recurring, known user base with compliance needs?** → Registered users (Model 3).
- **A typical product?** → A mix. Think authenticated hosts running a room that anonymous attendees join by link, with a few named external guests invited individually.

The good news is you don't have to commit to one for the whole app. A single room in OpenVidu Meet can accept authenticated users, identified guests and anonymous participants at the same time — each through their own link type, each with their own permissions.

## Need more than this?

If you're deciding how to architect permissions right now, the fastest way to feel the trade-offs is to try the model that removes the build-your-own burden:

👉 **See it in action — [spin up a permissioned room with OpenVidu Meet Embedded](../../meet/embedded/intro.md).**

To go deeper on the concepts covered here:

- [Users](../../meet/features/users/overview.md) — accounts, roles and org-wide access rules.
- [Room Members](../../meet/features/room-members/overview.md) — identified guests vs registered users.
- [Room Access](../../meet/features/rooms/access.md) — the three access-link types.
- [Recordings](../../meet/features/recordings/overview.md) — permissioning recordings after the meeting.
- Access tutorials for each model: [anonymous access](../../meet/embedded/tutorials/access/anonymous-access.md), [identified guests](../../meet/embedded/tutorials/access/identified-guests.md), and [users](../../meet/embedded/tutorials/access/users.md).

And if you need total control over the media pipeline instead, [OpenVidu Platform](../../docs/index.md) gives you the low-level SDKs to build your own access layer from the ground up.
