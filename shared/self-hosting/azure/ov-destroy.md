One command deletes the machines too. You must choose what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves them, `--delete-data` deletes them; with neither (or both) nothing is deleted and the command stops (exit `2`). The whole stack is one resource group, so deleting it is the teardown. This example destroys a Single Node stack:

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your Azure subscription:

  # The resource group, which holds everything the stack is: the virtual machine, its
  # disk, public IP, network, security group, Key Vault, the storage account with the
  # recordings and Meet data.
  az group delete --name openvidu-ce12a-rg --yes --only-show-errors

--delete-data: the recordings and Meet data are in the storage account: this deletes them.

▶ Delete the machine on Azure…
   · delete the resource group openvidu-ce12a-rg (the virtual machine, its disk, public IP, network, security group, Key Vault, the storage account with the recordings and Meet data; this returns when Azure is done)
   ✓ Delete the machine on Azure
✔ removed stack "ce12a" from this directory
```

- With **`--delete-data`** the storage account goes with the resource group, recordings and all.
- With **`--keep-data`** the storage account first moves to a resource group of its own, `<group>-data`, so it survives the deletion of the stack's group.
- **`--keep-infrastructure`** tears the OpenVidu deployment down but leaves the machines running (and says so, because they are still costing money). Use it to reinstall onto the same machines.
- A storage account **of your own** (named with `--param storageAccountName=<name>`) is not the stack's, so it stays either way.

A destroy deletes only what is the stack's: the resources its resource group holds, recognized by the `created-by=openvidu-cli` tag `ov` puts on the groups it creates. It never deletes a resource group it did not create. A stack deployed with `--remote-state` also keeps its record on Azure, and the destroy deletes that too.

!!! warning "Names may be shortened"

    A Key Vault name can be at most 24 characters, so when `openvidu-<name>-keyvault` would exceed it, `ov` shortens the prefix from `openvidu-` to `ov-` (resource group `ov-<name>-rg`, Key Vault `ov-<name>-keyvault`). Take the stack's cloud name from the `record:` line the deploy prints; it is what `ov stack import --cloud azure --stack-name <name>` needs.
