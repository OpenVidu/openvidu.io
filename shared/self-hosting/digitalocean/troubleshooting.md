### The account cannot hold the stack

A first deploy compares what it creates with the account's Droplet limit and checks the region and the Droplet sizes before anything is created. What does not fit stops it with exit `10`, naming what is short:

```text
ov: the DigitalOcean account cannot hold the stack in ams3, so nothing was created:
  - Droplets: 5 needed (4 masters and 1 media node), 3 free (limit 10, 7 in use)
Ask DigitalOcean for a higher Droplet limit (control panel: Settings > Team > Droplet limit, or a support ticket), delete Droplets you no longer use, or deploy another region with --do-region.
```

A size the region does not offer is a line of its own, and the way out names the size's `--param` and how to list the sizes the region offers. A region DigitalOcean does not have is exit `2`. The media nodes the autoscaler adds later are not in the check; when the limit leaves no room for `maxNumberOfMediaNodes`, a note says so.

### The stack name is too long for its Spaces

A Space name has 63 characters at most, so a High Availability stack's name (`openvidu-<name>`, or `--param stackName=`) takes 34 characters at most, and the other topologies' 38. A longer one stops the deploy with exit `2`, before the apply would fail half-way. Give the stack a shorter name, or pass one with `--param stackName=<name>`.

### The Spaces region has no Spaces

The Spaces go in `--do-spaces-region`, else the Droplets' region, and not every region offers Spaces. A region whose Spaces endpoint does not answer is named (`use a Spaces region that has Spaces: nyc1.digitaloceanspaces.com does not answer …: pass --do-spaces-region with one that does`).

### High Availability never gets ready with Let's Encrypt

A High Availability stack sits behind a load balancer that passes TLS through to the masters. Let's Encrypt's (and ZeroSSL's) HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production.

### No media, but every service is healthy

This is almost always a blocked **UDP** port (`443/udp` or the media range `50000-60000/udp`). HTTPS works and the stack looks fine, but media never arrives. On DigitalOcean the template opens the ports in the stack's firewall; if you narrowed it, open them there. Probing a running stack cannot prove this (the media range is dialable only while a participant holds it), so stop the stack for a few seconds and run the full check.

On a **Community** single node the stack's record keeps SSH to the node, so `check-ports` runs between stop and start. Start the stack again whatever the check reports (do not chain the three with `&&`: a failed check would leave the stack stopped):

```bash
ov stack stop
ov stack check-ports
ov stack start
```

A **PRO** stack is operated through its admin control protocol, not SSH, so `ov stack check-ports` on its own exits `2` there and prints the command that does reach the node, as `root` at the master's address. The key is not a file in the stack directory: `terraform -chdir=.openvidu/digitalocean output -raw sshPrivateKey > openvidu-key.pem` writes it (then `chmod 600 openvidu-key.pem`). Run the check between stop and start:

```bash
ov stack stop
ov stack check-ports --ssh root@<master> --ssh-key openvidu-key.pem
ov stack start
```

### The deploy timed out while waiting for OpenVidu

The Droplets were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, 40 minutes by default with `--cloud`). The infrastructure already exists, so simply resume: it waits and registers the stack, reusing what is there.

```bash
ov stack deploy <name> --cloud digitalocean --mode auto
```

Name the stack: without the name it would be registered as `openvidu`.

### A create failed partway

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so a failed attempt can always be cleaned up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

For closed ports and exit codes, the `sslip.io` fallback, a lost stack directory and the other cases shared by every cloud, see the generic [Troubleshooting](/docs/self-hosting/openvidu-cli.md#troubleshooting).
