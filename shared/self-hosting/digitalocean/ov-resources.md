| Resource | Notes |
| --- | --- |
| Droplets | One for Single Node; master nodes and an autoscaling pool of media nodes for Elastic and High Availability |
| A firewall | The ports OpenVidu needs, open to the internet (and outbound everywhere) |
| A VPC | Elastic and High Availability only |
| A load balancer | High Availability only |
| A Space and a bucket-scoped Spaces key | Recordings and OpenVidu Meet data; also the stack's secret store (`secrets.env`). High Availability has a second Space for the cluster's metrics and logs. `--param spaceName=<name>` uses your own |
| An SSH key pair and the stack's tag | The template generates the key; `ov` keeps the private half in `.openvidu/digitalocean/` |

`ov` records the stack's infrastructure in `openvidu-stack.yml` **before** creating it, so `ov stack destroy` in the directory removes whatever a failed deploy left behind.
