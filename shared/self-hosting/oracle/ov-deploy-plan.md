Before it touches your tenancy, auto mode prints a short plan, one line per step, and waits for a yes (`-y` answers in advance; the plan is printed anyway). `--debug` prints the commands themselves, and [assisted mode](#assisted-mode) prints them and runs nothing. This is a Single Node COMMUNITY deploy of a stack named `ce12o` (eu-madrid-1, 2026-10-29; OCIDs and the Object Storage namespace shown as placeholders):

```text
This is what ov does in your Oracle Cloud tenancy (region eu-madrid-1, compartment ocid1.compartment.oc1..<compartment>); --debug shows every command:

  1. Template: render the single node template into .openvidu/oracle/tf-oracle-openvidu-singlenode.tf
     and its variables into .openvidu/oracle/openvidu.auto.tfvars.json (0600)
  2. Machines: create the machine, which installs OpenVidu Community on itself with Terraform (about 3 minutes, then OpenVidu installs)
  3. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

On Elastic the **Machines** step creates the master and the media nodes; on High Availability, the four masters and the media nodes.

Then `ov` creates the machines, waits for OpenVidu and registers the stack in this directory. The machines take a few minutes; most of the wait is OpenVidu installing on them. The deploy ends with the stack's address and how to read its credentials:

```text
…
✔ OpenVidu Community (single node) is up on Oracle Cloud
  URL:          https://openvidu-u57z2l-51-170-56-241.sslip.io/
  credentials:  oci secrets secret-bundle get-secret-bundle-by-name --secret-name OPENVIDU_URL --vault-id ocid1.vault.oc1.eu-madrid-1.<vault> --query 'data."secret-bundle-content".content' --raw-output --region eu-madrid-1 | base64 -d
  SSH:          ubuntu@51.170.56.241 (key .openvidu/oracle/openvidu-ce12o-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

On a single node the instance gets the template's shape, `VM.Standard.E4.Flex` with 4 OCPUs, unless you pass `--param instanceType=<shape>` (and `--param instanceOCPUs=<n>`, `--param instanceMemory=<gb>` for Flex shapes). COMMUNITY gets 8 GB and a 100 GB boot volume; PRO, which runs the whole cluster on one machine, gets 16 GB and a 200 GB boot volume.
