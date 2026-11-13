One command deletes the machines too, and it must be told what happens to the recordings and OpenVidu Meet data: **`--keep-data`** leaves the Object Storage bucket and names it, **`--delete-data`** empties and deletes it. With neither, the destroy is refused and nothing is touched. This example destroys a Single Node stack:

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

On Elastic and High Availability the destroy also terminates the media nodes the scale-in detached from their pool, which needs `oci` and `jq` on your machine.

- **`--keep-infrastructure`** removes OpenVidu but leaves the machines running (and still costing money). It needs `--keep-data` or `--delete-data` too, which then act on the machines as on [your own servers](/docs/self-hosting/single-node/on-premises/admin.md#destroy); the bucket stays either way.
- A stack deployed with **`--remote-state`** also loses what it kept on Oracle Cloud: its state bucket (kept with `--keep-infrastructure`).
- A bucket of your own (`--param bucketName=<name>`; on High Availability, `bucketAppDataName` and `bucketClusterDataName`) and a vault of your own (`--oci-vault`) are not the stack's, so they stay either way.
- **The vault waits.** Oracle deletes a vault the template created only after at least 7 days; a deploy with the same name meanwhile creates another one.
