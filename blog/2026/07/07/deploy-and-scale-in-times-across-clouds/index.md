# We deployed the same video platform on five clouds and timed it: 5 minutes to 20, and the slow ones are slow for a reason

Mean time to a working deployment, by cloud and topology

"How long does it take to deploy?" sounds like a trivia question until you're the one watching a progress bar, wondering whether it's stuck. So we stopped guessing and measured it.

We built a tool, **ov-cloud-tester**, that deploys the *same* self-hosted WebRTC video stack on all five major clouds — AWS, Azure, Google Cloud, Oracle Cloud and DigitalOcean — in three topologies (single node, elastic, and high-availability), tears it down cleanly, and times the whole thing. We ran it many times per cloud and looked at both the averages *and* every individual run. The headline: standing up a working deployment ranges from about **5 minutes to 20**, DigitalOcean is consistently the fastest and Oracle the heaviest — and the *why*, plus which clouds are actually *predictable*, turns out to be more interesting than the ranking.

TL;DR

- **A single node is ready in ~5–10 minutes on every cloud.** DigitalOcean is quickest (~5.5 min), Oracle slowest (~10 min).
- **DigitalOcean wins because it builds almost nothing first** — a stock droplet, a firewall, an IP. No VPC, IAM, DNS zones or TLS certificates to provision before your server can exist.
- **Oracle does the most** — its elastic and HA deployments stand up a real autoscaler, a load balancer, and a coordinated multi-node cluster before anything is ready. That's a feature, not a bug; it just costs setup time.
- **HA is where clouds diverge hard:** GCP and DigitalOcean are ready in ~6 min, Azure and Oracle in ~11, and AWS averages ~18.
- **But the average lies — look at every run.** AWS HA isn't "18 minutes": it's *either* ~12–13 min *or* ~27, with nothing in between. GCP, by contrast, lands within seconds of itself every time. Predictability is its own metric.
- **"Time to ready" is not "time to provision."** The minutes hide in software boot, DNS, certificates and cluster formation — and that split varies more by cloud than raw VM launch does.
- **Scaling back *down* is the hard direction** — a single node can't do it at all, and elastic/HA have to gracefully *drain* nodes, not kill them. More on why at the end.

## What we measured, and how

Each test is one full **deploy → wait-ready → destroy** cycle, and we time each phase separately from the tool's own logs, so these are wall-clock numbers an operator actually experiences:

- **deploy** — the provisioning step: everything the cloud has to create (via Terraform / CloudFormation / ARM) before the machines exist.
- **wait-ready** — from "the machines exist" to "the deployment's real endpoint answers over HTTP": software boot, install, DNS, certificates, cluster formation.
- **destroy** — tearing it all down again (we run it, but it's not our focus here).

The number that matters is **time to ready = deploy + wait-ready**, and we report the *sum*, because the clouds split that work differently. AWS folds the software install into the deploy step (its CloudFormation stack blocks until the instance signals it's done), while others finish provisioning in seconds and then spend minutes booting before the endpoint responds. Only the sum is a fair comparison.

We ran **each configuration 4–5 times** and averaged — with two honest exceptions: **Oracle's elastic and HA, which we've only completed once each so far** (they're the slowest and priciest to spin up repeatedly), so treat those two cells as provisional. Every number below is real and measured; none is estimated.

The three topologies are genuinely different amounts of infrastructure: a **single node** runs everything on one server; **elastic** adds an autoscaling pool of media nodes; and **high availability (HA)** adds a fault-tolerant cluster of masters behind a load balancer. So it's no surprise HA takes longer — what's interesting is *how much* longer, and how differently each cloud gets there.

## The numbers

Mean time to a working deployment, with the number of runs behind each figure:

| Topology              | DigitalOcean  | GCP           | Azure      | AWS        | Oracle       |
| --------------------- | ------------- | ------------- | ---------- | ---------- | ------------ |
| **Single node**       | **5m31s** (4) | 6m07s (5)     | 6m10s (5)  | 7m24s (5)  | 9m46s (4)    |
| **Elastic**           | **4m21s** (4) | 5m17s (5)     | 5m47s (5)  | 6m56s (5)  | 5m48s (1)\*  |
| **High availability** | 6m03s (4)     | **6m02s** (4) | 10m35s (5) | 18m34s (5) | 11m46s (1)\* |

\* Single run so far — provisional.

For a **single node**, everyone lands in a tight 5–10 minute band; nothing here will hurt you. DigitalOcean is the sprinter, Oracle takes about twice as long. **DigitalOcean is fastest in every topology** (or tied with GCP). The *slowest* changes with the topology: Oracle for a single node, AWS for HA — and those two are slow for very different reasons, which we'll get to.

But before the "why," there's a "how reliably" — and it matters just as much.

## Every run, not just the average

Averages are comforting and occasionally dishonest. Here's every individual run:

Every individual deployment run, by cloud and topology, showing spread around the mean

Three things this shows that the table can't:

- **AWS HA is bimodal, and its average is a lie.** It isn't "18 minutes" — it's *either* ~12–13 minutes *or* ~27, in two tight clusters with nothing between them. The mean (that vertical tick) lands in the empty gap where **no run actually happened**. If you provision AWS HA, you'll likely get one of two very different experiences, and the headline number predicts neither.
- **GCP is the most predictable cloud by a wide margin.** Its elastic runs land within ~13 seconds of each other, its HA runs within ~26. When GCP says ~6 minutes, it means ~6 minutes, every time. For anything that deploys on a schedule — CI, blue-green rollouts, disaster-recovery drills — that consistency is worth as much as raw speed.
- **One slow run can drag a whole average.** Oracle's single node is usually ~8m50s, but one run out of four hit 12m34s and pulled the reported mean up to ~9m46s. DigitalOcean, by contrast, is both fast *and* tight — its dots cluster hard on the left in every panel.

The takeaway: when you benchmark deploys, don't trust a single average. A cloud that's fast on paper but swings by 15 minutes run-to-run is a cloud you can't build automation around.

## Why DigitalOcean is the fastest

DigitalOcean wins by asking the cloud to do almost nothing before your server exists. A single-node deploy is essentially **one stock Ubuntu droplet, one firewall, a floating IP, and an object-storage bucket** — and that's it. There's no VPC to carve out, no subnets or gateways or route tables, no IAM roles, no DNS zone, no TLS certificate to issue and validate before the box can come up. That scaffolding is exactly what makes the hyperscalers slower, and DigitalOcean simply doesn't have most of it.

Three details do the heavy lifting:

- **Stock droplets boot in seconds.** Every node is a plain Ubuntu image with the install driven by cloud-init — no custom image-baking pipeline to wait on.
- **It names itself, so there's no DNS to wait for.** With no custom domain, the box derives its own hostname from its public IP via [sslip.io](https://sslip.io) — which resolves instantly, so there's no DNS-propagation delay before the endpoint answers.
- **Terraform doesn't sit and wait.** The DigitalOcean config has no blocking "wait for the app to finish installing" gate, so provisioning returns as soon as the droplets are booted. (AWS CloudFormation, by contrast, literally pauses the stack on a *wait condition* until the instance signals it's ready — and the HA template has four of them.)

Even the bigger topologies stay lean: elastic scales with a small serverless function instead of a managed autoscaling group, and HA uses a plain layer-4 network load balancer that just forwards packets — so there's no certificate for the balancer to validate before traffic can flow.

The honest caveat

DigitalOcean doesn't make the actual OpenVidu install any faster — pulling the Docker images takes the same time on every cloud. What it does is minimize *everything around* the install: the provisioning, the networking, the DNS, the certificates. That's the whole trick.

## Why Oracle does the most

Oracle is the mirror image, and it's worth being fair here: it isn't slow because it's inefficient, it's slow because it genuinely builds *more*.

Even a **single node** starts from further back. Before Oracle launches that one VM, it provisions a whole private network — a VCN, internet gateway, route table, security list, subnet, and a network security group with its rules — plus a dynamic group and IAM policy and a KMS vault for secrets. Then every Oracle machine pays a boot-time tax the others don't: it installs the full Oracle command-line tool at startup and then *waits* for two Oracle-specific delays — IAM permission propagation, and the secret-vault's DNS actually becoming resolvable (Oracle reports both "ready" before they truly are). That's why Oracle's single node provisions in under a minute but takes ~10 to answer: the VM is up fast, the plumbing around it isn't.

**Elastic** adds real machinery: an instance-pool template, the pool itself, an autoscaler, and an entire serverless Function stack — with its own permissions and logging — that exists specifically to handle scaling *in*. **HA** goes furthest: instead of one master it launches **four**, behind a **network load balancer**, and those four masters have to *find each other and boot as a coordinated cluster* (a MongoDB replica set with Redis failover) before any of them is ready. Each master waits for the others; the media nodes wait for all the masters.

That's a lot of moving parts, and it's exactly why we've only managed one complete elastic and one complete HA run on Oracle so far — they take the longest and cost the most to stand up repeatedly. What we can say firmly is structural: Oracle's heavier topologies do strictly more work than anyone else's, and its one HA run (~11m46s) sits among the slowest. You're not waiting on slow servers — you're waiting on a genuinely bigger system assembling itself.

## Why AWS HA swings so wildly

AWS single node and elastic are middle-of-the-pack and consistent. HA is the outlier — and the reason isn't the network, it's the *order* in which the cluster comes up.

HA is the only topology with more than one master, and AWS brings its four masters up **in sequence, not in parallel**. Master 2 doesn't start until master 1 is fully healthy — booted, with OpenVidu installed and answering — then master 3 waits on master 2, and master 4 on master 3. There's no parallel bring-up with the already-created nodes coordinating as they go; it's a serial chain, each link gated on the previous one reporting healthy. So instead of installs running side by side, you pay for **four of them end to end**.

That serial chain explains both halves of AWS HA's behaviour. It's slow, because four full installs in a row simply take a while. And it's *unpredictable*, because a chain is only as fast as its slowest link — if any single master drags on its install, every master behind it waits. That's the ~12-or-~27 split from the chart above: a clean run threads all four masters in about 12–13 minutes, and a run where one of them stalls pulls the whole line out toward 27.

The transferable lesson

"Time to ready" is not "time to provision." On DigitalOcean the VM exists in seconds and the wait is the software install; on Oracle single node the VM is instant but the vault plumbing is slow; on AWS HA the masters install one after another instead of together. If you only benchmark "how fast does the VM launch," you'll be surprised by your own deploys — measure the whole thing, several times.

## What about scaling back *down*?

Deploying is only half the job. The other direction — scaling back *down* when the crowd leaves — is the genuinely hard one, and it already has [a post of its own](https://openvidu.io/blog/2026/05/26/scale-in-problem-in-videoconferences/index.md). The short version: you can't just kill a media node that has live meetings on it. You have to *drain* it — stop sending it new rooms, let the calls already on it finish, and only then let the cloud reclaim the machine. Terminate it early and you drop everyone mid-sentence.

Two things are worth knowing before you get there:

- **A single node doesn't scale in at all.** There's nothing to remove — it's one server. Scaling in only applies to the **elastic** and **HA** topologies, the ones with an autoscaling media tier.
- **The topology changes how you deploy, not how a node drains.** Whether there's one master or four in front of it, the media node being removed drains in exactly the same way — so scaling in behaves identically in elastic and HA.

Deploying, it turns out, is the easy half. Taking a cluster back down *without anyone noticing* is the part worth losing sleep over.

## Conclusion

Deploying a self-hosted video platform is a solved problem on every major cloud — but "solved" doesn't mean "identical," and it doesn't even mean "consistent." A single node is a 5-to-10-minute affair anywhere. Reach for high availability and the spread widens dramatically, and the reasons are legible if you look at what each cloud actually builds: DigitalOcean stays fast (and remarkably steady) by provisioning almost nothing around the server, Oracle takes its time because its elastic and HA deployments stand up a real autoscaler, load balancer and coordinated cluster, and AWS's HA clock swings between ~12 and ~27 minutes because it brings its four masters up one after another, each waiting for the previous to be fully healthy.

The practical takeaway is two-fold: **benchmark the topology you'll actually run, on the cloud you'll actually use — and run it more than once**, because time-to-provision and time-to-ready are different numbers, and the average of a handful of runs can hide a cloud that's quietly unpredictable.

All of these deployments — single node, elastic and HA, on all five clouds — ship as ready-made infrastructure with [OpenVidu](https://openvidu.io/); the numbers here came from deploying exactly those, over and over. If you want to run your own stopwatch, the [self-hosting deployment guides](https://openvidu.io/latest/docs/self-hosting/deployment-types/index.md) are the place to start — pick the topology that fits your traffic, and now you know roughly how long to expect the coffee break to be.
