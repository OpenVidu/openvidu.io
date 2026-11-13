One command deletes the machines too, and it must be told what happens to the recordings and OpenVidu Meet data: **`--keep-data`** leaves the Space and names it, **`--delete-data`** empties and deletes it. With neither, the destroy is refused and nothing is touched. Every DigitalOcean destroy needs `$DIGITALOCEAN_TOKEN`.

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your DigitalOcean account:

  # Everything the Terraform state in .openvidu/digitalocean holds: the Droplet, its
  # firewall, its tag, the SSH key, the Spaces key, the Space with the recordings and Meet
  # data.
  …

--delete-data: the recordings and Meet data are in the Space: this deletes them.

▶ Delete the machine on DigitalOcean…
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   · empty the Space openvidu-ce12d2-space-dae2e06c8c so it can be deleted
   · destroy .openvidu/digitalocean (this returns when Terraform is done)
   ✓ Delete the machine on DigitalOcean
✔ removed stack "ce12d2" from this directory
```

On Elastic and High Availability the destroy also deletes the autoscaler's Function and the media nodes it created. High Availability has two Spaces (application data and cluster data), and both flags name them apart.

- **`--keep-infrastructure`** removes OpenVidu but leaves the machines running (and still costing money). It needs `--keep-data` or `--delete-data` too, which then act on the machines as on [your own servers](/docs/self-hosting/single-node/on-premises/admin.md#destroy); the Space stays either way.
- A stack deployed with **`--remote-state`** also loses what it kept on DigitalOcean: its state Space.
- A Space of your own (`--param spaceName=<name>`, or `spaceAppDataName` and `spaceClusterDataName` on High Availability) is not the stack's, so it stays either way.

!!! warning "A kept Space holds the stack's credentials"

    DigitalOcean has no managed secret store, so the stack's Space also holds `secrets.env` (the Meet and LiveKit keys, the administrator's password) and, on Elastic and High Availability, the media nodes' SSH private key. After a `--keep-data` destroy, delete them from the Space unless you need them.
