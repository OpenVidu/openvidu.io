By default, the stack's directory is the only place that drives the machines: lose it and you lose control of them. A deploy with **`--remote-state`** also keeps the stack on Google Cloud, so another machine with the project's credentials can take it over completely. On Google Cloud, `--remote-state` stores:

| What | Where |
| --- | --- |
| **Terraform state** | a dedicated Cloud Storage bucket of the stack's own (`<project>-<stack>-<hash>-terraform-state`) |
| **The record** (infrastructure, no secrets) | the state bucket, under `openvidu/registry/` |
| **The machines' SSH private key**, which the template generates on Community (a PRO stack on Google Cloud has none: `gcloud compute ssh` logs in) | inside the Terraform state |

From an empty directory on another machine, `ov stack import --cloud gcp` reads that record and registers the stack, infrastructure included. `--stack-name` takes the stack's name **on Google Cloud**, exactly as the deploy's `record:` line prints it (`openvidu-<name>` for a stack deployed as `<name>`); (the name it was deployed as works too: `ov` reads the exact name first, then `openvidu-<name>`, and says which stack it imported):

```bash
mkdir openvidu && cd openvidu
ov stack import --cloud gcp --gcp-project my-project --stack-name openvidu-<name>
```

The record never holds a secret, so on OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag } you must pass `--openvidu-pro-license <license>` again, exactly as it was given to the deploy; without it the import stops before registering anything and says which flag is missing. A Community stack is imported the same way with no license: the import takes the SSH private key from the Terraform state and operates the stack over SSH.

From then on `ov stack status`, `ov stack deploy <name> --cloud gcp --param …` and `ov stack destroy` work here as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too).

A stack deployed **without** `--remote-state` has no record to read, so `ov` cannot drive its machines from a new directory: no `--param` redeploy, no `ov stack destroy` of the infrastructure. You can still adopt the running OpenVidu, on either edition, in one of three ways:

- `ov stack import --ssh <user>@<master>` from one of its nodes (any of the four masters on High Availability);
- `sudo ov stack import --this-node` on the node itself;
- `ov stack import -f <file>`, from a bundle you saved earlier with `ov stack export --bundle --out <file>`.

Each adopts **OpenVidu, not the machines**: `status`, `logs` and `config` work, but a `--param` redeploy or an `ov stack destroy` of the infrastructure does not, because the Terraform state is gone with the directory.

For the general mechanics of `ov stack import` and remote state, see [the CLI reference](/docs/self-hosting/openvidu-cli.md#remote-state).
