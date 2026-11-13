Before it touches your project, `--mode auto` shows a **short plan**: one numbered line per step, what is done and where, without the commands. Then it asks whether to run it, and only `yes` or `y` goes ahead (`-y` answers in advance, and the plan still appears; no answer or any other answer creates nothing). `--debug` prints the commands themselves, and [assisted mode](#assisted-mode) prints them and runs nothing. This is the plan of a Single Node COMMUNITY deploy of a stack named `ce12g` (europe-west2, 2026-10-29):

```text
This is what ov does in your Google Cloud project my-project (region europe-west2, zone europe-west2-b); --debug shows every command:

  1. Template: render the single node template into .openvidu/gcp/tf-gpc-openvidu-singlenode.tf
     and its variables into .openvidu/gcp/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 2 minutes, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

On Elastic the **Machines** step creates the master and the media nodes; on High Availability, the four masters and the media nodes.

Then `ov` creates the machines, waits for OpenVidu and registers the stack in this directory. The machines take a few minutes; most of the wait is OpenVidu installing on them. The deploy ends with the stack's address and how to read its credentials:

```text
…
✔ OpenVidu Community (single node) is up on Google Cloud
  URL:          https://openvidu-uj9zj7-34-105-214-170.sslip.io/
  credentials:  gcloud secrets versions access latest --secret=openvidu-ce12g-OPENVIDU_URL --project=my-project  (every secret starts with openvidu-ce12g-)
  SSH:          ubuntu@34.105.214.170 (key .openvidu/gcp/openvidu-ce12g-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

In this Single Node COMMUNITY example the instance gets the template's machine type, `e2-standard-4`, and a 100 GiB `pd-balanced` boot disk, unless you pass `--param instanceType=<type>`.
