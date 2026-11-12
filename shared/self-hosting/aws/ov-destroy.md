One command deletes the machines too. The destroy deletes **only what belongs to the stack according to its record**, never anything matched by name. You must choose what happens to the recordings and OpenVidu Meet data: `--keep-data` leaves the S3 bucket (the template marks it `Retain`), `--delete-data` empties and deletes it. With neither flag, or both, nothing is deleted and the command stops (exit `2`).

```console
$ ov stack destroy -y --delete-data
This is what will be deleted from your AWS account:

  # The machines (for elastic/HA also their auto-scaling group and load balancer),
  # the Elastic IP, the security groups and the secret.
  …
  aws cloudformation delete-stack --stack-name openvidu-ce10 --region us-east-1

  # The key pair this stack's deploy imported.
  aws ec2 delete-key-pair --key-name openvidu-ce10-key --region us-east-1

  # The template this stack's deploy staged (the bucket stays: every stack in the
  # region shares it).
  aws s3 rm s3://openvidu-cfn-templates-123456789012-us-east-1/openvidu-ce10/ --recursive --only-show-errors --region us-east-1
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

A bucket of your own (named with `--param`) is not the stack's, so it stays either way. The bucket `openvidu-cfn-templates-<account>-<region>` stays too, because every stack of the region shares it.

- **`--keep-infrastructure`** tears the OpenVidu deployment down but leaves the instances running (and says so, because they still cost money). Use it to reinstall onto the same machines.
- **`--dry-run`** asks nothing and changes nothing: it prints exactly what the destroy would do with the same flags.
- A stack deployed with **`--remote-state`** also keeps its record and SSH key on AWS. The destroy deletes those too: the stack's objects in the template bucket and the Secrets Manager secret that held the SSH private key.

See [Destroy a stack](/docs/self-hosting/openvidu-cli.md#command-reference) for the options shared by every deployment.

!!! warning "Reusing a stack name"

    Secrets Manager deletes a secret only after a recovery window, so its name remains in use for several days. Until then, deploying a new stack with the same name in the same region fails. Free the name with `aws secretsmanager delete-secret --secret-id <secret> --force-delete-without-recovery`, where `<secret>` is the name the deploy printed on its `credentials:` line: `openvidu-<region>-openvidu-<name>` for a single node, `openvidu-elastic-<region>-openvidu-<name>` for Elastic, `openvidu-ha-<region>-openvidu-<name>` for High Availability. Or deploy with a different name, or in a different region.
