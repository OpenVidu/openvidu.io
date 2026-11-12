| Resource | Notes |
| --- | --- |
| A resource group, `openvidu-<name>-rg` | Holds everything the stack is; `--azure-resource-group` names it; tagged `created-by=openvidu-cli` |
| Virtual machines | One for Single Node; master nodes and a scale set of media nodes for Elastic and High Availability |
| A static public IP and a network security group | The ports OpenVidu needs, open to the internet |
| A load balancer | High Availability only |
| A Storage Account and a Blob container (`openvidu-appdata`) | Recordings and OpenVidu Meet data. `--param storageAccountName=<name>` uses your own |
| A Key Vault, `openvidu-<name>-keyvault` | What the stack publishes: URL and credentials (and the kubeconfig on PRO) |
| An SSH key pair | `ov` generates it; the private half stays in `.openvidu/azure/` |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.
