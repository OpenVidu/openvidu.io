One command deletes the machines too, and it must be told what happens to the recordings and OpenVidu Meet data: **`--keep-data`** first moves the storage account to a resource group of its own, `<group>-data`, so it survives; **`--delete-data`** deletes it with the stack. With neither, nothing is deleted. The whole stack is one resource group, so deleting it is the teardown. This example destroys a Single Node stack:

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

- **`--keep-infrastructure`** removes OpenVidu but leaves the machines running (and still costing money). It needs `--keep-data` or `--delete-data` too, which then act on the machines as on [your own servers](/docs/self-hosting/single-node/on-premises/admin.md#destroy); the storage account stays either way.
- A stack deployed with **`--remote-state`** also loses what it kept on Azure: its record.
- A storage account **of your own** (`--param storageAccountName=<name>`) is not the stack's, so it stays either way. `ov` only deletes a resource group it created (tagged `created-by=openvidu-cli`).
