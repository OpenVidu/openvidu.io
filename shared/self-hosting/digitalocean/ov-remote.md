By default the stack's directory is the only place that drives its machines: lose it and you lose control of them. A deploy with **`--remote-state`** also keeps the stack on DigitalOcean, so another machine with the same account's credentials can take it over completely. The deploy prints the name to import on its `record:` line.

From an empty directory on the other machine, `ov stack import --cloud digitalocean` reads that record and registers the stack, infrastructure included. `--stack-name` takes the stack's name **on the cloud**, `openvidu-<name>` for a stack deployed as `<name>`, not the name of its directory. The record never holds a secret, so the license (and any other sensitive parameter) is passed again:

```bash
ov stack import --cloud digitalocean --stack-name openvidu-<name> --openvidu-pro-license <your-license>
```

The other machine needs `$DIGITALOCEAN_TOKEN` of the same account and the Spaces keys, and `--do-spaces-region` when the Spaces are not in `ams3`. A Community stack is imported the same way, with no license: the import takes the SSH private key from the Terraform state and operates the stack over SSH. On a PRO stack, without `--openvidu-pro-license` the import stops before registering anything and says which flag is missing; `--mode assisted` prints the reads and runs nothing.

What `--remote-state` keeps on DigitalOcean, where the stack's infrastructure already lives:

| What | Where |
| --- | --- |
| **Terraform state** | a dedicated Space, `<stack>-<8 hex>-terraform-state` (the hex from the account's id, since Space names are shared by every account in a region) |
| **The record** (infrastructure, no secrets) | the state Space (`openvidu/registry/`) |
| **The SSH private key** `ov` generated | the Terraform state |

`ov stack destroy` deletes all of it. A stack deployed **without** `--remote-state` has no record to read: the only way back is the directory that deployed it, or `--kubeconfig` for the cluster alone (PRO).

See [Remote state](/docs/self-hosting/openvidu-cli.md#remote-state) for the general part.
