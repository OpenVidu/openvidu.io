---
title: "Destroy an OpenVidu stack with the CLI"
description: "Tear an OpenVidu stack down with the OpenVidu CLI: preview with dry-run, choose what happens to recordings and data, and keep or remove the machines."
---

# Destroy a stack

`ov stack destroy` tears the deployment down and removes the directory's record. It asks for confirmation — type the stack name, or pass `-y`. `--dry-run` asks nothing and changes nothing: it prints exactly what the destroy would do with the same flags, and whether the record would go.

A destroy **deletes only what is the stack's by record**, never by name: the resources a cloud stack lists as its own, what its Terraform state holds, and on Azure a resource group that carries the `created-by=openvidu-cli` tag `ov` puts on groups it creates. It never deletes a bucket, account or group it did not create.

## Local and on-premises

On a server, the stack is stopped and disabled; its files and data stay under `/opt/openvidu`, so the same `ov stack deploy` brings it back with its data:

```console
$ ov stack destroy -y
✓ [172.30.0.96 single] systemctl stop openvidu
✓ [172.30.0.96 single] systemctl disable openvidu
stack stopped and disabled on all nodes (its files and data stay under /opt/openvidu)
✔ removed stack "web" from this directory
```

Two flags go further, independently:

- `--delete-data` removes the deployment's data after teardown (on a server, `/opt/openvidu/data`: MongoDB, MinIO, Redis, recordings, metrics and logs, certificates; on a local stack, the Docker volumes).
- `--delete-config` removes the whole deployment directory — on a server, `/opt/openvidu` with the systemd unit; locally, the compose and config files. It implies `--delete-data`.

```console
$ ov stack destroy --delete-data -y
✓ docker compose --profile * down -v
local deployment torn down
✔ removed stack "labc" from this directory
```

`--keep-context` tears the deployment down but keeps the directory's record.

## A cloud stack: the machines go too

A stack whose machines this CLI created (`--cloud`) also loses the machines — the deployment is **not** stopped first, because deleting the instance is a more thorough teardown than stopping services on it. What will be removed is printed before the confirmation:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your AWS account:
…
▶ Delete the machine on AWS…
   · delete the CloudFormation stack openvidu-ce10 (instance, Elastic IP, security group, secret)
   · wait for the resources to go
   · deleted the bucket openvidu-appdata-d56324d0 and everything in it
   · delete the key pair openvidu-ce10-key
   ✓ Delete the machine on AWS
✔ removed stack "ce10" from this directory
```

### You must choose what happens to the data

A destroy that deletes machines **must** say what becomes of the recordings and Meet data, on every cloud: with neither flag (or both), nothing is deleted and the command stops (exit `2`). There is no default, because either choice loses something — the data, or the money its storage costs.

| Cloud | `--keep-data` | `--delete-data` |
| --- | --- | --- |
| AWS | the data buckets stay (the template marks them `Retain`) | emptied and deleted after the stack |
| Google Cloud, Oracle, DigitalOcean | the data buckets (Spaces) are left out of the Terraform state before the destroy, so they stay | emptied and deleted by the destroy |
| Azure | the storage account moves to a resource group of its own (`<group>-data`) before the stack's group is deleted | deleted with the stack's resource group |

A bucket, Space or storage account **of your own** (named with `--param`) is not the stack's, so it stays either way.

!!! info "Destroy with `ov` to choose"

    Through `ov` the five clouds behave the same. Outside it they do not: deleting a CloudFormation stack from the AWS console keeps the data buckets, a bare `terraform destroy` deletes them, and deleting an Azure resource group from the portal deletes the storage account with it. Use `ov stack destroy` to make the choice yourself.

### Keep the machines

`--keep-infrastructure` tears the OpenVidu deployment down and **leaves the machines running** (and says that they are still costing money). Use it to reinstall onto the same machines.

### Remote-state cleanup

A stack deployed with `--remote-state` also keeps its Terraform state, record and SSH key on the cloud (see [Operate from another machine](remote.md#what-remote-state-stores-per-cloud)). `ov stack destroy` deletes those too: the state bucket `ov` created (kept with `--keep-infrastructure`) and, on AWS, the secret that held the SSH private key. From a state bucket that already existed under that name, the destroy removes only this stack's own objects and leaves the bucket.

## Destroying an imported or incomplete stack

- A stack **imported without its infrastructure** (`--kubeconfig`, or `--ssh` on a Community server) is torn down on the nodes its record names, but the directory that deployed it is the one that deletes a cloud stack's machines.
- A failed cloud **create** can still be destroyed: `ov` writes the stack's infrastructure into `openvidu-stack.yml` before creating anything, so `ov stack destroy` in the directory removes whatever the attempt left.

## Next steps

- [Deploy again](../deploy/local.md): the spec stays, so the same deploy recreates the stack.
- The full [command reference](../reference.md).
