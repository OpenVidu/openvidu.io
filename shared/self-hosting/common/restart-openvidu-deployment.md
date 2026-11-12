Depending on your [OpenVidu deployment type](/docs/self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

	On Windows or macOS the stack runs with Docker Compose. Run where `docker-compose.yaml` is located:

	```bash
	docker compose restart
	```

	On Linux, OpenVidu Local is operated with the [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md): follow the other tab, from the local stack's directory.

=== "OpenVidu Single Node / Elastic / High Availability"

	Operate the stack with the [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md) from its directory. Turning an agent on or off is a live change with `ov stack agent`, which restarts only that agent across every node of the deployment:

	```bash
	ov stack agent enable agent-speech-processing
	# ov stack agent disable agent-speech-processing
	```

	A new agent definition you created is applied with `ov stack config file apply agent-<name>.yaml`. To restart every service of the deployment (for example after editing a service file by hand), run `ov stack restart`.
