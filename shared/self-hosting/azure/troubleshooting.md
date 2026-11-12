Most problems and their fixes are the same on every cloud: see [Troubleshooting the OpenVidu CLI](/docs/self-hosting/openvidu-cli.md#troubleshooting) for closed ports (a deploy that stops with exit `6`), Let's Encrypt and port 80, a deploy that timed out while waiting for OpenVidu (resume it with `ov stack deploy <name> --cloud azure --mode auto`, which reuses what is already there), and cleaning up a create that failed partway. A few are specific to Azure.

**A resource group without the `created-by` tag.** `ov` deletes only a resource group it created, recognized by a `created-by=openvidu-cli` tag. A deploy **refuses** a resource group that exists without that tag, because deleting the stack would delete whatever else is in it. If an earlier version of `ov` created the group without the tag, add it (the refusal prints the command):

```bash
az group update --name <group> --set tags.created-by=openvidu-cli
```

**The vCPU quota blocked the deploy.** Azure caps the vCPUs a subscription runs in a location, per VM family and in total, and a new subscription usually has 10 per family. Before it creates anything, the deploy adds up what its machines need and stops with exit `10` if a family is short, naming it:

```text
ov: this Azure subscription cannot hold the stack in northeurope, so nothing was created:
  - Standard DSv3 Family vCPUs: 16 needed (4 masters, Standard_D4s_v3), 10 free (limit 10, 0 in use)
Request more vCPU quota for the subscription in northeurope (Azure portal: Quotas > Compute), or deploy smaller or other sizes with --param masterNodeInstanceType=<size> --param mediaNodeInstanceType=<size>.
```

Request more quota, pick smaller sizes with `--param`, or deploy in another location.

The check also runs on a redeploy of an Elastic or High Availability stack that raises the number of media nodes it makes sure of (`fixedNumberOfMediaNodes`, or else `minNumberOfMediaNodes`): `ov` reads how many media nodes the scale set holds and checks the quota of the ones it adds, before changing anything (exit `10`):

```text
ov: this Azure subscription cannot hold the media nodes this deploy adds in northeurope, so nothing was changed:
  - Standard FSv2 Family vCPUs: 8 needed (1 more media node, Standard_F8s_v2), 2 free (limit 10, 8 in use)
Request more vCPU quota for the subscription in northeurope (Azure portal: Quotas > Compute), or ask for fewer media nodes.
```

A higher `maxNumberOfMediaNodes` or `initialNumberOfMediaNodes` is not checked: the media nodes the autoscaler adds later count against the media family's quota when Azure creates them, and do not come up if the subscription cannot hold them.

**High Availability never gets ready with Let's Encrypt.** On Azure a High Availability stack sits behind a load balancer that passes TLS through to the masters, and Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production.
