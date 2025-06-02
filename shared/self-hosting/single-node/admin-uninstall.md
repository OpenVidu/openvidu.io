## Uninstalling OpenVidu

To uninstall OpenVidu, just execute the following commands:

```bash
sudo su
systemctl stop openvidu
rm -rf /opt/openvidu/
rm /etc/systemd/system/openvidu.service
rm /etc/sysctl.d/50-openvidu.conf
```
