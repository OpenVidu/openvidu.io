Before it touches your subscription, the deploy prints a short plan, one line per step, and asks for confirmation (`-y` confirms in advance; the plan is printed anyway). `--debug` prints the commands themselves, and [assisted mode](#review-the-commands-first-assisted-mode) prints them and runs nothing. This is the plan of a Single Node COMMUNITY deploy of a stack named `ce12a` (northeurope, 2026-10-29):

```text
note: recorded this stack's infrastructure in openvidu-stack.yml, so the command that continues this deploy needs no flags
This is what ov does in your Azure subscription (location northeurope); --debug shows every command:

  1. SSH key: the stack's own key pair, its public half handed to the template (.openvidu/azure/openvidu-ce12a-key.pub)
  2. Template: render the single node template into .openvidu/azure/cf-openvidu-singlenode.bicep
  3. Resource group: create openvidu-ce12a-rg in northeurope
  4. Machines: Create the deployment openvidu-ce12a with the machine, which installs OpenVidu Community on itself (about 4 minutes)
  5. Wait for OpenVidu to answer, read the stack over SSH and register this directory as the stack

Run these in your account? Only yes or y goes ahead [y/N]:
```

On Elastic the **Machines** step creates the master and the media nodes; on High Availability, the four masters and the media nodes.

Then `ov` creates the machines, waits for OpenVidu and registers the stack in this directory. The machines take a few minutes; most of the wait is OpenVidu installing on them. The deploy ends with the stack's address and how to read its credentials:

```text
…
✔ OpenVidu Community (single node) is up on Azure
  URL:          https://openvidu-zclupo-40-112-77-3.sslip.io/
  credentials:  az keyvault secret show --vault-name openvidu-ce12a-keyvault --name OPENVIDU-URL --query value -o tsv
  SSH:          ubuntu@40.112.77.3 (key .openvidu/azure/openvidu-ce12a-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The VM gets the template's size, `Standard_D4s_v3`, and its OS disk, 100 GB on Community and 200 GB on PRO, which runs Kubernetes and its data tier there. On Single Node `--param instanceType=<size>` picks another size; on Elastic and High Availability the sizes are `masterNodeInstanceType` (`Standard_D4s_v3`) and `mediaNodeInstanceType` (`Standard_F8s_v2`), with a 100 GB disk on each media node.
