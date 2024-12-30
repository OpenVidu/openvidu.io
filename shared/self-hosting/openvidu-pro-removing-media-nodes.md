
### Removing Media Nodes Gracefully

To stop a Media Node gracefully, you need to stop the containers `openvidu`, `ingress`, and `egress` with a `SIGINT` signal. Here is a simple script that you can use to stop all these containers gracefully:

```bash
#!/bin/bash
# Stop OpenVidu, Ingress, and Egress containers gracefully (1)
docker container kill --signal=SIGINT openvidu || true
docker container kill --signal=SIGINT ingress || true
docker container kill --signal=SIGINT egress || true

# Wait for the containers to stop (2)
while [ $(docker inspect -f '{{.State.Running}}' openvidu 2>/dev/null) == "true" ] || \
    [ $(docker inspect -f '{{.State.Running}}' ingress 2>/dev/null) == "true" ] || \
    [ $(docker inspect -f '{{.State.Running}}' egress 2>/dev/null) == "true" ]; do
    echo "Waiting for containers to stop..."
    sleep 5
done
```

1. This script stops the OpenVidu, Ingress, and Egress containers gracefully. The `true` at the end of each command is to avoid the script from stopping if the container is not running.
2. This script waits for the containers to stop before exiting.

When all the containers are stopped, you can then stop the systemd service and remove the VM:

```
sudo systemctl stop openvidu
```

### Removing Media Nodes Forcefully

To remove a Media Node forcefully, without considering the rooms, ingress, and egress processes running in the node, you can simply stop the OpenVidu service in the Media Node and delete the VM.

```bash
sudo systemctl stop openvidu
```
