### The deploy waits until it times out { #the-deploy-waits-until-it-times-out }

If an Oracle Cloud deploy keeps waiting for the stack to publish its URL until `--wait-timeout` runs out (40 minutes by default with `--cloud`), the machine could not write its secrets into the vault. Look at `/var/log/cloud-init-output.log` on the master (over SSH, with the machines' key as **Access OpenVidu** above describes). A `LimitExceeded` from the vault means it already holds the secrets of another stack, or too many versions of them: the secret names are fixed, so one vault serves one stack at a time. Destroy the attempt and deploy again letting the template create a vault of its own (leave `--oci-vault` out), or point `--oci-vault` at a vault no other stack uses.

The infrastructure already exists, so once the cause is fixed you simply resume, reusing what is there. Name the stack, as the deploy does: without it the resume would register a stack named `openvidu`:

```bash
ov stack deploy openvidu --cloud oracle --mode auto
```

### What the stack publishes cannot be read { #what-the-stack-publishes-cannot-be-read }

Oracle answers `NotAuthorizedOrNotFound` both for a secret not published yet and for one the user may not read. If the stack's secrets cannot be read at all, the wait ends with the permission to grant:

```text
ov: the machines exist, but what they publish cannot be read from here: the user of your oci configuration may not read the stack's secrets (listing them answers NotAuthorizedOrNotFound): a group of that user needs `allow group <group> to read secret-family in compartment id ocid1.compartment.oc1..c` (your tenancy's administrator grants it)
```

### A name is already in use { #a-name-is-already-in-use }

The stack's dynamic groups, policies and (with `--remote-state`) its state bucket are named after the stack and a hash of the tenancy and compartment. A name that already exists (a stack of the same name in the same compartment, deployed from another directory, or what an earlier deploy left) stops the deploy before anything is created, and names the resource. Deploy this one with another name (`--param stackName=<another name>`), import the other stack (`ov stack import`), or delete what an earlier attempt left.

### A quota blocked the deploy { #a-quota-blocked-the-deploy }

Before creating anything, the deploy compares what a first deploy needs against what the tenancy has free, and stops when something does not fit: OCPUs and memory of the shapes in the availability domain, a free vault, and a free Customer Secret Key slot (OCI allows two per user). Ask Oracle for higher limits (console: **Governance & Administration → Limits, Quotas and Usage**), deploy in another region, delete a Customer Secret Key or a pending-deletion vault you no longer use, or choose smaller shapes (`--param masterNodeOcpus=<n> --param masterNodeMemory=<gb> --param masterNodeShape=<shape>`, and the `mediaNode…` equivalents).

### High Availability never gets ready with Let's Encrypt { #ha-never-gets-ready-with-lets-encrypt }

A High Availability stack sits behind a network load balancer that passes TLS through to the masters. Let's Encrypt's (and ZeroSSL's) HTTP challenge reaches a port 80 that only redirects to HTTPS, so the certificate is never issued and `ov stack status --wait` times out. Deploy High Availability with the default `selfsigned` certificate, or with `owncert` for production.

---

For problems common to every cloud (closed ports, exit codes, timed-out waits, quotas), see the [generic CLI troubleshooting](/docs/self-hosting/openvidu-cli.md#troubleshooting).
