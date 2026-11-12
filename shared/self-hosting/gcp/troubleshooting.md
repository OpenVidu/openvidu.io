These are the problems specific to a Google Cloud deploy. For the ones common to every cloud (closed ports and exit codes, blocked UDP and no media, reused names, runtime logs), see the [generic troubleshooting](/docs/self-hosting/openvidu-cli.md#troubleshooting).

### The project has no `default` network

Each Google Cloud fact (zone, network, quotas) is read before anything is created, so a problem stops the deploy with nothing touched. If the project has no `default` network (an organization policy such as `compute.skipDefaultNetworkCreation` leaves new projects without one), the deploy stops with exit `2` and prints the fix:

```text
ov: the Google Cloud project my-proj has no network named default, which a deploy uses unless you name another …, so nothing was created: create it (`gcloud compute networks create default --subnet-mode=auto --project=my-proj`), or pass the network to use with --param network=<name> (and --param subnetwork=<name> when it is in custom subnet mode)
```

### A quota blocked the deploy

`ov` adds up what a first deploy creates (vCPUs, SSD disk, static and in-use addresses) and compares it with what the region leaves free. What does not fit stops the deploy with exit `10`, before anything is created, naming each quota:

```text
ov: the Google Cloud project my-proj cannot hold the stack in europe-west2, so nothing was created:
  - CPUS (vCPUs of E2 and N1 machines): 24 needed …, 8 free (limit 24, 16 in use)
  - SSD_TOTAL_GB (GB of balanced and SSD persistent disk): 1000 needed …, 500 free (limit 500, 0 in use)
Request more quota for the project in europe-west2 (Google Cloud console: IAM & Admin > Quotas), or deploy another region, or smaller or other sizes with --param masterNodeInstanceType=<type> --param mediaNodeInstanceType=<type> --param masterNodesDiskSize=<GiB> --param mediaNodesDiskSize=<GiB>.
```

Request more quota, pick smaller sizes with `--param`, or deploy in another region, then run the same command again.

### Service-account key creation is blocked

The template mints a Cloud Storage service-account key that egress uses to upload recordings. An organization policy that blocks key creation (`iam.disableServiceAccountKeyCreation`) stops the apply. Allow key creation in the project, or the deploy cannot finish.

### The deploy timed out while waiting for OpenVidu

The machines were created but did not finish deploying OpenVidu within the wait window (`--wait-timeout`, 40 minutes with `--cloud` by default). The infrastructure already exists, so simply **resume**: it waits and registers the stack, reusing what is there.

```bash
ov stack deploy --cloud gcp --mode auto
```

### High Availability never gets ready with Let's Encrypt

A High Availability stack sits behind a load balancer that passes TLS through to the masters. Let's Encrypt's HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production.

### No domain: the `sslip.io` fallback

A deploy with no `--domain-name` derives an `sslip.io` name from the public IP (on High Availability, from the load balancer's address), so Let's Encrypt has a name to certify. This is fine for testing; use your own domain for anything real. No Google Cloud template points a domain, so with `--domain-name` the deploy prints the `A` record to create as soon as the machines exist, and `ov stack status --wait` waits until it resolves.

### The state bucket already keeps another stack's state

With `--remote-state`, `ov` refuses a state bucket whose record names another stack (the same stack deployed from another directory), with exit `2` and nothing created. Take that stack over here instead:

```bash
ov stack import --cloud gcp --stack-name openvidu-<name> --gcp-project my-proj
```
