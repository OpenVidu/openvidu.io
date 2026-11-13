One command deletes the machines too, and it must be told what happens to the recordings and OpenVidu Meet data: **`--keep-data`** leaves the S3 bucket, **`--delete-data`** empties and deletes it. On High Availability there are two buckets (application data and cluster data), and both flags act on both. With neither, the destroy is refused and nothing is touched. The destroy deletes only what the stack's record lists, never anything matched by name.

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your AWS account:

  # The machines (for elastic/HA also their auto-scaling group and load balancer),
  # the Elastic IP, the security groups and the secret.
  …
  aws cloudformation delete-stack --stack-name openvidu-ce10 --region us-east-1
…

▶ Delete the machine on AWS…
   · delete the CloudFormation stack openvidu-ce10 (instance, Elastic IP, security group, secret)
   · wait for the resources to go
   · deleted the bucket openvidu-appdata-d56324d0 and everything in it
   · delete the key pair openvidu-ce10-key
   · delete the template this deploy staged in s3://openvidu-cfn-templates-123456789012-us-east-1/openvidu-ce10/
   ✓ Delete the machine on AWS
✔ removed stack "ce10" from this directory
```

- **`--keep-infrastructure`** removes OpenVidu but leaves the machines running (and still costing money). It needs `--keep-data` or `--delete-data` too, which then act on the machines as on [your own servers](/docs/self-hosting/single-node/on-premises/admin.md#destroy); the S3 bucket stays either way.
- A stack deployed with **`--remote-state`** also loses what it kept on AWS: its objects in the template bucket and the secret that held the SSH private key.
- A bucket of your own (named with `--param`) and the shared `openvidu-cfn-templates-<account>-<region>` bucket are not the stack's, so they stay.

!!! warning "Reusing a stack name"

    Secrets Manager deletes a secret only after a recovery window, so for several days a new stack with the **same name in the same region** fails to deploy. Free the name with `aws secretsmanager delete-secret --secret-id <secret> --force-delete-without-recovery` (`<secret>` is the name on the deploy's `credentials:` line), or deploy with a different name or region.
