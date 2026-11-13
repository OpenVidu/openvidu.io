By default, the stack's directory is the only place that drives the machines: if you lose it, you lose control of them. A deploy with **`--remote-state`** (Terraform 1.12.0 or later) also keeps the stack on Oracle Cloud, so another machine with your OCI credentials can take it over completely. It keeps, in a state bucket of the stack's own:

| What | Where |
| --- | --- |
| The Terraform state | a dedicated Object Storage bucket, `<stack>-<hash>-terraform-state` |
| The record (infrastructure, no secrets) | the same bucket (`openvidu/registry/`) |
| The machines' SSH private key, which the template generates | the Terraform state |

From an empty directory on another machine, `ov stack import --cloud oracle` reads that record and registers the stack. The bucket is named after the tenancy and the compartment too, so the import needs `--oci-compartment` (and the region, which defaults to your `oci` profile's). `--stack-name` takes the stack's name **on the cloud**, `openvidu-<name>`, exactly as the deploy's `record:` line prints it, not the name of its directory. The record never holds a secret, so a PRO license must be passed again:

```bash
ov stack import --cloud oracle --stack-name openvidu-el --oci-region eu-madrid-1 \
  --oci-compartment ocid1.compartment.oc1..<compartment> --openvidu-pro-license <your-license>
```

From then on, `ov stack status`, `ov stack deploy <name> --cloud oracle --param …` and `ov stack destroy` work here as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too). A Community stack is imported the same way, with no license; the SSH private key comes from the Terraform state. A stack deployed **without** `--remote-state` has no record to read, so no directory can drive its machines again. OpenVidu itself can still be adopted from one of its nodes: `ov stack import --ssh <user>@<master>` (any master on High Availability), `sudo ov stack import --this-node` on the node itself, or `-f` of a file `ov stack export --bundle --out <file>` wrote. That adopts OpenVidu, not the infrastructure: the new directory runs `ov stack status`, `config` and the like, but not a `--param` redeploy or an `ov stack destroy` of the machines.

See [Remote state](/docs/self-hosting/openvidu-cli.md#remote-state) for the general behavior of `ov stack import`.
