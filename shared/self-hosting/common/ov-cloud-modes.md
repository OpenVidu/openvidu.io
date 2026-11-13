Choose how the deploy runs with `--mode` (without it, `ov` asks):

- **`--mode auto`**: `ov` runs every command for you, with your own cloud CLI and credentials. It first shows [its plan](#what-the-deploy-runs) and asks once before creating anything; `-y` answers yes in advance. The commands on this page use it.
- **`--mode assisted`**: `ov` runs **nothing** in your account. It prints the commands; you review them and run them yourself, with your own credentials. Then you run the same `ov stack deploy` again, and `ov` finds the machines, waits for OpenVidu and registers the stack in this directory, creating nothing. See [Assisted mode](#assisted-mode).
