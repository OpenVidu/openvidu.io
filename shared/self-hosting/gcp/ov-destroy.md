One command deletes the machines too, and it must be told what happens to the recordings and OpenVidu Meet data: **`--keep-data`** leaves the Cloud Storage bucket and names it, **`--delete-data`** empties and deletes it. With neither, the destroy is refused and nothing is touched. On High Availability there are two buckets (application data and cluster data), and both flags name them apart.

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Google Cloud project my-project:

  # Everything the Terraform state in .openvidu/gcp holds: the machine, its disk, its
  # static address, the firewall rules, the service account and the secrets.
  terraform -chdir=.openvidu/gcp init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/gcp destroy -auto-approve -input=false -no-color
  …
--delete-data: the recordings and Meet data are in the Cloud Storage bucket: this deletes them.

▶ Delete the machine on Google Cloud…
   · destroy .openvidu/gcp (this returns when Terraform is done)
   ✓ Delete the machine on Google Cloud
✔ removed stack "ce12g" from this directory
```

The destroy deletes only what the stack's Terraform state holds, never anything matched by name. On Elastic and High Availability it says "the machines" and also removes the media nodes' instance group.

- **`--keep-infrastructure`** removes OpenVidu but leaves the machines running (and still costing money). It needs `--keep-data` or `--delete-data` too, which then act on the machines as on [your own servers](/docs/self-hosting/single-node/on-premises/admin.md#destroy); the bucket stays either way.
- A stack deployed with **`--remote-state`** also loses what it kept on Google Cloud: its state bucket (kept with `--keep-infrastructure`).
- A bucket of your own (`--param bucketName=<name>`) is not the stack's, so it stays either way.

!!! info "Destroy with `ov` to control the data"

    A bare `terraform destroy` deletes the data buckets. Use `ov stack destroy` to choose.
