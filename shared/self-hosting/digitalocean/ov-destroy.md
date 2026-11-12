One command deletes the machines too. You must choose what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the Space, `--delete-data` deletes it. With neither (or both), nothing is deleted and the command stops (exit `2`): there is no default, because either choice loses something, the data or the money its storage costs. A Space must be empty to go, and the machine writes into it until it is gone, so the Space is emptied between two passes:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your DigitalOcean account:

  # Everything the Terraform state in .openvidu/digitalocean holds: the Droplet, its
  # firewall, its tag, the SSH key, the Spaces key, the Space with the recordings and Meet
  # data. A Space must be empty to go, and the machine writes into it until it is gone, so
  # the Space is emptied between two passes; only a Space the state holds is emptied,
  # never one of your own (--param spaceName=<name>).
  terraform -chdir=.openvidu/digitalocean init -input=false -no-color -force-copy
  env OPENVIDU_STACK_DESTROY=1 terraform -chdir=.openvidu/digitalocean destroy -auto-approve -input=false -no-color
  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 rm s3://openvidu-ce12d2-space-dae2e06c8c --recursive --endpoint-url https://ams3.digitaloceanspaces.com
  env OPENVIDU_STACK_DESTROY=1 terraform -chdir=.openvidu/digitalocean destroy -auto-approve -input=false -no-color

--delete-data: the recordings and Meet data are in the Space: this deletes them.

▶ Delete the machine on DigitalOcean…
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   · empty the Space openvidu-ce12d2-space-dae2e06c8c so it can be deleted
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   ✓ Delete the machine on DigitalOcean
✔ removed stack "ce12d2" from this directory
```

The destroy needs `$DIGITALOCEAN_TOKEN` (every DigitalOcean destroy asks for it, even a single node's, which drains nothing). On Elastic and High Availability it also deletes the autoscaler's Function and the media nodes it created, which the Terraform state does not hold: the template's destroy removes them by their tags with the token. `OPENVIDU_STACK_DESTROY=1` tells the template the whole stack is going, so no media node drains first.

With `--delete-data`, the Space the template created is deleted with the stack: the destroy empties it and Terraform deletes it. With `--keep-data`, the Space is first removed from the Terraform state, so a single destroy removes everything else and the Space remains, with the recordings, Meet data and this deployment's `secrets.env`. High Availability has two Spaces (the recordings and Meet data in one, the cluster's metrics and logs in the other); both flags name them apart. A Space of your own (`--param spaceName=<name>`) stays either way. `--keep-infrastructure` tears the deployment down but leaves the Droplets running (and says so, because they are still costing money).

A stack deployed with `--remote-state` also keeps its Terraform state and record in a state Space of its own; the destroy removes that too. If the state Space already existed under that name, the destroy removes only this stack's objects and leaves the Space.

!!! warning "The Space is the secret store"

    DigitalOcean has no managed secret store, so the stack's own Space holds both the recordings and `secrets.env` (the URLs and credentials). The Space is created without `force_destroy`, so `--delete-data` empties it in an explicit, separate step before deleting; `--keep-data` leaves it in place, with `secrets.env` and the recordings. Keep the Spaces keys available whenever you operate the stack.

See [Destroy](/docs/self-hosting/single-node/on-premises/admin.md#destroy) for the options shared by every deployment.
