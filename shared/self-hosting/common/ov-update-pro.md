**A release of `ov` deploys the same release of OpenVidu**: `ov` X.Y.Z deploys OpenVidu X.Y.Z. To update a stack, [install the `ov` of the version you want](/docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli) and run `ov stack update` from the stack's directory. Every plan and every message names the version the stack runs and the one it moves to.

```bash
ov stack update --dry-run   # the plan
ov stack update             # asks, then updates
```

Without `-y`, it asks for confirmation; with no terminal, `-y` is required. A stack that already runs this version says so and does nothing, and an older `ov` refuses to downgrade a stack.

The update installs this version of OpenVidu over the one the stack runs, with the values from the stack's configuration documents:

- **Your configuration is merged.** The documents (`openvidu.yaml` and the service files) are merged with this version's against the base kept in the cluster since the deploy or the last update: `openvidu.yaml` by values, the service files by lines. A setting the new version adds gets its default value; a default nobody touched moves to the new one; your values, comments and secrets stay. A value that both you and the new version changed is a conflict: the update stops before touching anything (exit `4`) and names it.
- **The plan comes from a dry run of the update itself:** each image that changes, the services whose instances are replaced and the values that move (secrets as `***`).
- **The nodes' disk is checked first:** the images each node lacks, against its free space. A node without enough free space stops the update (exit `9`).
- **A failure rolls back.** After confirmation, the update backs the documents up in the cluster, writes them, upgrades the stack and waits for it (`--wait-timeout`, 10 minutes by default). If the upgrade or the wait fails, it returns the stack to the version it ran and puts the documents back. `ov stack update --rollback` finishes a rollback that did not finish.

The update changes OpenVidu, not the machines: the nodes, their size and the number of media nodes stay as they are.
