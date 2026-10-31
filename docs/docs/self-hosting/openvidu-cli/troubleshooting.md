---
title: "Troubleshooting the OpenVidu CLI"
description: "Fix common OpenVidu CLI problems: closed ports and exit codes, Let's Encrypt and port 80, reused stack names, cloud quotas and timed-out deploys."
---

# Troubleshooting

## A deploy stopped with exit code 6: a port does not reach the node

Before anything is installed, a remote deploy (and `ov stack join`) checks the node's inbound ports. A **required** port closed, or the node's firewall dropping the pod networks on PRO, stops the deploy with exit `6` and a table with the exact rule to add:

```
▶ Check the inbound ports…
   ⚠ Check the inbound ports — 1 of 5 checked port(s) do NOT reach the node: 443/udp
       Fix:
         - sudo ufw allow 443/udp   (run it on the node)
```

`ov` reads firewalls but never changes them — run the printed fix on the node. Then redeploy. Run [`ov stack check-ports`](operate/status.md#check-the-ports) at any time to see the full report; it is the only check that verifies UDP, which a healthy-looking stack with no media needs. A **recommended** port that does not answer, such as `443/udp` in the example above, only warns and the deploy continues; `--skip-port-check` turns the check off.

## No media, but every service is healthy

Almost always a blocked **UDP** port (`443/udp` or the media range). HTTPS works and the stack looks fine, but media never arrives. A running stack cannot prove this by dialling, so stop it for a few seconds and run the full check:

```bash
ov stack stop && ov stack check-ports && ov stack start
```

Open the ports the report flags on the node and on any perimeter firewall (cloud security group, router).

## Let's Encrypt fails: port 80 must be reachable

`--certificate-type letsencrypt` (and `zerossl`) obtains a certificate over HTTP, so **port 80 must reach the node** from the internet. If it is blocked, certificate issuance fails even though 443 is open. Open `80/tcp`, or use `owncert` to bring your own certificate, or `selfsigned` for a throwaway.

## No domain: the `sslip.io` fallback

A deploy with no `--domain-name` on a machine with a public IPv4 address derives a `sslip.io` name from it (for example `openvidu-40mfas-54-82-78-43.sslip.io`), so Let's Encrypt has a name to certify. This is fine for testing; use your own domain for anything real. A private or named target still needs `--domain-name`.

## AWS: a stack name is taken for a few days after destroy

AWS Secrets Manager deletes a secret with a recovery window, so the stack's secret name stays taken for some days. Deploying a new stack with the **same name in the same region** fails until then. Free the name at once:

```bash
aws secretsmanager delete-secret --secret-id openvidu-<region>-openvidu-<name> --force-delete-without-recovery
```

Or deploy with a different name (or in a different region).

## Azure: a resource group without the created-by tag

`ov` deletes only a resource group it created, recognised by a `created-by=openvidu-cli` tag. A deploy **refuses** a resource group that exists without that tag (deleting the stack would delete whatever else is in it). If an earlier `ov` created the group untagged, mark it — the refusal prints the command:

```bash
az group update --name <group> --set tags.created-by=openvidu-cli
```

## A cloud quota blocked the deploy

If the cloud refuses to create the machines (an instance-type or vCPU quota, an address or disk limit), the error comes from your cloud CLI, which `ov` runs as you. Request a quota increase, pick a smaller instance type (`--aws-instance-type` and the per-cloud equivalents), or deploy in another region. A region that does not offer the default instance type is handled automatically for the default (`ov` substitutes the same size in another family and says so), but a type you chose yourself is never replaced: the deploy stops before creating anything.

## A cloud deploy timed out while waiting for OpenVidu

The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, default 40 minutes with `--cloud`). The infrastructure already exists, so simply **resume** — it waits and registers the stack, reusing what is there:

```bash
ov stack deploy --cloud <cloud> --mode auto
```

No other flag is needed: everything is already in `openvidu-stack.yml`, and a cloud stack that already exists is reused, not created again.

## A cloud create failed partway

`ov` writes the stack's infrastructure into `openvidu-stack.yml` **before** creating anything, so a failed attempt can always be cleaned up from the directory:

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

- **PRO:** `ov stack import --kubeconfig ./kubeconfig.yaml` (the cluster holds its own state), or `sudo ov stack import --this-node` on the node.
- **Community:** `ov stack import --ssh ubuntu@<host> --ssh-key <key>` (rebuilt from the node's files if needed).
- **A cloud stack deployed with `--remote-state`:** `ov stack import --cloud <cloud> --stack-name <name>` brings back the infrastructure too, so `ov stack destroy` and `--param` redeploys work again. Without `--remote-state`, only the deploying directory can drive the machines.

## See also

- [Status and health checks](operate/status.md) and [the port checks](operate/status.md#check-the-ports).
- [Operate from another machine](operate/remote.md).
- The full [command reference](reference.md).
