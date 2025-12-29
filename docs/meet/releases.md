## 3.5.0

!!! info "For the Release Notes of OpenVidu Platform 3.5.0, please visit here: [OpenVidu Platform 3.5.0 :fontawesome-solid-external-link:{.external-link-icon}](../docs/releases.md#350){:target="_blank" .platform-link-color}"

### Changelog

- **End-to-End encryption in rooms**: End-to-End Encryption (E2EE) can now be enabled in rooms to protect all sensitive data such as audio, video, chat messages, and participant names. With E2EE enabled, content is encrypted on the sender’s device and can only be decrypted by authorized participants on their own devices using a secret shared key, ensuring that no intermediate server (including the OpenVidu Meet deployment itself) can access the data. When creating a room, E2EE can be enabled, and participants must join the meeting using the same shared secret. Audio and video streams are fully encrypted end to end. Chat messages and participant names are also encrypted and automatically decrypted on reception.
- **Improved meeting layout with Last N Speakers support**: the meeting layout has been enhanced with a new _Last N Speakers_ mode, designed to improve visual clarity and client-side performance in meetings with a large number of participants. This layout prioritizes the local user and up to N remote participants based on recent voice activity, where N is configurable (from 1 to 6). The layout is intelligent, applying stable replacement policies to avoid excessive or distracting participant reordering, only updating when meaningful changes in voice activity are detected. Audio remains continuously active even when participants are not visible, preventing any loss of spoken content while significantly reducing hardware usage on the client side.
- **Fixed an authentication issue when joining meetings with an expired access token**: this issue prevented users from joining a meeting inside a room when an expired access token was present. This could happen if the user had previously logged into OpenVidu Meet and the access token had already expired (after 2 hours). When accessing a room view directly without going through the console, the token was not properly refreshed, causing an authentication error even though authentication was not required to join the meeting. This has now been corrected to ensure seamless access to rooms regardless of token expiration state.
- **Fixed a potential inconsistent recording state after a server crash**: this issue occurred when a recording was in an active state (`active` or `ending`) and its lifecycle was completed, but the corresponding webhook event (`egress_ended`) was not received due to the server becoming unavailable. As a result, the recording state was never properly updated. A new scheduler has been introduced to periodically (every 15 minutes) detect recordings in this situation and automatically reconcile their state.
- **Fixed a potential inconsistent room state after a server crash**: this issue occurred when a room was in an active meeting state (`active_meeting`) and the meeting was ended, but the expected webhook event (`room_finished`) was not received, typically due to a server failure. In these cases, the room state was never updated correctly. A new scheduler has been introduced to periodically (every 15 minutes) detect rooms in this situation and automatically reconcile their state.
- **Fixed an issue with duplicate participant name suffixes**: participant names could end up with repeated "_1" suffixes when joining a meeting with the same name as an existing participant. This is now fixed.
- Rooms cannot be updated while a meeting is active.
- **Room names and participant names can now include any character**: the restriction to only allow alphanumeric characters, hyphens, and underscores has been removed. Room names and participant names can now include any character, supporting better internationalization and customization.
- **OpenVidu Meet persistent data is now stored in MongoDB instead os S3**: OpenVidu Meet now uses MongoDB as the primary database to store all Meet-related data (with the exception of recording files, which continue to be stored in S3). This change addresses the limitations of the S3 API when performing advanced search and query operations. When upgrading from a previous version OpenVidu Meet 3.5.0 will automatically perform a migration of the existing data from S3 to MongoDB.
- **Better room and recording filter and sorting capabilities**: as a result of persistent data migration to MongoDB, new filtering options have been added to the room and recording search functionality based on their status. In addition, search results can now be sorted by multiple fields, both in ascending and descending order, providing more flexible and powerful querying capabilities.

    !!! warning
        The migration process of OpenVidu Meet persistent data from S3 to MongoDB is expected to run transparently and without any issues. However, as a precaution measure, it is strongly recommended to create a backup of the existing data in S3 before upgrading OpenVidu to version 3.5.0.

### Breaking changes

- **Rooms can no longer be updated while a meeting is active**: updating a room is now restricted when there is an active meeting associated with it, preventing state inconsistencies and unexpected behavior during ongoing sessions.
- **Default sorting of rooms and recordings has changed**: rooms and recordings are now sorted by creation date by default, instead of being ordered alphabetically by room ID.

## 3.4.0

!!! info "For the Release Notes of OpenVidu Platform 3.4.0, please visit here: [OpenVidu Platform 3.4.0 :fontawesome-solid-external-link:{.external-link-icon}](../docs/releases.md#340){:target="_blank" .platform-link-color}"

### Introducing OpenVidu Meet

We are excited to announce a new product in the OpenVidu family: **OpenVidu Meet**.

### What is OpenVidu Meet?

OpenVidu Meet is a fully featured video calling service built on top of OpenVidu, designed to provide an easy-to-use, self-hosted solution for virtual meetings. Its design principles are:

- **Simplicity**: OpenVidu Meet is built on the same concepts as OpenVidu, but wraps them in a higher-level API, ideal for virtual meeting use cases. Simply manage rooms, meetings, and recordings.
- **Feature-rich**: OpenVidu Meet includes all the features you would expect from a modern video conferencing solution: HQ audio/video, screen sharing, chat, recording, and more. We will be continuously adding more features, taking advantage of all the advanced capabilities of OpenVidu: live-captions, AI integrations, streaming to large audiences, breakout rooms...
- **Refined UI/UX**: OpenVidu Meet user interface boasts a modern and intuitive design. Years of experience in the video conferencing space have been distilled into a polished user experience that feels familiar and gets out of the way. Perfect for all kinds of use cases, from e-learning to telehealth, collaboration and customer support.
- **Self-hosted and secure by design**: OpenVidu Meet is self-hosted, allowing you to retain full control over your data and compliance, and at the same time leverage your infrastructure. It can be easily deployed on-premises or in the cloud, with native integrations available for AWS, Azure, and GCP.
- **Embed-first integration**: OpenVidu Meet can act as a final application, but it is also designed to be embedded into your own web app with minimal effort. It provides a Web Component, REST API and Webhooks to integrate rooms, automate lifecycles, and connect to your business logic.

### Why a separate OpenVidu product?

Visitors to the OpenVidu website will notice that there are now two distinct products: **OpenVidu Meet** and **OpenVidu Platform**, with very distinct color schemes. Both products serve complementary needs:

- **OpenVidu Platform** is just what OpenVidu has always been: a powerful platform for builders who want complete flexibility with SDKs and APIs to craft bespoke real-time experiences. For users of any previous version of OpenVidu, nothing changes: what was previously "OpenVidu" has now simply been renamed "OpenVidu Platform".
- **OpenVidu Meet** is a response to the growing demand for specialized video conferencing solutions that cater to the unique needs of virtual meetings. While OpenVidu Platform provides a powerful foundation for real-time communication, OpenVidu Meet builds on that foundation to deliver a more focused set of features and a simplified integration process.

By separating the product lines, we keep the developer‑first power of OpenVidu Platform while offering a refined, ready‑to‑use solution for common videoconferencing use cases (e‑learning, telehealth, collaboration, customer support...). This clarity helps teams choose low‑level control with OpenVidu Platform, or the fastest path to value-off‑the‑shelf with OpenVidu Meet. In short, many use cases that fall under the category of "video conferencing applications" can be satisfied with OpenVidu Meet, saving development time and resources.

You can read more about the differences between both OpenVidu products here: [OpenVidu Meet vs OpenVidu Platform](../openvidu-meet-vs-openvidu-platform.md).

### Am I the right fit for OpenVidu Meet?

**If you are new to OpenVidu**, you may find that OpenVidu Meet is ideal for teams, businesses, and organizations that need a reliable and secure video conferencing solution running on their servers. It is perfect for any use case that falls under the category of "video conferencing application", without the need for extensive custom development. OpenVidu Meet is currently built for the web, with mobile support coming soon.

If your use case requires a high degree of customization, or if you need to build a unique real-time experience that goes beyond the typical video conferencing features, OpenVidu Platform is likely a better fit. It also supports a wider range of platforms, including native mobile and desktop applications.

**If you come from a previous version of OpenVidu** (<= 3.3.0), the most likely scenario is that you will still want to keep using OpenVidu Platform. However, if your application primarily focuses on video conferencing features, you may find that OpenVidu Meet offers a more streamlined and more maintainable solution. We invite you to give OpenVidu Meet a try and see if it aligns with your requirements!

### Future roadmap of OpenVidu Meet

- Mobile platforms embedding (iOS and Android).
- More branding and customization options.
- Locked rooms.
- E2E encryption.
- Live captions.
- AI meeting summaries.
- And much more...

### Get started with OpenVidu Meet

If you want to learn more about OpenVidu Meet, check out the following resources:

- Compare OpenVidu Meet vs OpenVidu Platform: [OpenVidu Meet vs OpenVidu Platform](../openvidu-meet-vs-openvidu-platform.md)
- Launch OpenVidu Meet locally in a couple of minutes: [Try OpenVidu Meet locally](./deployment/local.md)
- Embed OpenVidu Meet into your web app: [OpenVidu Meet Embedded](./embedded/intro.md)

### Patch releases

#### 3.4.1

- **Update authentication methods to use header-based tokens instead of cookies**: when [embedding OpenVidu Meet](../meet/embedded/intro.md), the strategy (`SameSite=Strict`) was causing issues when loading the application and the embedable component from different domains. Using the most permissive cookie policy available (`SameSite=None`) still caused issues in some browsers that block third-party cookies by default. Now OpenVidu Meet avoids cookies and instead uses header-based tokens for authentication, which is more reliable and secure. See [commit 4e80b5a :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-meet/commit/4e80b5a060c1ae0f8942527dbdc6ee221992caab){:target="\_blank"}.