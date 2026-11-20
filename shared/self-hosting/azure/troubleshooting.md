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

Request more quota, pick smaller sizes with `--param`, or deploy in another location. The same check runs on a redeploy that raises the number of media nodes the stack keeps, and stops with exit `10` before changing anything if the media family is short.

**High Availability never gets ready with Let's Encrypt.** On Azure a High Availability stack sits behind a load balancer that passes TLS through to the masters, and Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production.

**The deploy timed out waiting for OpenVidu.** The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, 40 minutes by default with `--cloud`). The infrastructure already exists, so simply resume, reusing what is there (name the stack, as on the first deploy):

```bash
ov stack deploy <name> --cloud azure --mode auto
```

A deploy in assisted mode resumes with `--mode assisted` instead: the error prints the command to run.

**A create failed partway.** `ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating anything, so a failed attempt can always be cleaned up from the directory:

```bash
ov stack destroy --delete-data   # or --keep-data
```

**No media, but every service is healthy.** This is almost always a blocked **UDP** port (`443/udp` or the media range): HTTPS works and the stack looks fine, but media never arrives. [Ports](/docs/self-hosting/single-node/azure/admin.md#ports) in the administration guide shows how to run the full check, and [Logs](/docs/self-hosting/single-node/azure/admin.md#logs) how to read the logs of every service.
