Before it touches your account, `ov` prints a **short plan**, one line per step, and waits for a yes: only `yes` or `y` goes ahead (`-y` answers in advance; it skips the question, never the plan). `--debug` prints the commands themselves, and [assisted mode](#review-the-commands-first-assisted-mode) prints them and runs nothing. This is a Single Node COMMUNITY deploy of a stack named `ce12d2` (ams3, 2026-10-29):

```text
This is what ov does in your DigitalOcean account (region ams3, Spaces in ams3); --debug shows every command:

  1. Template: render the single node template into .openvidu/digitalocean/tf-do-openvidu-singlenode.tf
     and its variables into .openvidu/digitalocean/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 1 minute, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

On Elastic the **Machines** step creates the master and the media nodes; on High Availability, the four masters and the media nodes.

Then `ov` creates the machines, waits for OpenVidu and registers the stack in this directory. The machines take a few minutes; most of the wait is OpenVidu installing on them. The deploy ends with the stack's address and how to read its credentials:

```text
…
✔ OpenVidu Community (single node) is up on DigitalOcean
  URL:          https://openvidu-324jl8-164-92-159-209.sslip.io/
  credentials:  env AWS_ACCESS_KEY_ID=$SPACES_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$SPACES_SECRET_ACCESS_KEY AWS_SESSION_TOKEN= aws s3 cp s3://openvidu-ce12d2-space-dae2e06c8c/secrets.env - --endpoint-url https://ams3.digitaloceanspaces.com
  SSH:          root@164.92.159.209 (key .openvidu/digitalocean/openvidu-ce12d2-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The Droplet gets the template's size, `s-4vcpu-8gb` (4 vCPU, 8 GB, 160 GB disk), unless you pass `--param instanceType=<slug>`. DigitalOcean logs you in as `root`.
