By default, the stack's directory is the only place that drives the machines: lose it and you lose control of them. A deploy with **`--remote-state`** also keeps the stack on Azure, so another machine with access to the subscription can take it over completely. `ov` keeps:

- the **record** (the infrastructure, never a secret) in a Blob container (`openvidu-registry`) of a storage account the template creates for it in the stack's resource group;
- the **SSH private key** `ov` generated in the stack's Key Vault (`OPENVIDU-SSH-PRIVATE-KEY`).

The deploy prints where, on its `record:` line. From an empty directory on another machine, `ov stack import --cloud azure` reads that record and registers the stack, infrastructure included, so `ov stack destroy` and `--param` redeploys work from there too:

```bash
ov stack import --cloud azure --azure-resource-group <group> --stack-name <name> \
  --openvidu-pro-license <license> -y
```

`--stack-name` is the name you deployed the stack as (`<name>`), not the name of the directory. From it `ov` resolves the stack's name **on the cloud**, which the `record:` line prints: `openvidu-<name>`, or `ov-<name>` where Azure shortens the prefix to fit the Key Vault's 24-character limit. The record holds no secret, so the license (and any other parameter the template marks sensitive) must be passed again, exactly as it was given to the deploy. A Community stack is imported the same way, with no license. See [Remote state](/docs/self-hosting/openvidu-cli.md#remote-state) for the general command and how `--remote-state` works across clouds.

!!! warning "Azure Policy may forbid shared key access"

    `ov` writes and reads the record with the storage account's key (`--auth-mode key`), which needs shared key access on the account. Where an Azure Policy of your organization forbids it, `--remote-state` cannot keep the record on Azure: a policy that **denies** it fails the deploy with `RequestDisallowedByPolicy` (deploy without `--remote-state`), and one that **turns it off** lets the deploy finish with a warning but keeps no record (and the import then says so). Keep the directory that deployed the stack, or carry it with `ov stack export --bundle --out <file>` and `ov stack import -f <file>`.
