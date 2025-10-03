- **Privacy**: you can't afford to let your client's data get out of your reach. OpenVidu allows you to meet all your privacy and regulatory requirements: no data at all is sent to any third-party server. Everything is self-contained on your own servers.
- **Leverage your resources**: your organization has access to its own infrastructure that can be used to host these services. SaaS solutions generally offer complete freedom from infrastructure management, but this comes with generally high prices that cover both the provider's infrastructure and their service surcharge. OpenVidu allows taking full advantage of your own infrastructure, reducing costs and increasing performance.

It is important to mention that when we talk about self-hosting OpenVidu, we don't just mean installing it in bare-metal servers or private VPCs. OpenVidu also supports deployments in the most popular cloud providers, using their native services when possible. **AWS** and **Azure** are currently supported, and others are coming soon. You can learn more about the different options to deploy OpenVidu in the [deployment types](/docs/self-hosting/deployment-types.md) section.

One of OpenVidu's main goals is offering a self-hosted, production-ready live-video platform with all the advanced capabilities typically reserved for SaaS solutions. This includes outstanding **performance**, **scalability**, **fault tolerance** and **observability**:

<div class="grid cards" markdown>

-   :material-lightning-bolt:{ .openvidu-call-feature-icon .middle } __Performance__

    ---

    OpenVidu is built to be incredibly powerful. It is based on the best open source WebRTC stacks: [LiveKit :fontawesome-solid-external-link:{.external-link-icon}](https://livekit.io/){target="\_blank"} and [mediasoup :fontawesome-solid-external-link:{.external-link-icon}](https://mediasoup.org/){target="\_blank"}. By combining the best of both worlds, OpenVidu provides outstanding performance.

    [:octicons-arrow-right-24: Learn more about performance](/docs/self-hosting/production-ready/performance.md)

-   :material-chart-timeline-variant-shimmer:{ .openvidu-call-feature-icon .middle } __Scalability__

    ---

    OpenVidu has been designed from the outset with scalability in mind. Host videoconference rooms and large live streams with hundreds of participants. Autoscale your cluster to adapt to the demand and optimize your resources.

    [:octicons-arrow-right-24: Learn more about scalability](/docs/self-hosting/production-ready/scalability.md)

-   :material-shield-refresh:{ .openvidu-call-feature-icon .middle } __Fault Tolerance__

    ---

    OpenVidu offers fault tolerance in all its components. Deploy a reliable high-availability cluster knowing that if one of your node goes down, others will be able to continue working with no downtime.

    [:octicons-arrow-right-24: Learn more about fault tolerance](/docs/self-hosting/production-ready/fault-tolerance.md)

-   :material-microscope:{ .openvidu-call-feature-icon .middle } __Observability__

    ---

    OpenVidu brings everything necessary to monitor the status, health, load and history of your deployment. It automatically collects events, metrics and logs, and provides [OpenVidu Dashboard](/docs/self-hosting/production-ready/observability/openvidu-dashboard.md) and a [Grafana stack](/docs/self-hosting/production-ready/observability/grafana-stack.md) to navigate them.

    [:octicons-arrow-right-24: Learn more about observability](/docs/self-hosting/production-ready/observability/index.md)

</div>
