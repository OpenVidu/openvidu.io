# Users and permissions

## Participant roles in a room

Participants in a room can have different roles, which grant different permissions. The role of a participant is determined by the room link used to join. See [Room links](../rooms-and-meetings/#room-links) for more information.

Available roles are:

- **Moderator**: grants permissions to end the meeting, start/stop recordings, share room links and manage participants. Also grants permissions of `Speaker` role.
- **Speaker**: grants permissions to share their camera, microphone and screen.

### Changing participant roles during a meeting

Participants with `Moderator` role can upgrade or downgrade other participants' roles during the meeting from the "Participants" side panel:

## OpenVidu Meet authentication

OpenVidu Meet is by default protected with an administrator **username and password**. These credentials will be required when accessing OpenVidu Meet console:

The initial administrator credentials are:

- **Username**: **`admin`**
- **Password**: specified on installation time

The value of the password will be asked on installation. If left empty, a random password will be generated. The location of the administration password depends on the environment of the deployment:

Credentials are always username **`admin`** and password **`admin`**.

Credentials will be logged at the end of the installation process:

```text
OpenVidu Meet is available at:

    URL: https://<YOUR_DOMAIN>
    Credentials:
      - User: admin
      - Password: XXXXXXX
```

Warning

If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

In the Secrets Manager of the CloudFormation stack, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

Warning

If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

In the Azure Key Vault, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

Warning

If you [modify the initial administrator password](#modify-openvidu-meet-authentication), this value will no longer be valid.

### Modify OpenVidu Meet authentication

Administrator credentials can be modified from the **"User & Permissions"** view:
