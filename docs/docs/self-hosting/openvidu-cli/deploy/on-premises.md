---
title: "Deploy OpenVidu on your servers with the CLI"
description: "Deploy OpenVidu Community or PRO on your own Linux servers over SSH or on the machine itself, from Single Node to Elastic and High Availability."
page_features: [lazyvideo]
---

# Deploy OpenVidu on premises with the OpenVidu CLI

Deploy OpenVidu on your own Linux servers. `ov` installs and starts the stack over SSH or on the machine it runs on, generating every credential, and leaves a copy of itself on each node so the stack can be operated from there too, as well as from the stack's directory on your machine.

<!-- VIDEO: deploy-on-premises.mp4 (docs-video) -->

Community runs on Docker Compose and a systemd unit; PRO runs on Kubernetes. **The edition is the whole decision** — `--edition community` (the default) or `--edition pro` — and how OpenVidu is installed and run on the server follows from it. Elastic and High Availability grow past one machine, so they are PRO only.

## Requirements

- One or more **Linux servers** with a sudo-capable user, reachable over SSH (and, for Elastic and High Availability, reachable from each other on their private addresses).
- A **domain** pointing at the server (at a load balancer in front of the masters, for HA in production), and a **certificate type**:
    - `letsencrypt` or `zerossl` — a certificate obtained automatically (needs port 80 reachable).
    - `owncert` — bring your own, with `--owncert-public-key` and `--owncert-private-key`.
    - `selfsigned` — for a throwaway.
- The [ports OpenVidu needs](../operate/status.md#check-the-ports) reachable. Required: `443/tcp`, and `22/tcp` for `ov` itself. Recommended, because media is relayed over TURN on 443 without them, at a cost in latency and quality: `443/udp`, `7881/tcp` and the media range `50000-60000/udp`; and `80/tcp`, which `letsencrypt` and `zerossl` need to obtain the certificate. With the `ingress` module, `1935/tcp` and `7885/udp`. On PRO, also the cluster API on `6443/tcp` from your machine, and the node's own firewall must let the pod networks `10.42.0.0/16` and `10.43.0.0/16` reach it. Between the nodes of an Elastic or High Availability stack, `6443/tcp`, `10250/tcp` and `8472/udp` (and `2379-2380/tcp` between HA masters). See the port check below.
- The [OpenVidu CLI](../install.md). Nothing else needs to be pre-installed on the servers: the deploy brings Docker and the Compose plugin (Community) or the OpenVidu node agent (PRO) when they are missing.
- For PRO, your **OpenVidu Pro license** (`--openvidu-pro-license`).

## Check the ports first

The commonest way an on-premises OpenVidu "does not work" is a stack that comes up perfectly and has no media: every service healthy, and UDP never reaching the node. `ov stack check-ports` finds that in seconds, **before deploying anything**, by running a temporary listener on the node and probing it — which verifies TCP *and* UDP, something dialling a running stack cannot do.

```console
$ ov stack check-ports --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 \
    --domain-name 172-30-0-96.openvidu-local.dev
checking the inbound ports of 172.30.0.96…
read-node: reading what is already bound and what the firewall allows
listener: the node's python3 is holding 9 port(s) for us
probe: probing 172-30-0-96.openvidu-local.dev: 3 TCP, 6 UDP
checked in 4.6s
Inbound ports of 172-30-0-96.openvidu-local.dev (172.30.0.96)
  state     fresh — nothing of ours is deployed here, so every port was free to measure
  method    a temporary listener on the node (its own python3; nothing written to disk)
  verdict   3 of 6 checked port(s) do NOT reach the node: 443/udp, 50000-60000/udp, 7881/tcp

Required
  the stack does not work without these
  ✓ 443/tcp           open
      Caddy — the probe arrived at the node — the whole path is open
  ✓ 22/tcp            open
      SSH — ov is connected to the node over SSH

Recommended
  it works without these, but every call is worse
  ! 443/udp           dropped · host-firewall
      OpenVidu LiveKit Server — the ufw firewall on the node drops it (deny (incoming), allow (outgoing), allow (routed))
      Participants behind restrictive networks are relayed over TURN/TLS on 443/tcp instead of UDP.
      fix (on the node): sudo ufw allow 443/udp
  ! 50000-60000/udp   dropped · host-firewall
      OpenVidu LiveKit Server — the ufw firewall on the node drops it (deny (incoming), allow (outgoing), allow (routed)) [sampled: 50000, 52500, 55000, 57500, 60000]
      Media is relayed through TURN on 443, which adds latency and load and lowers quality under load.
      fix (on the node): sudo ufw allow 50000:60000/udp
  ! 7881/tcp          dropped · host-firewall
      OpenVidu LiveKit Server — the ufw firewall on the node drops it (deny (incoming), allow (outgoing), allow (routed))
      Media is relayed through TURN on 443, which adds latency and load and lowers quality under load.
      fix (on the node): sudo ufw allow 7881/tcp
  ✓ 80/tcp            open
      Caddy — the probe arrived at the node — the whole path is open
…
```

The fix is printed, never run: `ov` reads firewalls, it does not change them. Here only recommended ports fail, so the check warns and exits `0`; a required port that fails exits `8`. The report goes on to check the DNS name and that the node reaches the registries the deploy pulls from. The same check runs automatically before every remote deploy (`--skip-port-check` turns it off). See [Status and health checks](../operate/status.md#check-the-ports) for the full report and its options.

## Deploy

An empty directory on your machine is the stack. Pick the edition and topology. The examples use a domain that resolves to a private address, so they bring their own certificate (`owncert`; a path to a PEM file, a base64 PEM or the PEM itself). On a server reachable from the internet on port 80, `--certificate-type letsencrypt` obtains one automatically, and `selfsigned` is enough for a throwaway.

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```console
    $ mkdir ov-ce && cd ov-ce
    $ ov stack deploy web \
      --environment on-premises \
      --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 \
      --domain-name 172-30-0-96.openvidu-local.dev \
      --certificate-type owncert \
      --owncert-public-key fullchain.pem --owncert-private-key privkey.pem \
      --mode auto
    note: generated 11 credential(s) and pinned them in this stack's spec, so a later deploy reuses them instead of replacing them: livekit-api-key, livekit-api-secret, redis-password, minio-access-key, minio-secret-key, mongo-admin-password, mongo-replica-set-key, dashboard-admin-password, grafana-admin-password, meet-initial-admin-password, meet-initial-api-key
    checking the inbound ports before installing anything…
      Ports of 172.30.0.96 (Community single node)
      PORT             SCOPE   LEVEL        STATE  TO OPEN
      443/tcp          public  required     open
      443/udp          public  recommended  open
      80/tcp           public  recommended  open
      50000-60000/udp  public  recommended  open
      7881/tcp         public  recommended  open
      22/tcp           admin   required     open
      all 6 checked port(s) arrive at the node
    ✓ [172.30.0.96 single] if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then echo 'docker and the compose plugin are already installed'; else curl -fsSL https://get.docker.com -o /tmp/get-docker.sh && sh /tmp/get-docker.sh && rm -f /tmp/get-docker.sh; fi && systemctl enable --now docker
    ✓ [172.30.0.96 single] write 44 files to /opt/openvidu (docker-compose.yaml, config/, .ov/base/)
    ✓ [172.30.0.96 single] write 2 host files (/etc/systemd/system/openvidu.service, /etc/sysctl.d/50-openvidu.conf)
    ✓ [172.30.0.96 single] sysctl -q -p /etc/sysctl.d/50-openvidu.conf || echo 'note: the sysctl settings could not be applied now; they apply at boot'; systemctl daemon-reload && systemctl enable openvidu
    ✓ [172.30.0.96 single] install this CLI at /usr/local/bin/ov
    ✓ [172.30.0.96 single] render config/ into data/runtime/ (ov stack render) — 21 created, 0 updated, 1 unchanged, 0 removed
    ✓ [172.30.0.96 single] docker compose --env-file data/runtime/compose.env pull --quiet
    ✓ [172.30.0.96 single] systemctl restart openvidu
    deploy completed successfully
    wrote spec to openvidu-stack.yml
    ✔ stack "web" recorded in this directory
    ✔ published /opt/openvidu/stack/context.yaml (recover this stack's directory elsewhere with `ov stack import --ssh ubuntu@<host>`)
    ✔ the node operates this stack itself (`sudo ov stack status` there)
    waiting for OpenVidu to be ready on the node (Ctrl-C to stop waiting; the deployment keeps running)…
      ⏳ still starting: caddy, openvidu, dashboard, meet, grafana (0s)
      ⏳ still starting: openvidu, dashboard, meet, grafana (5s)
      ⏳ still starting: openvidu, dashboard, meet (10s)
      ⏳ still starting: openvidu (15s)
    ✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet, grafana)

    Inbound ports
      all 6 checked port(s) arrive at the node
      measured from the node's own network: this says nothing about the internet path
      full report: ov stack check-ports
    ```

    Plain Docker Compose and a systemd unit: no installer image, no operator. The ports are checked before anything is installed, and every credential is generated and **pinned** into the spec, so a later deploy reuses them instead of locking the stack out of its data.


=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The only difference from Community is `--edition pro` and the license; everything else follows from it.

    ```console
    $ mkdir ov-pro && cd ov-pro
    $ ov stack deploy prod \
      --edition pro --environment on-premises \
      --ssh ubuntu@172.30.0.101 --ssh-key ~/.ssh/id_ed25519 \
      --openvidu-pro-license <your-license> \
      --domain-name 172-30-0-101.openvidu-local.dev \
      --certificate-type owncert --owncert-public-key fullchain.pem --owncert-private-key privkey.pem \
      --mode auto

    ▶ Connect to the VM…
       · open an SSH session and check root/sudo access
       ✓ Connect to the VM

    ▶ Check the inbound ports…
       · bind the ports on the node and probe them from here (nothing is installed yet, so UDP is verifiable)
           Ports of 172.30.0.101 (Pro single node)
           PORT             SCOPE   LEVEL        STATE  TO OPEN
           443/tcp          public  required     open
           443/udp          public  recommended  open
           80/tcp           public  recommended  open
           50000-60000/udp  public  recommended  open
           7881/tcp         public  recommended  open
           6443/tcp         admin   required     open
           22/tcp           admin   required     open
           ✓ host firewall: the ufw firewall lets 10.42.0.0/16 and 10.43.0.0/16 reach the node
       ✓ Check the inbound ports

    ▶ Install the OpenVidu node agent…
       · upload the OpenVidu node-agent installer
       · run the node agent installer (k3s v1.36.4+k3s1)
       ✓ Install the OpenVidu node agent

    ▶ Deploy OpenVidu…
       · fetch the node's credentials
       · read the stack's configuration
       · generate the deployment
       · write the stack values (domain, TLS, modules, credentials)
       · create the configuration documents (openvidu.yaml and the service files)
       · install OpenVidu (reusing the existing credentials on a redeploy)
       ✓ Deploy OpenVidu

    ▶ Leave the OpenVidu CLI on the node…
       · copy this CLI (ov-admin, 63 MB) to /usr/local/bin/ov
       · give the node its own stack directory
       ✓ Leave the OpenVidu CLI on the node

    ▶ Check access from outside…
       · reach https://172-30-0-101.openvidu-local.dev/ (services may still be starting)
       ✓ Check access from outside

    ✔ deploy completed.
    wrote spec to openvidu-stack.yml
    ✔ stack "prod" recorded in this directory

    Inbound ports
      all 7 checked port(s) arrive at the node
      measured from the node's own network: this says nothing about the internet path
      full report: ov stack check-ports
    ```

    Kubernetes, with OpenVidu as a Helm release. The node needs nothing pre-installed: the node agent and the software it installs come inside `ov`. Services come up over a few minutes after the deploy returns; [`ov stack status --wait`](../operate/status.md) blocks until they are ready.

=== "Elastic **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    An Elastic stack is **deployed on one machine** (the master) with `--deployment-type elastic`, exactly as a Single Node PRO; every media node then **joins** it.

    ```console
    $ mkdir ov-elastic && cd ov-elastic
    $ ov stack deploy el --edition pro --environment on-premises --deployment-type elastic \
        --ssh ubuntu@172.30.0.101 --ssh-key ~/.ssh/id_ed25519 \
        --openvidu-pro-license <your-license> \
        --domain-name 172-30-0-101.openvidu-local.dev \
        --certificate-type owncert --owncert-public-key fullchain.pem --owncert-private-key privkey.pem \
        --mode auto

    ▶ Connect to the VM…
       · open an SSH session and check root/sudo access
       ✓ Connect to the VM

    ▶ Check the inbound ports…
       · bind the ports on the node and probe them from here (nothing is installed yet, so UDP is verifiable)
           Ports of 172.30.0.101 (master node of an elastic stack)
           PORT      SCOPE   LEVEL        STATE  TO OPEN
           443/tcp   public  required     open
           80/tcp    public  recommended  open
           6443/tcp  admin   required     open
           22/tcp    admin   required     open
           ✓ host firewall: the ufw firewall lets 10.42.0.0/16 and 10.43.0.0/16 reach the node
       ✓ Check the inbound ports

    …

    ✔ deploy completed.
    wrote spec to openvidu-stack.yml
    ✔ stack "el" recorded in this directory

    Inbound ports
      all 4 checked port(s) arrive at the node
      measured from the node's own network: this says nothing about the internet path
      full report: ov stack check-ports
    ```

    The stack is up with its data tier on the master, but its media services have nowhere to run yet. Join a media node from the same directory:

    ```console
    $ ov stack join --ssh ubuntu@172.30.0.102 --as media
    → reading the join address and token from 172.30.0.101
    → checking the ports of 172.30.0.102 from here and from the stack's masters
      Ports of 172.30.0.102 (media node of an elastic stack)
      PORT                      SCOPE     LEVEL        STATE  TO OPEN
      443/udp                   public    recommended  open
      50000-60000/udp           public    recommended  open
      7881/tcp                  public    recommended  open
      22/tcp                    admin     required     open
      10250/tcp ← 172.30.0.101  internal  required     open   (only from 172.30.0.101)
      8472/udp ← 172.30.0.101   internal  required     open   (only from 172.30.0.101)

      Ports of 172.30.0.101 (reached from 172.30.0.102)
      PORT                  SCOPE     LEVEL     STATE       TO OPEN
      6443/tcp ← this node  internal  required  open
      8472/udp ← this node  internal  required  unverified
      ✓ host firewall: the ufw firewall lets 10.42.0.0/16 and 10.43.0.0/16 reach the node

    ▶ Connect…
       · check root/sudo access on 172.30.0.102
       ✓ Connect

    ▶ Join the cluster…
       · upload the OpenVidu node-agent installer
       · join 172.30.0.102 to the stack as a media node
       ✓ Join the cluster

    ▶ Leave the OpenVidu CLI on the node…
       · copy this CLI (ov-admin, 63 MB) to /usr/local/bin/ov
       ✓ Leave the OpenVidu CLI on the node

    ▶ Wait for the stack to see the node…
       · wait until fake-vm-172-30-0-102 is ready in the stack
       ✓ Wait for the stack to see the node

    ✔ 172.30.0.102 joined the stack as a media node.
    ```

    `ov` reads the join address and token from the master over SSH and logs into the new server with the same user, key and port (the token never appears on screen). Before installing anything it checks the ports the new node needs, from your machine and from the masters: a required internal port that does not arrive stops the join with exit `6` and the `ufw` rule to add on each side. Each media node is one more `ov stack join --ssh`. See [Scaling](../operate/scaling.md).

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    High Availability is four masters plus one or more media nodes. Deploy the first master with `--deployment-type ha` (as the Elastic tab, with `ha`), then join three more as masters and the media nodes:

    ```bash
    ov stack join --ssh ubuntu@172.30.0.97 --as master
    ov stack join --ssh ubuntu@172.30.0.98 --as master
    ov stack join --ssh ubuntu@172.30.0.99 --as master
    ov stack join --ssh ubuntu@172.30.0.100 --as media
    ```

    <!-- PENDING-RUN (docs-ov): on-premises pro ha joins output -->

    A master join takes the stack's domain from the directory; `--lb-host` names the load balancer in front of the masters and `--public-ip` the server's public address, both kept reachable on the cluster API. As the masters join, Redis Sentinel, the MongoDB replica set, MinIO and the clustered Loki and Mimir spread one replica per master. `join` refuses what the stack has no place for before touching any server: `--as master` on an Elastic stack, any join to a single node, and any join to a Community stack. See [Scaling](../operate/scaling.md).

### The port preflight

Before anything is installed, a remote deploy binds the node's ports with a temporary listener and probes them, and prints a table of them (`checking the inbound ports before installing anything…` in the output above). A **required** port closed (or, on PRO, the node's firewall dropping the pod and service networks) stops the deploy with **exit code 6** and the exact rule to add for the detected firewall. A recommended port only warns and the deploy continues. `--skip-port-check` deploys without the check; `--this-node` skips it by construction (reachability cannot be verified from the node itself).

### Deploying again

A deploy to a node that already runs OpenVidu says so and keeps its data: it rewrites `docker-compose.yaml` and `config/` from the spec (your `docker-compose.override.yaml` stays) and reuses the credentials the data was written with:

```text
172.30.0.96 already runs OpenVidu on 172-30-0-96.openvidu-local.dev (currently stopped). Deploying again rewrites its files from the spec and restarts it.
  · Its docker-compose.yaml and config/ are rewritten from the spec you are deploying; docker-compose.override.yaml is kept.
  · Its data is kept — nothing deletes MongoDB, MinIO or recordings.
  · The credentials in your spec are reused, so the kept data stays readable.
```

A deploy from a directory whose spec already exists needs the mode named (`--mode auto` or `--mode assisted`).

## Install on the server itself

Instead of `--ssh`, put `ov` on the server, log in, and deploy with **`--this-node`** — *the machine I am running on*. The CLI writes the deployment there and escalates with `sudo`, so a user with passwordless sudo is enough. The stack of `--this-node` lives in `/opt/openvidu/stack`:

```console
$ sudo ov stack deploy web --environment on-premises --this-node \
  --domain-name 172-30-0-96.openvidu-local.dev \
  --certificate-type selfsigned
…
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard)
```

Either way the server ends up operable from itself: a deploy from your laptop hands the node the CLI and its own stack directory on the way out, so `sudo ov stack status` works there with no directory to name.

## Review the commands first: assisted mode

`--mode assisted` runs **nothing** on the server. It writes the same files and prints the same commands, step by step, for you to review and run yourself.

## Next steps

- [Check the status](../operate/status.md) and run the health check.
- [Change the configuration](../operate/configuration.md) or [the modules](../operate/modules.md).
- [Scale the media nodes](../operate/scaling.md) of an Elastic or HA stack.
- [Operate the stack from another machine](../operate/remote.md).
- The full [command reference](../reference.md).
