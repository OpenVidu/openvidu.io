---
title: "Troubleshooting the OpenVidu CLI"
description: "Fix common OpenVidu CLI problems: closed ports and exit codes, Let's Encrypt and port 80, reused stack names, cloud quotas and timed-out deploys."
---

# Troubleshooting

## A deploy stopped with exit code 6: a port does not reach the node

Before anything is installed, a remote deploy (and `ov stack join`) checks the node's inbound ports. A **required** port that does not arrive (`443/tcp`, or `22/tcp` for `ov` itself), or the node's firewall dropping the pod networks on PRO, stops the deploy with exit `6`, before anything is installed, and prints the rule to add for the firewall it found.

```console
$ ov stack deploy web --environment on-premises --ssh ubuntu@172.30.0.96 …
…
checking the inbound ports before installing anything…
  Ports of 172.30.0.96 (Community single node)
  PORT             SCOPE   LEVEL        STATE   TO OPEN
  443/tcp          public  required     closed  sudo ufw allow 443/tcp
  443/udp          public  recommended  open
  80/tcp           public  recommended  open
  50000-60000/udp  public  recommended  open
  7881/tcp         public  recommended  open
  22/tcp           admin   required     open
  1 of 6 checked port(s) do NOT reach the node: 443/tcp
ov: nothing was installed: 443/tcp must reach the node first. ov changes no firewall: add the rules above and deploy again (--skip-port-check deploys anyway)
```

On PRO, the node's own firewall must also let the pod networks reach it. When it does not, the port check says so before anything is installed:

```text
▶ Check the inbound ports…
…
       ✗ host firewall: the ufw firewall on the node does not let 10.42.0.0/16 and 10.43.0.0/16 reach the node: the pods cannot reach the cluster API, LiveKit or the kubelet, and the deploy does not finish
           sudo ufw allow from 10.42.0.0/16
           sudo ufw allow from 10.43.0.0/16
…
ov: nothing was installed: the pod networks (10.42.0.0/16, 10.43.0.0/16) must reach the node first. ov changes no firewall: add the rules above and deploy again (--skip-port-check deploys anyway)
```

`ov` reads firewalls but never changes them: run the printed fix on the node, then deploy again. A **recommended** port that is not reachable (`443/udp`, `80/tcp`, `7881/tcp` or the media range `50000-60000/udp`) only warns, and the deploy continues; `--skip-port-check` turns the check off. Run [`ov stack check-ports`](operate/status.md#check-the-ports) at any time for the full report: it is the check that verifies UDP, the usual culprit when a stack looks healthy but has no media.

## No media, but every service is healthy

This is almost always a blocked **UDP** port (`443/udp` or the media range). HTTPS works and the stack looks fine, but media never arrives. Probing a running stack cannot prove this, so stop it for a few seconds and run the full check:

```bash
ov stack stop && ov stack check-ports && ov stack start
```

Open the ports the report flags on the node and on any perimeter firewall (cloud security group, router). `check-ports` needs SSH access to the node, so it does not run against a PRO cloud stack registered through its kubeconfig (exit `2`); there, the template opens the ports, and the cloud's firewall rules for the stack are the place to look.

## Let's Encrypt fails: port 80 must be reachable

`--certificate-type letsencrypt` (and `zerossl`) obtains a certificate over HTTP, so **port 80 must reach the node** from the internet. If it is blocked, certificate issuance fails even though 443 is open. Open `80/tcp`, or use `owncert` to bring your own certificate, or `selfsigned` for a throwaway deployment.

## High Availability never gets ready with Let's Encrypt

On Google Cloud, Azure, Oracle Cloud and DigitalOcean, a High Availability stack sits behind a load balancer that passes TLS through to the masters. Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production. On AWS the load balancer terminates TLS with an ACM certificate, so the question does not arise. See the High Availability tab of each [cloud guide](index.md#where-you-can-deploy).

## No domain: the `sslip.io` fallback

A deploy with no `--domain-name` on a machine with a public IPv4 address derives an `sslip.io` name from it (for example `openvidu-40mfas-54-82-78-43.sslip.io`), so Let's Encrypt has a name to certify. On a High Availability cloud stack the name comes from the load balancer's address. This is fine for testing; use your own domain for anything real. A machine without a public IPv4 address, or one you reach by hostname, still needs `--domain-name`.

## AWS: a stack name stays in use for several days after a destroy

AWS Secrets Manager deletes a secret with a recovery window, so the stack's secret name remains in use for several days. Deploying a new stack with the **same name in the same region** fails until then. To free the name immediately:

```bash
aws secretsmanager delete-secret --secret-id <secret> --force-delete-without-recovery
```

`<secret>` is the name on the deploy's `credentials:` line: `openvidu-<region>-openvidu-<name>` for a single node, `openvidu-elastic-<region>-openvidu-<name>` for Elastic, `openvidu-ha-<region>-openvidu-<name>` for High Availability.

Or deploy with a different name (or in a different region).

## Azure: a resource group without the created-by tag

`ov` deletes only a resource group it created, recognized by a `created-by=openvidu-cli` tag. A deploy **refuses** a resource group that exists without that tag (deleting the stack would delete whatever else is in it). If an earlier version of `ov` created the group without the tag, add it (the refusal prints the command):

```bash
az group update --name <group> --set tags.created-by=openvidu-cli
```

## A cloud quota blocked the deploy

If the cloud refuses to create the machines (an instance-type or vCPU quota, an address or disk limit), the error comes from your cloud CLI, which `ov` runs as you. Request a quota increase, pick a smaller instance type (`--aws-instance-type` on AWS, `--param instanceType=<type>` on the other clouds), or deploy in another region. If a region does not offer the default instance type, `ov` substitutes the same size in another family and says so. A type you chose yourself is never replaced: the deploy stops before creating anything.

## A cloud deploy timed out while waiting for OpenVidu

The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, default 40 minutes with `--cloud`). The infrastructure already exists, so simply **resume**: it waits and registers the stack, reusing what is there:

```bash
ov stack deploy --cloud <cloud> --mode auto
```

No other flag is needed: everything is already in `openvidu-stack.yml`, and a cloud stack that already exists is reused, not created again.

## Oracle Cloud: the deploy waits until it times out

If an Oracle Cloud deploy keeps waiting for the stack to publish its URL until `--wait-timeout` runs out, the machine could not write its secrets into the vault. Look at `/var/log/cloud-init-output.log` on the instance (over SSH, with the key pair in `.openvidu/oracle/`). A `LimitExceeded` from the vault means it already holds the secrets of another stack, or too many versions of them: the secret names are fixed, so one vault serves one stack at a time. Destroy the attempt and deploy again with a vault of its own, or without `--oci-vault` so the template creates one.

## A cloud create failed partway

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so a failed attempt can always be cleaned up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

## Something is wrong at runtime: read the logs

```bash
ov stack logs --tail 100      # every service, one stream
ov stack logs -f              # follow live
ov stack status               # per-service state
ov stack test                 # active health check
```

## I lost the stack's directory

The directory holds the handle to the stack, not the stack itself. Recreate it with [`ov stack import`](operate/remote.md):

- **PRO:** `ov stack import --kubeconfig <file>` (the cluster holds its own state). Get the file on the master with `sudo ov stack kubeconfig --this-node --server <its public address>`, or on a cloud from the stack's secret store (the `credentials:` line of the deploy); or run `sudo ov stack import --this-node` on the master itself.
- **Community:** `ov stack import --ssh ubuntu@<host> --ssh-key <key>` (rebuilt from the node's files if needed).
- **A cloud stack deployed with `--remote-state`:** `ov stack import --cloud <cloud> --stack-name openvidu-<name>` (the name on the deploy's `record:` line) brings back the infrastructure too, so `ov stack destroy` and `--param` redeploys work again. Without `--remote-state`, only the deploying directory can drive the machines.

## See also

- [Status and health checks](operate/status.md) and [the port checks](operate/status.md#check-the-ports).
- [Operate from another machine](operate/remote.md).
- The full [command reference](reference.md).
