One command deletes the machines too. A destroy that deletes machines **must** say what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the Object Storage bucket, `--delete-data` deletes it. With neither (or both), nothing is deleted and the command stops (exit `2`).

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Oracle Cloud tenancy (compartment ocid1.compartment.oc1..<compartment>):

  # Everything the Terraform state in .openvidu/oracle holds: the instances (and, on Elastic
  # and High Availability, the media nodes' instance pool, its instance configuration and
  # autoscaling configuration, and the scale-in Function), the network the stack created,
  # its network security groups, the dynamic groups and policies, the bucket's Customer
  # Secret Key, the SSH key's object in the bucket, and the vault and its secrets (a vault
  # stays pending deletion for the period Oracle imposes).
  terraform -chdir=.openvidu/oracle init -input=false -no-color -force-copy
  terraform -chdir=.openvidu/oracle destroy -auto-approve -input=false -no-color

--delete-data: the recordings and Meet data are in the Object Storage bucket: this deletes them.
note: Oracle does not delete a vault at once: the stack's vault stays pending deletion, with its secrets, for 7 days or more, and a deploy with the same name meanwhile creates another one

▶ Delete the machine on Oracle Cloud…
   · destroy .openvidu/oracle (this returns when Terraform is done)
   ✓ Delete the machine on Oracle Cloud
✔ removed stack "ce12o" from this directory
```

`--delete-data` empties and deletes the Object Storage bucket the template created, recordings and all; `--keep-data` first removes it from the Terraform state, so the destroy leaves it in place and names it. A bucket of your own (`--param bucketName=<name>`; on High Availability, `bucketAppDataName` and `bucketClusterDataName`) stays either way.

On Elastic and High Availability, media nodes the scale-in detached from their pool are no longer in the Terraform state; the template's destroy finds them by their tags and terminates them with `oci` and `jq`. Nothing drains then: the whole stack goes.

A few points specific to Oracle Cloud:

- **The vault waits.** A vault the template created (no `--oci-vault`) is not deleted immediately: OCI schedules it for deletion after a waiting period of at least 7 days. A deploy with the same name meanwhile creates another one. A vault of yours (`--oci-vault`) is not the stack's, so the destroy leaves it, with the stack's secrets still in it.
- **Keep the machines.** `--keep-infrastructure` tears the OpenVidu deployment down but leaves the machines running (and says so, because they still cost money). Use it to reinstall onto the same machines.
- **Remote-state cleanup.** A stack deployed with `--remote-state` also keeps its Terraform state and record in a bucket of its own; `ov stack destroy` deletes that too (kept with `--keep-infrastructure`). If the state bucket already existed under that name, the destroy removes only this stack's objects and leaves the bucket.

See [Destroy a stack](/docs/self-hosting/single-node/on-premises/admin.md#destroy) for the options common to every deployment.
