By default, the stack's directory is the only place that drives the machines: if you lose it, you lose control of them. To operate the stack from another machine, deploy it (or redeploy it) with **`--remote-state`**, which keeps everything that drives the stack on AWS itself, so another machine with your AWS credentials can take it over completely. See [Remote state](/docs/self-hosting/openvidu-cli.md#remote-state) for the general picture.

On AWS, `--remote-state` keeps:

| What | Where |
| --- | --- |
| **The record** (infrastructure, no secrets) | the template bucket (`<stack>/registry/`) |
| **The SSH private key** `ov` generated | a Secrets Manager secret (`openvidu/<stack>/ssh-private-key`) |

CloudFormation keeps the infrastructure itself, so there is no Terraform state file to store.

The deploy prints where the record is in its last lines (an Elastic stack named `dpaws2`):

```console
✔ OpenVidu Pro (elastic) is up on AWS
  URL:          https://openvidu-239b62-51-95-197-8.sslip.io/
  credentials:  aws secretsmanager get-secret-value --secret-id openvidu-elastic-eu-south-2-openvidu-dpaws2 --query SecretString --output text --region eu-south-2
  record:       s3://openvidu-cfn-templates-123456789012-eu-south-2/openvidu-dpaws2/registry/openvidu-stack.yml (from another machine: ov stack import --cloud aws --stack-name openvidu-dpaws2)
  SSH key:      Secrets Manager secret openvidu/openvidu-dpaws2/ssh-private-key (the private half, for that import)
```

From an empty directory on another machine, `ov stack import --cloud aws` reads that record and registers the stack, infrastructure included. `--stack-name` takes the stack's name **on the cloud**, exactly as the `record:` line prints it (`openvidu-<name>`, not the directory's name). The record never holds a secret, so any parameter the template marks as sensitive, the license in particular, must be passed again:

```console
$ mkdir -p ~/stacks/dpaws2 && cd ~/stacks/dpaws2
$ ov stack import --cloud aws --aws-region eu-south-2 --stack-name openvidu-dpaws2 --openvidu-pro-license <license> -y
…
✔ imported the AWS stack openvidu-dpaws2 (elastic) into /home/me/stacks/dpaws2
  URL:          https://openvidu-239b62-51-95-197-8.sslip.io/
  SSH key:      both halves, the private one from the stack's secret store on the cloud.

From here, as from the directory that deployed it:
  ov stack status
  ov stack deploy dpaws2 --cloud aws --param Name=Value --mode auto   # change a template parameter
  ov stack destroy --keep-data   # or --delete-data: what becomes of the recordings
```

From then on, `ov stack status`, `ov stack deploy <name> --cloud aws --param …` and `ov stack destroy` work here as they did in the directory that deployed the stack (a destroy from the imported directory deletes the machines too). A Community stack is imported the same way, with no license: the import takes the SSH private key from the Secrets Manager secret and operates the stack over SSH. On a PRO stack, without `--openvidu-pro-license` the import stops before registering anything and says which flag is missing; `--mode assisted` prints the reads and runs nothing.

A stack deployed **without** `--remote-state` has no record to read, so no other machine can take over its infrastructure. A PRO stack can still be adopted another way, without the machines: `ov stack import --ssh <user>@<master>` (any master on High Availability), `sudo ov stack import --this-node` on the master itself, or `ov stack import -f <bundle>` from a file written by `ov stack export --bundle --out`. That registers OpenVidu, not the EC2 machines, so from such a directory you operate OpenVidu but cannot change the template or destroy the infrastructure: for that, keep the directory that deployed the stack, or deploy with `--remote-state`.
