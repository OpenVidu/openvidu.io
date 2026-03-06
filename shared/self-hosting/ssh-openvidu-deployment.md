Depending on your [OpenVidu deployment type](../../docs/self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

	If you are using [OpenVidu Local (Development)](../../docs/self-hosting/deployment-types.md#openvidu-local-development), simply navigate to the configuration folder of the project:

	```bash
	# For OpenVidu Local COMMUNITY
	cd openvidu-local-deployment/community

	# For OpenVidu Local PRO
	cd openvidu-local-deployment/pro
	```

=== "OpenVidu Single Node"

	If you are using [OpenVidu Single Node](../../docs/self-hosting/deployment-types.md#openvidu-single-node), SSH into the only OpenVidu node and navigate to:

	```bash
	cd /opt/openvidu/config
	```

=== "OpenVidu Elastic"

	If you are using [OpenVidu Elastic](../../docs/self-hosting/deployment-types.md#openvidu-elastic), SSH into the only Master Node and navigate to:

	```bash
	cd /opt/openvidu/config/cluster/media_node
	```

=== "OpenVidu High Availability"

	If you are using [OpenVidu High Availability](../../docs/self-hosting/deployment-types.md#openvidu-high-availability), SSH into any of your Master Nodes (doesn't matter which one) and navigate to:

	```bash
	cd /opt/openvidu/config/cluster/media_node
	```
