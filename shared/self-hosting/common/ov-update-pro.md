**A release of `ov` deploys the same release of OpenVidu**: `ov` X.Y.Z deploys OpenVidu X.Y.Z. To update a stack, [install the `ov` of the version you want](/docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli) and run `ov stack update` from the stack's directory. Every plan and every message names the version the stack runs and the one it moves to.

```bash
ov stack update --dry-run   # the plan
ov stack update             # asks, then updates
```

Without `-y`, it asks for confirmation; with no terminal, `-y` is required. A stack that already runs this version says so and does nothing, and an older `ov` refuses to downgrade a stack.

- **Your configuration is merged.** `openvidu.yaml` and the service files are merged with this version's: your values, comments and secrets stay, and new settings get their defaults. A value that both you and the new version changed is a conflict: the update stops before touching anything and names it.
- **The plan** lists each image that changes, the services that restart and the values that move (secrets as `***`).
- **The nodes' disk is checked first.** A node without enough free space stops the update before anything changes.
- **A failure rolls back** to the version the stack ran, with its documents. `ov stack update --rollback` finishes a rollback that did not finish.

The update changes OpenVidu, not the machines: the nodes, their size and the number of media nodes stay as they are.

**The `ov` on the node.** A deploy leaves its `ov` at `/usr/local/bin/ov` on the node, and once the stack runs the new version that older `ov` refuses every change. When the update reaches the node over the SSH login the deploy recorded, it replaces that `ov` itself. Otherwise (a cloud stack, or one deployed with `--this-node` and updated from elsewhere) it ends with a note: replace `/usr/local/bin/ov` on the node with the new `ov` yourself ([Install the OpenVidu CLI](/docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli)).
