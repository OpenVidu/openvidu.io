| Resource | Notes |
| --- | --- |
| Compute Engine instances | One for Single Node; master nodes and a managed instance group of media nodes for Elastic and High Availability |
| A static address and a firewall rule | The ports OpenVidu needs, open to the internet |
| A passthrough TCP load balancer | High Availability only |
| A Cloud Storage bucket | Recordings and OpenVidu Meet data. `--param bucketName=<name>` uses your own |
| Two service accounts and a service-account key | The instance's (Meet uses it) and a storage-only one whose key egress uploads with |
| Secret Manager secrets | What the stack publishes: one secret per key, prefixed with the stack name (and the kubeconfig on PRO) |
| An SSH key pair | The template generates it; `ov` keeps the private half in `.openvidu/gcp/` |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.
