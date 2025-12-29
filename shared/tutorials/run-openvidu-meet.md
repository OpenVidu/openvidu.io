You need **Docker Desktop**. You can install it on [Windows :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/desktop/setup/install/windows-install/){:target="\_blank"}, [Mac :fontawesome-solid-external-link:{.external-link-icon}](https://docs.docker.com/desktop/setup/install/mac-install/){:target="\_blank"} or [Linux :fontawesome-solid-external-link:{.external-link-icon}](http://docs.docker.com/desktop/setup/install/linux/){:target="\_blank"}.

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.5.0 up -y openvidu-meet-init
```

!!! info

    For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally :fontawesome-solid-external-link:{.external-link-icon}](/meet/deployment/local.md){:target="\_blank"}.
