| Resource | Notes |
| --- | --- |
| A CloudFormation stack, `openvidu-<name>` | Holds every resource below except the key pair; `--aws-stack-name` sets its name |
| EC2 instances | One for Single Node; master nodes and an auto scaling group of media nodes for Elastic and High Availability |
| Security groups, and an Elastic IP on Single Node and Elastic | The ports OpenVidu needs, open to the internet. High Availability is reached through its load balancer instead |
| A Network Load Balancer | High Availability only |
| An S3 bucket and an IAM user scoped to it | Recordings and OpenVidu Meet data. `--aws-app-data-bucket` uses your own bucket. High Availability adds a second bucket for the cluster's metrics and logs (`--param S3ClusterDataBucketName=<name>` uses your own) |
| A Secrets Manager secret | What the stack publishes: URL and credentials (and, on PRO, the access `ov` administers it with) |
| An EC2 key pair, `openvidu-<name>-key` | Only its public half; the private half stays in `.openvidu/aws/` |
| The bucket `openvidu-cfn-templates-<account>-<region>` | Stages the template, shared by every stack of the account in that region |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy --delete-data` (or `--keep-data`) in the directory removes whatever a failed deploy left behind.
