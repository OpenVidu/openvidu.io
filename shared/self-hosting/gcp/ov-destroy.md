One command deletes the machines too. You must choose what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the bucket, `--delete-data` deletes it. With neither flag (or both), nothing is deleted and the command stops (exit `2`): there is no default, because either choice loses something, the data or the money its storage costs.

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Google Cloud project my-project:

  # Everything the Terraform state in .openvidu/gcp holds: the machines, addresses,
  # firewall rules, secrets and service accounts.
  terraform -chdir=.openvidu/gcp init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/gcp destroy -auto-approve -input=false -no-color
  …
--delete-data: the recordings and Meet data are in the Cloud Storage buckets: this deletes them.

▶ Delete the machines on Google Cloud…
   · destroy .openvidu/gcp (this returns when Terraform is done)
   ✓ Delete the machines on Google Cloud
✔ removed stack "ce12g" from this directory
```

A destroy **deletes only what belongs to the stack according to its Terraform state**, never anything matched by name:

- `--delete-data` empties and deletes the bucket the template created, recordings and all. On High Availability there are two buckets (application data and cluster data), named apart, and both go.
- `--keep-data` first removes the bucket from the Terraform state, so the destroy leaves it in place and prints its name. A bucket of your own (`--param bucketName=<name>`) is not in the state, so it stays either way.
- `--keep-infrastructure` tears the OpenVidu deployment down but **leaves the machines running** (and says so, because they are still costing money). Use it to reinstall onto the same machines.

!!! info "Destroy with `ov` to control the data"

    Through `ov`, the five clouds behave the same way. Outside `ov`, they do not: a bare `terraform destroy` on Google Cloud deletes the data buckets. Use `ov stack destroy` to make the choice yourself.

A stack deployed with `--remote-state` also keeps its Terraform state, record and SSH key on Google Cloud. `ov stack destroy` deletes those too: the state bucket `ov` created (kept with `--keep-infrastructure`). If the state bucket already existed under that name, the destroy removes only this stack's objects and leaves the bucket.

A failed create can still be destroyed: `ov` records the stack's infrastructure in `openvidu-stack.yml` before creating anything, so `ov stack destroy` in the directory removes whatever the attempt left behind.
