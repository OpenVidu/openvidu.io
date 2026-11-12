Depending on your [OpenVidu deployment type](/docs/self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

	If you are using [OpenVidu Local (Development)](/docs/self-hosting/deployment-types.md#openvidu-local-development) on Windows or macOS, the stack runs with Docker Compose. Navigate to the configuration folder of the project, where the `agent-<name>.yaml` files live:

	```bash
	# For OpenVidu Local COMMUNITY
	cd openvidu-local-deployment/community

	# For OpenVidu Local PRO
	cd openvidu-local-deployment/pro
	```

	On Linux, OpenVidu Local is deployed with the [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md): follow the other tab, from the local stack's directory.

=== "OpenVidu Single Node / Elastic / High Availability"

	These deployments are operated with the [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md) from the directory where you deployed the stack. You do not SSH into a node or edit files on it by hand: `ov stack config` reads and changes the stack's configuration on every node for you, and the agent definition files `agent-<name>.yaml` are documents of the stack.

	List the configuration documents, agents included, and open the one you need in your editor (`ov` applies it when you save). A new agent definition is a file you write on your machine and add with `ov stack config file apply agent-<name>.yaml`:

	```bash
	ov stack config file ls
	ov stack config file edit agent-speech-processing.yaml
	```
