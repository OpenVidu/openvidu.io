Depending on your [OpenVidu deployment type](../../docs/self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

	Run where `docker-compose.yaml` is located:

	```bash
	docker compose restart
	```

=== "OpenVidu Single Node"

	Run this command in your node:

	```bash
	sudo systemctl restart openvidu
	```

=== "OpenVidu Elastic"

	Run this command in your Master Node:

	```bash
	sudo systemctl restart openvidu
	```

=== "OpenVidu High Availability"

	Run this command in one of your Master Nodes:

	```bash
	sudo systemctl restart openvidu
	```

