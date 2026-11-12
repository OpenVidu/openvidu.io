| Resource | Notes |
| --- | --- |
| Compute Engine instances | One for Single Node; master nodes and a managed instance group of media nodes for Elastic and High Availability |
| A static address and a firewall rule | The ports OpenVidu needs, open to the internet |
| A passthrough TCP load balancer | High Availability only |
| A Cloud Storage bucket | Recordings and OpenVidu Meet data. `--param bucketName=<name>` uses your own. High Availability adds a second bucket for the cluster's metrics and logs |
| A service account, and object-storage credentials | The instance's service account (Meet uses it) on both editions. On **COMMUNITY**{ .openvidu-tag .openvidu-community-tag } a storage-only service account whose key egress uploads recordings with (`GCP_CREDENTIALS_JSON`); on **PRO**{ .openvidu-tag .openvidu-pro-tag } an HMAC key on the bucket, reached through Cloud Storage's S3-compatible API |
| Secret Manager secrets | What the stack publishes: one secret per key, prefixed with the stack name (PRO also publishes the stack's access there) |
| An SSH key pair (**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }) | The template generates it and `ov` keeps the private half in `.openvidu/gcp/`. **PRO**{ .openvidu-tag .openvidu-pro-tag } keeps no key pair: its node is reached with `gcloud compute ssh` |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.
