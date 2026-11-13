By default the stack's directory is the only place that drives its machines: lose it and you lose control of them. A deploy with **`--remote-state`** also keeps the stack on DigitalOcean, so another machine with the same account's credentials can take it over completely. The deploy prints the name to import on its `record:` line.

From an empty directory on the other machine, `ov stack import --cloud digitalocean` reads that record and registers the stack, infrastructure included. `--stack-name` takes the stack's name **on the cloud**, `openvidu-<name>` for a stack deployed as `<name>`, not the name of its directory. The record never holds a secret, so the license (and any other sensitive parameter) is passed again:

```bash
ov stack import --cloud digitalocean --stack-name openvidu-<name> --openvidu-pro-license <your-license>
```

The other machine needs `$DIGITALOCEAN_TOKEN` of the same account and the Spaces keys. The state Space is looked for in `--do-spaces-region`, else `--do-region`, else `$DO_REGION`, else `ams3`, so pass `--do-spaces-region` when the Spaces are in another region. A Community stack is imported the same way, with no license: the import takes the SSH private key from the Terraform state and operates the stack over SSH.

What `--remote-state` keeps on DigitalOcean, where the stack's infrastructure already lives:

| What | Where |
| --- | --- |
| **Terraform state** | a dedicated Space, `<stack>-<8 hex>-terraform-state` (the hex from the account's id, since Space names are shared by every account in a region) |
| **The record** (infrastructure, no secrets) | the state Space (`openvidu/registry/`) |
| **The machines' SSH private key**, which the template generates | the Terraform state |

`ov stack destroy` deletes all of it. A stack deployed **without** `--remote-state` has no record to read: the way back is the directory that deployed it. If that directory is gone, a PRO stack is still adopted from one of its nodes with `ov stack import --ssh <user>@<master>` (any master on High Availability), with `sudo ov stack import --this-node` run on the node itself, or with `ov stack import -f <file>` of a bundle written beforehand by `ov stack export --bundle --out <file>`. That adopts OpenVidu, so `ov stack status`, `config` and `logs` work, but not the infrastructure: there is no `--param` redeploy and no `ov stack destroy` of the machines from that directory.

See [Remote state](/docs/self-hosting/openvidu-cli.md#remote-state) for the general part.
