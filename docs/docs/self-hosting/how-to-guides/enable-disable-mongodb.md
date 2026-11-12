---
title: "Enable and disable the bundled MongoDB"
description: "Control the bundled MongoDB service, the database behind OpenVidu Dashboard, OpenVidu Meet and analytics storage, with the OpenVidu CLI."
---

# Enable and disable MongoDB

OpenVidu stores application data in MongoDB for these services:

- OpenVidu Dashboard
- OpenVidu Meet
- Analytics (sent by OpenVidu Server)

## MongoDB follows the modules

MongoDB is one of OpenVidu's **data services** (`redis`, `mongodb` and `minio`). You never start or stop it directly: it comes up because a module needs it (the `dashboard` and `meet` modules), and it goes away when no module needs it anymore. So the usual way to stop running MongoDB is to [disable the modules](enable-disable-modules.md) that depend on it:

```bash
ov stack module rm dashboard
ov stack module rm meet
```

Keep in mind that disabling those modules disables the features they provide.

## Force it on a Community server

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    On a Community server MongoDB has its own setting, `openviduStack.mongo.enabled`. Set it with the CLI, which applies the change and recreates only the affected services:

    ```bash
    # Disable the bundled MongoDB service (and the services that depend on it)
    ov stack config set openviduStack.mongo.enabled=false

    # Enable it again
    ov stack config set openviduStack.mongo.enabled=true
    ```

    If you want to use an external MongoDB instead of the bundled one, check the [Use an external MongoDB](external-mongodb.md) guide.

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    On Kubernetes MongoDB follows the module selection and has no `mongo.enabled` setting of its own: add or remove the `dashboard` and `meet` modules as shown above, and MongoDB comes up or down with them.

After applying the change, confirm with `ov stack status` that the expected services (OpenVidu Dashboard, OpenVidu Meet, analytics) can connect to MongoDB.
