---
draft: true
date: 2026-03-09
categories:
 - No OV - Tecnología; WebRTC / MoQ / RTMP / …
authors:
 - sergio
hide:
 - navigation
 - search-bar
 - version-selector
---

# Scaling Up is easy, hell is Scaling Down: The Scale-In problem in videoconferences.

Autoscaling is one of the killer features of cloud infrastructure. It promises zero-waste elasticity: when demand rises, you spin up more nodes; when demand drops, you shut them down and stop paying for them. For most cloud workloads, this works beautifully. But for real-time media platforms — videoconferencing systems built on top of media servers — the "shut them down" part is far more dangerous than it first appears.

<!-- more -->

This post dives into the **scale-in problem**: why you can't simply terminate a media server node that has active meetings running inside it, how the broader cloud industry has addressed it, and how OpenVidu implements a robust solution across AWS, Azure and GCP.

## The Scaling Illusion: Why "Turning it Off" is Harder than "Turning it On"

Scaling _out_ is easy. Your CPU climbs past the alarm threshold, your autoscaling policy fires, a new VM boots, and within a couple of minutes it joins the pool and starts sharing the load. The system designer gets to feel clever.

Scaling _in_ is where the illusion shatters. Your CPU drops, the policy fires in reverse, and the cloud provider picks a node to terminate. If that node is running a web server, this is fine — kill it, redirect traffic, done. If that node is hosting eight simultaneous videoconferences, you have just murdered forty people's calls mid-sentence.

The asymmetry runs deeper than just "be careful". Scale-out is a purely additive operation: you are adding capacity to a cluster that continues to work normally. Scale-in is a destructive operation performed against a live system. Getting it wrong doesn't generate a 5xx error you can retry — it breaks a human experience that cannot be rewound.

## The "Stateful" Trap: Why Media Servers Aren't Web Servers

The reason scale-in is so dangerous for videoconferencing comes down to one word: **state**.

A web server (or an API gateway, a GraphQL endpoint, a static file server) is fundamentally stateless. Each request arrives, is processed independently, and the response is sent back. If the server handling your HTTP request disappears mid-flight, the client simply retries on another server and nothing is lost. The server holds no lasting obligation to any client.

A media server is the opposite. When a Room starts, the media server becomes the _anchor_ of that meeting. Each participant's WebRTC connection is established _directly to that specific node_. It manages the routing of hundreds of audio and video tracks. It may be recording the session. It may be running live transcription. The entire communication fabric of the Room hangs off that single machine.

### You can't kill a node while people are talking

This is the hard constraint. When participants join a videoconference, their devices negotiate a WebRTC connection with the media server and exchange ICE candidates, DTLS certificates and SRTP keys specific to that server. There is no transparent "session migration" in WebRTC — you cannot pick up an existing connection and silently hand it to a different server the way a TCP load balancer can reassign a connection after a reconnect.

If the media server node disappears, every participant in every Room hosted on that node gets disconnected simultaneously. From a user's perspective there is no graceful degradation: the call simply ends without warning.

This is the constraint that makes scale-in in videoconferencing non-trivial. You can't kill the node. You have to wait for it to become empty first.

## The "Draining" Strategy: Architecture for a Graceful Exit

The solution that the industry has converged on is called **draining** (sometimes "graceful shutdown" or "cordon-and-drain", borrowing Kubernetes vocabulary).

The idea is straightforward:

1. **Mark the node as draining.** This signals to the rest of the cluster that this node should not receive any new work: no new Rooms, no new Egress recordings, no new Ingress ingest jobs.
2. **Let existing work finish naturally.** Active Rooms and jobs continue uninterrupted. Participants don't notice anything.
3. **Terminate the node once it is empty.** When the last Room ends and the last job completes, the node has zero active load and can be safely shut down.

The challenge is integrating this logic with the autoscaling mechanisms of each cloud provider, all of which have their own opinions about how termination should work.

## Bringing Scale-In to the Major Clouds

OpenVidu implements the draining strategy on every cloud it supports. The approach differs per provider because each exposes different primitives for intercepting a termination decision.

### 1. AWS: Intercepting Scale-In with Lifecycle Hooks

[AWS Auto Scaling Groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html){:target="_blank"} support a native feature called [**Lifecycle Hooks**](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html){:target="_blank"}. When the ASG decides to terminate an instance (because CPU has dropped below the target), instead of killing it immediately it puts the instance in a `Terminating:Wait` state and fires a lifecycle transition event. The instance stays alive in this pending state until something either completes the hook or the wait timeout expires.

OpenVidu uses this hook as its scale-in interception point:

1. The ASG signals termination → instance enters `Terminating:Wait`.
2. OpenVidu's internal logic receives the event and **stops the node from accepting new Rooms, Egress and Ingress**.
3. The node continues serving its existing sessions normally.
4. When the last active job finishes, OpenVidu programmatically completes the lifecycle hook.
5. The ASG moves the instance to `Terminating:Proceed` and terminates it cleanly.

Of the three clouds, this is the most direct implementation. The Lifecycle Hook mechanism was purpose-built for exactly this kind of scenario, so AWS introduces the least friction: there is no need to protect instances manually or coordinate a separate runbook. AWS gives you a configurable timeout (set generously enough to outlast even long meetings) and OpenVidu simply completes the hook when the node is ready.

### 2. Azure: Orchestrating Virtual Machine Scale Sets (VMSS)

Azure's native scale-in mechanism for [Virtual Machine Scale Sets (VMSS)](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview){:target="_blank"} is a [**termination notification**](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-terminate-notification){:target="_blank"}: when a scale-in event fires, Azure notifies the instance and gives it up to **15 minutes** to wrap up — after that, it terminates the VM regardless of what is running inside. Unlike the AWS Lifecycle Hook, this ceiling is hard and cannot be extended. A business meeting can easily last longer than 15 minutes, so relying on this native feature alone would still risk disrupting active sessions.

To work around it, OpenVidu takes a more active stance and bypasses the native scale-in policy altogether:

1. **All Media Node instances are protected from automatic termination** by default. Azure VMSS cannot kill them unilaterally.
2. A custom [**Automation Account runbook**](https://learn.microsoft.com/en-us/azure/automation/automation-runbook-types){:target="_blank"} is used instead of relying on the native scale-in policy. When the system determines a node should be removed, the runbook is triggered, determines the target instance, and sends a [**Run Command**](https://learn.microsoft.com/en-us/azure/virtual-machines/run-command-overview){:target="_blank"} to execute the graceful shutdown script directly on that node. At this point the runbook's job is done and it exits.
3. The **graceful shutdown script, now running on the node itself**, stops it from accepting any new Rooms, Egress or Ingress jobs, and then waits for all active work to finish.
4. Once the node is empty, the shutdown script **deletes the instance from the VMSS**, taking care of its own removal without any further coordination from the runbook.

The trade-off is a **latency of up to 5 minutes** between the moment an instance is flagged and the moment the graceful shutdown actually begins (an Azure platform constraint). But there is no hard ceiling on how long a session can run — a 2-hour board meeting will complete without disruption.

### 3. Google Cloud (GCP): Precision with Managed Instance Groups (MIGs)

[GCP Managed Instance Groups](https://cloud.google.com/compute/docs/instance-groups){:target="_blank"} don't provide a native "wait for draining" hook at the level of a single instance in the same way AWS does. OpenVidu's approach here is to sidestep the native scale-in mechanism entirely:

1. The MIG is configured for **scale-out only**. GCP autoscaling can add instances but will never directly terminate one.
2. A [**Cloud Run Function**](https://cloud.google.com/functions){target="\_blank"}, triggered on a schedule by [Cloud Scheduler](https://cloud.google.com/scheduler/docs){target="\_blank"}, periodically compares the current MIG size with the current recommended size (i.e., how many nodes the autoscaler _would_ request given load). If the current count exceeds the target, it calculates the excess instances and removes them from the MIG.
3. Removed instances don't die immediately. Each Media Node runs a **cron job every minute** that checks whether it is still registered in the MIG. If it detects that it has been removed, it invokes the graceful shutdown script.
4. The shutdown script marks the node as draining, waits for all active Rooms and jobs to complete, and then terminates the process — letting GCP reclaim the VM.

This approach gives OpenVidu full control over the termination decision and timeline, at the cost of some added complexity in the coordination layer.

## Conclusion: If you aren't scaling down, you aren't truly in the Cloud.

Cloud elasticity is only half-useful if you can only scale in one direction. A cluster that grows under load but can never shrink is just an expensive fixed-size deployment with a complicated launch ceremony. And for a real-time media platform, the cost of getting it wrong isn't a slow API or a retried request — it's forty people staring at a frozen screen wondering what just happened.

Scale-in for media servers isn't a flag you flip. It requires understanding that your nodes are stateful, that WebRTC sessions cannot be migrated transparently, and that the only safe termination is a node that has been fully drained. Each cloud provider exposes different primitives for intercepting a termination decision, which means each solution comes with its own trade-offs:

| Cloud | Mechanism | Pros | Cons |
|---|---|---|---|
| :material-aws: [**AWS**](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html){:target="_blank"} | ASG Lifecycle Hooks | Native first-class support. No need to protect instances or run external runbooks. Configurable timeout. | — |
| :material-microsoft-azure: [**Azure**](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview){:target="_blank"} | VMSS instance protection + Automation Account runbook + Run Command | No hard ceiling on session duration. Node drives its own removal. | Up to 5 min latency before graceful shutdown begins. More moving parts to deploy. |
| :material-google-cloud: [**GCP**](https://cloud.google.com/compute/docs/instance-groups){:target="_blank"} | Scale-out-only MIG + Cloud Run Function + per-node cron job | Full control over which instance is selected and when. No dependency on provider-level termination hooks. | Polling-based coordination (1-min cron). Slightly higher complexity in the coordination layer. |
| <span style="white-space:nowrap">:material-digital-ocean: [**DigitalOcean**](https://docs.digitalocean.com/products/droplets/){:target="_blank"}</span> | _(Autoscaling not yet supported)_ | Fixed-size pool; simple to reason about. | No automatic scale-in. Pool size must be managed manually. |
| :custom-oracle-cloud-infrastructure: [**OCI**](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/creatinginstancepool.htm){:target="_blank"} | _(Coming soon)_ | — | — |

Ask yourself: does your current videoconferencing infrastructure actually scale down? If the answer is "I'm not sure" or "we just set the minimum to something safe", you are paying for idle nodes every single night, every weekend, every off-peak hour.

In OpenVidu, graceful scale-in is solved out of the box. Whether you deploy on AWS, Azure or GCP, the autoscaling configuration ships with a strategy that guarantees no active Room is ever disrupted by a scale-down event. Your cloud bill shrinks during quiet hours. Your users never notice a thing.

**Ready to deploy a videoconferencing infrastructure that actually scales in both directions?** Check out the [OpenVidu self-hosting docs](../../docs/self-hosting/deployment-types.md) and see how far you can go.