## Uninstalling OpenVidu

To uninstall any OpenVidu Node, just execute the following commands:

```bash
sudo su
systemctl stop openvidu
rm -rf /opt/openvidu/
rm /etc/systemd/system/openvidu.service
```
