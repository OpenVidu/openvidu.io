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
