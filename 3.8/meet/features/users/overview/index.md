# Users

OpenVidu Meet has a built-in user management system that controls access to the OpenVidu Meet app. **Users** are accounts identified by a `userId` and protected by a password. Each user is assigned a **role** that determines what they can do.

## User roles

Every user has one of the following roles:

| Role             | Description   | Permissions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **admin**        | Administrator | Full control over OpenVidu Meet: create and manage **all** [users](https://openvidu.io/3.8/meet/features/users/management/index.md), [rooms](https://openvidu.io/3.8/meet/features/rooms/overview/index.md), [room members](https://openvidu.io/3.8/meet/features/room-members/overview/index.md) and [recordings](https://openvidu.io/3.8/meet/features/recordings/overview/index.md). Can also change the system configuration — [room appearance](https://openvidu.io/3.8/meet/features/rooms/management/#room-appearance), [webhook configuration](https://openvidu.io/3.8/meet/embedded/reference/webhooks/index.md) and [API key](https://openvidu.io/3.8/meet/embedded/reference/rest-api/#generate-an-api-key). |
| **room_manager** | Room manager  | Can create and manage **their own** rooms, including their configuration, members and recordings. Can also access rooms — and their recordings, depending on their [member permissions](https://openvidu.io/3.8/meet/features/room-members/overview/#permissions) — where they are a member, or that are [open to all users](https://openvidu.io/3.8/meet/features/rooms/access/#member-access-links).                                                                                                                                                                                                                                                                                                                  |
| **room_member**  | Room member   | Can only access rooms — and their recordings, depending on their [member permissions](https://openvidu.io/3.8/meet/features/room-members/overview/#permissions) — where they are a member, or that are open to all users. Cannot create or manage rooms.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

Info

Roles control what a user can do in OpenVidu Meet as an account. The permissions a member has in a room are a separate concept. See [Room Members](https://openvidu.io/3.8/meet/features/room-members/overview/index.md) for more information on how member permissions work.

## Root administrator

The root administrator is a special user with the fixed `userId` **`admin`**. This user has full control over OpenVidu Meet and **cannot be deleted**. Its password is set during installation:

- In **local deployments**: the password is always **`admin`**.
- In **production deployments**: the password is specified during installation (or randomly generated if not provided).

These credentials are required to access the OpenVidu Meet app, at least for the first time, to create other users and manage the system:

\[[](../../../../assets/videos/meet/users/overview/login-dark.mp4#only-dark)\](https://openvidu.io/3.8/assets/videos/meet/users/overview/login-dark.mp4) \[[](../../../../assets/videos/meet/users/overview/login-light.mp4#only-light)\](https://openvidu.io/3.8/assets/videos/meet/users/overview/login-light.mp4)

The location of the initial administrator password depends on the deployment environment:

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

If you [change the administrator password](https://openvidu.io/3.8/meet/features/users/management/#changing-credentials), this value will no longer be valid.

In the Secrets Manager of the CloudFormation stack, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

Warning

If you [change the administrator password](https://openvidu.io/3.8/meet/features/users/management/#changing-credentials), this value will no longer be valid.

In the Azure Key Vault, in secret **`MEET_INITIAL_ADMIN_PASSWORD`**

Warning

If you [change the administrator password](https://openvidu.io/3.8/meet/features/users/management/#changing-credentials), this value will no longer be valid.

## How users access rooms

Users do not get access to a room just by having an account. Access works as follows:

- **Admins** and the **room owner** always have full access to a room, with all permissions granted.
- A user added as a [member](https://openvidu.io/3.8/meet/features/room-members/overview/index.md) of a room can access it through the **room's user access link**, logging in with their credentials.
- If a room is configured to be **accessible to all users**, any user can join — even without being an explicit member — with `Speaker` permissions.

See [Room Access](https://openvidu.io/3.8/meet/features/rooms/access/index.md) for the complete picture of how access to a room is granted.

## In this section

- [Creation & Management](https://openvidu.io/3.8/meet/features/users/management/index.md) — create users, update their role, reset passwords and delete users from the OpenVidu Meet app (admins only), change your own password, and the equivalent REST API operations.
