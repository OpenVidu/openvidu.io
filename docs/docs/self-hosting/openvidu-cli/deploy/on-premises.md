---
title: "Deploy OpenVidu on premises with the OpenVidu CLI"
description: "Deploy OpenVidu Community or PRO on your own Linux servers over SSH or on the machine itself, from Single Node to Elastic and High Availability."
page_features: [lazyvideo]
---

# Deploy OpenVidu on premises with the OpenVidu CLI

Deploy OpenVidu on your own Linux servers. `ov` installs and starts the stack over SSH, or on the machine it runs on, and generates every credential. It also leaves a copy of itself on each node, so you can operate the stack from the node as well as from the stack's directory on your machine.

Community runs on Docker Compose and a systemd unit; PRO runs on Kubernetes. **The edition is the only decision you make**: `--edition community` (the default) or `--edition pro`. How OpenVidu is installed and run on the server follows from it. Elastic and High Availability span more than one machine, so they require PRO.

## Requirements

- One or more **Linux servers** (Ubuntu recommended), each with at least **4 CPU cores and 4 GB of RAM** for Community, and generous disk (100 GB recommended) if you record sessions. For PRO, which runs Kubernetes, size them as the cloud templates do by default: 4 vCPU and 8 GB per node.
- A sudo-capable user on each server, reachable over SSH (and, for Elastic and High Availability, the servers reachable from each other on their private addresses).
- A **domain** pointing at the server (at a load balancer in front of the masters, for HA in production), and a **certificate type**:
    - `letsencrypt` or `zerossl`: a certificate obtained automatically (requires port 80 to be reachable; does not work behind the load balancer of a High Availability stack).
    - `owncert`: bring your own, with `--owncert-public-key` and `--owncert-private-key`.
    - `selfsigned`: for a throwaway deployment.
- The [ports OpenVidu needs](../operate/status.md#check-the-ports) reachable. Required: `443/tcp`, and `22/tcp` for `ov` itself. Recommended: `443/udp`, `7881/tcp` and the media range `50000-60000/udp` (without them, media is relayed over TURN on 443, at a cost in latency and quality), and `80/tcp`, which `letsencrypt` and `zerossl` need to obtain the certificate. With the `ingress` module, `1935/tcp` and `7885/udp`. On PRO, also the cluster API on `6443/tcp` from your machine, and the node's own firewall must let the pod networks `10.42.0.0/16` and `10.43.0.0/16` reach it. Between the nodes of an Elastic or High Availability stack, `6443/tcp`, `10250/tcp` and `8472/udp` (and `2379-2380/tcp` between HA masters). See the port check below.
- The [OpenVidu CLI](../install.md). Nothing else needs to be pre-installed on the servers: the deploy brings Docker and the Compose plugin (Community) or the OpenVidu node agent (PRO) when they are missing.
- For PRO, your **OpenVidu PRO license** (`--openvidu-pro-license`): [create an OpenVidu account :fontawesome-solid-external-link:{.external-link-icon}](../../../../account.md){:target="_blank"} to get one; there is a 15-day free trial.

## Check the ports first

The most common reason an on-premises OpenVidu "does not work" is a stack that comes up perfectly but has no media: every service is healthy, yet UDP never reaches the node. `ov stack check-ports` finds that in seconds, **before deploying anything**, by running a temporary listener on the node and probing it. This verifies both TCP *and* UDP, which probing a running stack cannot do.

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

The fix is printed, never run: `ov` reads firewalls, it does not change them. Here only recommended ports fail, so the check warns and exits `0`; if a required port fails, it exits `8`. The report goes on to check the DNS name and that the node reaches the registries the deploy pulls from. The same check runs automatically before every remote deploy (`--skip-port-check` turns it off). See [Status and health checks](../operate/status.md#check-the-ports) for the full report and its options.

## Deploy

Each stack lives in its own empty directory on your machine. Choose the edition and topology. The examples use a domain that resolves to a private address, so they bring their own certificate (`owncert`; a path to a PEM file, a base64 PEM or the PEM itself), kept here in `~/certs/`. On a server reachable from the internet on port 80, `--certificate-type letsencrypt` obtains one automatically, and `selfsigned` is enough for a throwaway deployment.

=== "Single Node **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    ```console
    $ mkdir ov-ce && cd ov-ce
    $ ov stack deploy web \
      --environment on-premises \
      --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 \
      --domain-name 172-30-0-96.openvidu-local.dev \
      --certificate-type owncert \
      --owncert-public-key ~/certs/fullchain.pem --owncert-private-key ~/certs/privkey.pem \
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

    Plain Docker Compose and a systemd unit: no installer image, no operator. The ports are checked before anything is installed, and every credential is generated and **pinned** in `openvidu-stack.yml`, so a later deploy reuses them instead of locking the stack out of its data.


=== "Single Node **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The only difference from Community is `--edition pro` and the license; everything else follows from it.

    ```console
    $ mkdir ov-pro && cd ov-pro
    $ ov stack deploy prod \
      --edition pro --environment on-premises \
      --ssh ubuntu@172.30.0.101 --ssh-key ~/.ssh/id_ed25519 \
      --openvidu-pro-license <your-license> \
      --domain-name 172-30-0-101.openvidu-local.dev \
      --certificate-type owncert --owncert-public-key ~/certs/fullchain.pem --owncert-private-key ~/certs/privkey.pem \
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

    An Elastic stack is **deployed on one machine** (the master) with `--deployment-type elastic`, exactly like a Single Node PRO; every media node then **joins** it.

    ```console
    $ mkdir ov-elastic && cd ov-elastic
    $ ov stack deploy el --edition pro --environment on-premises --deployment-type elastic \
        --ssh ubuntu@172.30.0.101 --ssh-key ~/.ssh/id_ed25519 \
        --openvidu-pro-license <your-license> \
        --domain-name 172-30-0-101.openvidu-local.dev \
        --certificate-type owncert --owncert-public-key ~/certs/fullchain.pem --owncert-private-key ~/certs/privkey.pem \
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
       · wait until node-172-30-0-102 is ready in the stack
       ✓ Wait for the stack to see the node

    ✔ 172.30.0.102 joined the stack as a media node.
    ```

    `ov` reads the join address and token from the master over SSH and logs in to the new server with the same user, key and port (the token never appears on screen). Before installing anything it checks the ports the new node needs, from your machine and from the masters: if a required internal port is not reachable, the join stops with exit `6` and prints the `ufw` rule to add on each side. Each media node is one more `ov stack join --ssh`. See [Scaling](../operate/scaling.md).

=== "High Availability **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    High Availability is four masters plus one or more media nodes. There are two ways to expose them. For a test cluster, point the domain at the first master, as below. In production, put a TCP load balancer in front of the masters ([In production: behind a load balancer](#in-production-behind-a-load-balancer)), so the stack survives the loss of any of them.

    Deploy the first master with `--deployment-type ha` (as in the Elastic tab, but with `ha`), then join three more masters and the media nodes from the same directory:

    ```bash
    ov stack deploy ha --edition pro --environment on-premises --deployment-type ha \
      --ssh ubuntu@172.30.0.110 --ssh-key ~/.ssh/id_ed25519 \
      --openvidu-pro-license <your-license> \
      --domain-name 172-30-0-110.openvidu-local.dev \
      --certificate-type owncert --owncert-public-key ~/certs/fullchain.pem --owncert-private-key ~/certs/privkey.pem \
      --mode auto
    ov stack join --ssh ubuntu@172.30.0.111 --as master
    ov stack join --ssh ubuntu@172.30.0.112 --as master
    ov stack join --ssh ubuntu@172.30.0.113 --as master
    ov stack join --ssh ubuntu@172.30.0.114 --as media
    ```

    Each master join checks the cluster's internal ports (the API on `6443/tcp`, etcd on `2379-2380/tcp`, the kubelet on `10250/tcp`, the overlay on `8472/udp`) both ways with the masters already in the stack, then joins the machine and confirms it carries the labels the stack schedules by:

    ```console
    $ ov stack join --ssh ubuntu@172.30.0.111 --as master
    → reading the join address and token from 172.30.0.110
    → checking the ports of 172.30.0.111 from here and from the stack's masters
      Ports of 172.30.0.111 (master node of an ha stack)
      PORT                      SCOPE     LEVEL        STATE  TO OPEN
      443/tcp                   public    required     open
      80/tcp                    public    recommended  open
      22/tcp                    admin     required     open
      6443/tcp ← 172.30.0.110   internal  required     open   (only from 172.30.0.110)
      8472/udp ← 172.30.0.110   internal  required     open   (only from 172.30.0.110)
      2379/tcp ← 172.30.0.110   internal  required     open   (only from 172.30.0.110)
      2380/tcp ← 172.30.0.110   internal  required     open   (only from 172.30.0.110)
      10250/tcp ← 172.30.0.110  internal  required     open   (only from 172.30.0.110)

      Ports of 172.30.0.110 (reached from 172.30.0.111)
      PORT                   SCOPE     LEVEL     STATE       TO OPEN
      6443/tcp ← this node   internal  required  open
      8472/udp ← this node   internal  required  unverified
      2379/tcp ← this node   internal  required  open
      2380/tcp ← this node   internal  required  open
      10250/tcp ← this node  internal  required  open
      ✓ host firewall: no firewall is active on the node

    ▶ Connect…
       · check root/sudo access on 172.30.0.111
       ✓ Connect

    ▶ Join the cluster…
       · upload the OpenVidu node-agent installer
       · join 172.30.0.111 to the stack as a control-plane node
       ✓ Join the cluster

    ▶ Confirm the node's labels…
       · confirm this master carries the labels the stack schedules by
       ✓ Confirm the node's labels

    ▶ Leave the OpenVidu CLI on the node…
       · copy this CLI (ov-admin, 63 MB) to /usr/local/bin/ov
       ✓ Leave the OpenVidu CLI on the node

    ▶ Wait for the stack to see the node…
       · wait until node-172-30-0-111 is ready in the stack
       ✓ Wait for the stack to see the node

    ✔ 172.30.0.111 joined the stack as a master node.
    ```

    As the masters join, Redis Sentinel, the MongoDB replica set, MinIO and the clustered Loki and Mimir place one replica on each master. The first wait after the joins takes several minutes while the replicas settle:

    ```console
    $ ov stack status --wait
    waiting for https://172-30-0-110.openvidu-local.dev to be ready (Ctrl-C to stop)…
      ⏳ master nodes 4/4, media nodes 1/1, services 28/53, restarting: caddy-proxy-75b8b6cbf5-5g5cx, caddy-proxy-75b8b6cbf5-7vjvg (0s)
    …
    ✔ ha is ready (https://172-30-0-110.openvidu-local.dev)
    ```

    Before touching any server, `join` rejects any node the stack has no place for: `--as master` on an Elastic stack, any join to a single node, and any join to a Community stack. See [Scaling](../operate/scaling.md).

    #### In production: behind a load balancer

    Put a load balancer in front of the four masters, so the stack survives losing one:

    - **TCP passthrough**, not TLS termination: `443/tcp`, `80/tcp` and `6443/tcp` (the cluster API, at the address `--lb-host` names), and `1935/tcp` with RTMP ingest, to the four masters, with a TCP health check on `443`.
    - **The domain points at the load balancer.** Caddy on the masters terminates TLS, so the certificate is `selfsigned` or `owncert`: Let's Encrypt does not work behind a passthrough load balancer.
    - **Deploy the first master with the load balancer's domain and `--skip-port-check`.** Its port check probes the domain, and nothing behind the load balancer is healthy yet. Before skipping the check, open the ports listed in [Requirements](#requirements) yourself:

        ```bash
        ov stack deploy ha --edition pro --environment on-premises --deployment-type ha \
          --ssh ubuntu@<master-1> --ssh-key ~/.ssh/id_ed25519 \
          --openvidu-pro-license <your-license> \
          --domain-name <domain of the load balancer> --certificate-type selfsigned \
          --skip-port-check --mode auto
        ```

    - **Join the masters with `--lb-host`** (the load balancer in front of the masters) **and `--public-ip`** (the node's public address). The cluster API's certificate covers both, so the API stays reachable at either address:

        ```bash
        ov stack join --ssh ubuntu@<master> --as master --lb-host <load-balancer> --public-ip <master's public IP>
        ```

    - When the nodes reach each other on a private network and you reach them on public addresses, the join's port check reports the internal ports (`6443`, `8472`, `2379-2380`, `10250`) as closed although they are open between the nodes. Open them between the nodes, then join the masters and the media nodes with `--skip-port-check`.

    Expect the stack to be ready about 10 minutes after the last join: wait for it with `ov stack status --wait --wait-timeout 20m`, so the wait does not time out before the stack is ready.

### The port preflight

Before anything is installed, a remote deploy binds the node's ports with a temporary listener and probes them, and prints a table of them (`checking the inbound ports before installing anything…` in the output above). If a **required** port is closed (or, on PRO, the node's firewall drops the pod and service networks), the deploy stops with **exit code 6** and prints the exact rule to add for the detected firewall. A recommended port only warns and the deploy continues. `--skip-port-check` deploys without the check; `--this-node` never runs it (reachability cannot be verified from the node itself).

### Deploying again

A deploy to a node that already runs OpenVidu says so and keeps its data: it rewrites `docker-compose.yaml` and `config/` from `openvidu-stack.yml` (your `docker-compose.override.yaml` stays) and reuses the credentials the data was written with:

```text
172.30.0.96 already runs OpenVidu on 172-30-0-96.openvidu-local.dev (currently stopped). Deploying again rewrites its files from the spec and restarts it.
  · Its docker-compose.yaml and config/ are rewritten from the spec you are deploying; docker-compose.override.yaml is kept.
  · Its data is kept — nothing deletes MongoDB, MinIO or recordings.
  · The credentials in your spec are reused, so the kept data stays readable.
```

A remote deploy asks which mode to use unless you pass `--mode auto` or `--mode assisted`; with `--non-interactive`, `--mode` is required.

## Install on the server itself

Instead of `--ssh`, put `ov` on the server, log in, and deploy with **`--this-node`** (*the machine I am running on*). The CLI writes the deployment there and escalates with `sudo`, so a user with passwordless sudo is enough. A `--this-node` stack lives in `/opt/openvidu/stack`:

```console
$ sudo ov stack deploy web --environment on-premises --this-node \
  --domain-name 172-30-0-96.openvidu-local.dev \
  --certificate-type selfsigned
…
✔ OpenVidu is ready at https://172-30-0-96.openvidu-local.dev (caddy, openvidu, dashboard, meet, grafana)
```

Either way the server ends up operable from itself: a deploy from your laptop, as its last step, leaves the CLI and a stack directory of its own on the node, so `sudo ov stack status` works there with no directory to name.

## Review the commands first: assisted mode

`--mode assisted` runs **nothing** on the server. It writes the same files and prints the same commands, step by step, for you to review and run yourself. Add it to any deploy above:

```bash
ov stack deploy web --environment on-premises --ssh ubuntu@172.30.0.96 --ssh-key ~/.ssh/id_ed25519 \
  --domain-name 172-30-0-96.openvidu-local.dev --certificate-type selfsigned --mode assisted
```

## Next steps

- [Build your app](../../../build-your-app/index.md) against it, or follow a [tutorial](../../../tutorials/application-server/index.md): it connects with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` (`ov stack config get livekit-api-key` and `livekit-api-secret` print them).
- [Check the status](../operate/status.md) and run the health check.
- [Change the configuration](../operate/configuration.md) or [the modules](../operate/modules.md).
- [Scale the media nodes](../operate/scaling.md) of an Elastic or HA stack.
- [Operate the stack from another machine](../operate/remote.md).
- The full [command reference](../reference.md).
