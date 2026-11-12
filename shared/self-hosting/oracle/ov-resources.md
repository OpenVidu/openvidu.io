| Resource | Notes |
| --- | --- |
| Compute instances | One for Single Node; a master node and an autoscaling pool of media nodes for Elastic; four master nodes and an autoscaling pool of media nodes for High Availability |
| A virtual cloud network, subnet and network security groups | The ports OpenVidu needs, open to the internet. `--param subnet_ocid=<ocid>` (and `vcn_ocid=<ocid>`) puts the stack in a public, regional subnet of yours instead |
| A network load balancer | High Availability only |
| An Object Storage bucket and a Customer Secret Key | Recordings and OpenVidu Meet data, reached over the S3-compatible API. `--param bucketName=<name>` uses your own (on High Availability, `bucketAppDataName`, plus `bucketClusterDataName` for the observability data's bucket) |
| A KMS vault, one secret per key | What the stack publishes: URL and credentials (and, on PRO, the access `ov` administers it with). `--oci-vault` uses one of yours, one per stack; otherwise the template creates one |
| An autoscaling instance pool and a scale-in OCI Function | Elastic and High Availability only, unless `--param fixedNumberOfMediaNodes=N` runs a fixed count with neither |
| Dynamic groups and policies | In the tenancy and the compartment, named `<stack>-<hash>-…` so two stacks of the same name in different compartments do not collide |
| An SSH key pair | The template generates it. On Community `ov` saves the private half in `.openvidu/oracle/`; on PRO it stays in Object Storage (the `ssh_private_key_object` output) |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.
