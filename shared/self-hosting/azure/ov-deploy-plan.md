Before it touches your subscription, the deploy prints a short plan, one line per step, and asks for confirmation (`-y` confirms in advance; the plan is printed anyway). This is the plan of a Single Node COMMUNITY deploy of a stack named `ce12a` (northeurope, 2026-10-29):

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

Every command is shown with `--debug`, and `--mode assisted` prints them all too. Azure takes its parameters on the `az deployment group create` line itself; on Community there is no separate parameters file (on PRO the license goes in a `0600` file, `.openvidu/azure/secure-parameters.json`, instead of the command line):

??? example "Every command (`--debug` and assisted mode)"

    ```text
    This is what will be done in your Azure subscription (location northeurope):

      # The key pair for this stack, its public half handed to the template (.openvidu/azure/openvidu-ce12a-key.pub).
      # Render the template (az compiles the Bicep itself): .openvidu/azure/cf-openvidu-singlenode.bicep
      az group create --name openvidu-ce12a-rg --location northeurope --only-show-errors -o none
      # Create the machine; it installs OpenVidu on itself. The command returns when Azure is done (about 4 minutes); OpenVidu comes up after.
      az deployment group create --resource-group openvidu-ce12a-rg --name openvidu-ce12a --template-file .openvidu/azure/cf-openvidu-singlenode.bicep --only-show-errors --query properties.provisioningState -o tsv --parameters certificateType=letsencrypt deployedBy=instance … stackName=openvidu-ce12a 'publicIpAddressObject={"newOrExistingOrNone":"new","name":"openvidu-ce12a-pip"}' adminSshKey="{\"sshPublicKey\":\"$(cat .openvidu/azure/openvidu-ce12a-key.pub)\"}"

      # What the stack published: URL and credentials, as secrets in the Key Vault the deployment outputs (OPENVIDU_URL appears once OpenVidu serves).
      az deployment group show --resource-group openvidu-ce12a-rg --name openvidu-ce12a --query properties.outputs -o json
      KV="$(az deployment group show --resource-group openvidu-ce12a-rg --name openvidu-ce12a --query properties.outputs.sharedInfoKeyVault.value -o tsv)"
      az keyvault secret show --vault-name $KV --name OPENVIDU-URL --query value -o tsv
    ```

Then `ov` runs the commands, waits for OpenVidu and registers the stack. The `az deployment group create` returns in about four minutes, once Azure has provisioned the VM but before OpenVidu is installed, so most of the waiting comes afterwards:

```text
▶ Create the machines on Azure…
   …
note: recorded this stack's infrastructure in openvidu-stack.yml, so `ov stack destroy` removes it even if the wait below fails
   ✓ Create the machines on Azure

▶ Wait for the machines to deploy OpenVidu…
   · waiting for OpenVidu to come up: the stack has not published its URL yet (OpenVidu is still installing)
   …
   · OpenVidu is up: the stack published its URL and https://openvidu-zclupo-40-112-77-3.sslip.io/health/caddy answers 200
   ✓ Wait for the machines to deploy OpenVidu

▶ Register the stack…
note: this stack was deployed on the machine itself, so its desired state named 127.0.0.1; retargeted at 40.112.77.3, the host this import reached
✔ registered stack "ce12a" in /home/me/ce12a
   ✓ Register the stack

✔ OpenVidu Community (single node) is up on Azure
  URL:          https://openvidu-zclupo-40-112-77-3.sslip.io/
  credentials:  az keyvault secret show --vault-name openvidu-ce12a-keyvault --name OPENVIDU-URL --query value -o tsv
  SSH:          ubuntu@40.112.77.3 (key .openvidu/azure/openvidu-ce12a-key.pem)

Try it:
  ov stack status
  ov stack logs --tail 50
```

The `retargeted` note is expected: the machine deployed OpenVidu on itself, and `ov` points your directory at its public address. The VM gets the template's size, `Standard_D4s_v3`, and its OS disk, 100 GB on Community and 200 GB on PRO, which runs Kubernetes and its data tier there. On Single Node `--param instanceType=<size>` picks another size; on Elastic and High Availability the sizes are `masterNodeInstanceType` (`Standard_D4s_v3`) and `mediaNodeInstanceType` (`Standard_F8s_v2`), with a 100 GB disk on each media node.
