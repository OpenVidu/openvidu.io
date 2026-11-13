**`ov` prints the commands and runs none of them.** It only reads what it needs to write them (the default VPC, the instance types the region offers, and, with a domain, the Route 53 zone) and writes the rendered template and its parameters to `.openvidu/aws/`. This is the plan of a PRO stack named `pro`:

```text
── PLAN · nothing below has run ───────────────────────────────────────
Run these commands yourself in your AWS account (region us-east-1); ov runs none of them.
Once they have finished, run this same command again: ov finds the machines and ends the deploy.

  # SSH access: the key pair for this stack (.openvidu/aws/openvidu-pro-key.pem), its public half imported here.
  aws ec2 import-key-pair --key-name openvidu-pro-key --public-key-material fileb://.openvidu/aws/openvidu-pro-key.pub --region us-east-1
  …

Nothing above has been run. Once these commands have finished, run this same command again:

  ov stack deploy pro --cloud aws --mode assisted

It finds the machines, waits for OpenVidu to come up and registers this directory as the
stack. It creates nothing in your account.
── end of plan ────────────────────────────────────────────────────────
```

**Run them yourself**, with your own credentials. Read them first, and change them if you need to.

**Then run the command the plan ends with.** It needs no other flags, since every parameter is already in `openvidu-stack.yml`, but it **carries the stack's name** (`pro`): without it the stack would be registered as `openvidu`. When the CloudFormation stack is there as this deploy asks for it (complete, with the same parameters), `ov` finds the machines, waits for OpenVidu and registers the stack, creating nothing:

```text
The machines on AWS are there, as this deploy asks for them (CREATE_COMPLETE): it ends here,
creating nothing. It waits for OpenVidu to come up and registers this directory as the stack.

▶ Find the machines on AWS…
…
▶ Wait for the machines to deploy OpenVidu…
…
▶ Register the stack…
…
✔ OpenVidu Pro (single node) is up on AWS
```

While CloudFormation is still working (a status ending in `_IN_PROGRESS`), it says so and asks you to run the same command again later. If there is no stack yet, or its parameters differ from the ones this deploy asks for, it prints the commands again, saying first what differs when something does (the parameters, or what Terraform would change) (the update ones, on a stack that exists). With `--remote-state` it also prints the commands that save the stack's record, without running them, and settings a redeploy applies inside the stack (as `ov stack config set` does) are printed for you to run, not applied.
