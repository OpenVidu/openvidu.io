# Creation & Management

Only **admin** users can manage other users — from the **"Users"** page of the OpenVidu Meet app or programmatically through the [REST API](#rest-api-reference). Any user can change their own password from their profile.

## Create a user

From the **"Users"** page, click **"Create User"** and provide a `userId`, a name and a [role](https://openvidu.io/3.8/meet/features/users/overview/#user-roles) (`admin`, `room_manager` or `room_member`). For the **temporary password**, you can either specify one or auto-generate one and then copy it.

Info

The `userId` must be between 5 and 20 characters and contain only lowercase letters, numbers and underscores.

\[[](../../../../assets/videos/meet/users/management/create-user-dark.mp4#only-dark)\](https://openvidu.io/3.8/assets/videos/meet/users/management/create-user-dark.mp4) \[[](../../../../assets/videos/meet/users/management/create-user-light.mp4#only-light)\](https://openvidu.io/3.8/assets/videos/meet/users/management/create-user-light.mp4)

Send the credentials to the user. On their **first login** they are required to change the temporary password before they can use OpenVidu Meet.

## Update a user's role

Change a user's [role](https://openvidu.io/3.8/meet/features/users/overview/#user-roles) from the user list at any time. The [root administrator](https://openvidu.io/3.8/meet/features/users/overview/#root-administrator) (**`admin`**) and your own account cannot be modified.

\[[](../../../../assets/videos/meet/users/management/update-user-role-dark.mp4#only-dark)\](https://openvidu.io/3.8/assets/videos/meet/users/management/update-user-role-dark.mp4) \[[](../../../../assets/videos/meet/users/management/update-user-role-light.mp4#only-light)\](https://openvidu.io/3.8/assets/videos/meet/users/management/update-user-role-light.mp4)

## Reset a user's password

Generate a new temporary password for a user from the user list (for example, if they forgot theirs). As with creation, the user must set a new password on their next login.

\[[](../../../../assets/videos/meet/users/management/reset-user-password-dark.mp4#only-dark)\](https://openvidu.io/3.8/assets/videos/meet/users/management/reset-user-password-dark.mp4) \[[](../../../../assets/videos/meet/users/management/reset-user-password-light.mp4#only-light)\](https://openvidu.io/3.8/assets/videos/meet/users/management/reset-user-password-light.mp4)

## List & filter users

The **"Users"** page lists every user with their role and registration date. You can search by name and filter by role.

Clicking a user opens their **profile page**, which shows the user's details together with buttons for every action you can perform on them: [update their role](#update-a-users-role), [reset their password](#reset-a-users-password) and [delete the user](#delete-users).

## Delete users

Users can be deleted individually or in bulk from the **"Users"** page. The root administrator cannot be deleted, and you cannot delete your own account. Deleting a user removes their account and automatically removes them from any room where they were a [member](https://openvidu.io/3.8/meet/features/room-members/overview/index.md). In addition:

- If the user **owns rooms**, ownership of those rooms is transferred to the [root administrator](https://openvidu.io/3.8/meet/features/users/overview/#root-administrator).
- If the user is **currently in a meeting**, they are kicked from it immediately.

\[[](../../../../assets/videos/meet/users/management/delete-user-dark.mp4#only-dark)\](https://openvidu.io/3.8/assets/videos/meet/users/management/delete-user-dark.mp4) \[[](../../../../assets/videos/meet/users/management/delete-user-light.mp4#only-light)\](https://openvidu.io/3.8/assets/videos/meet/users/management/delete-user-light.mp4)

## Changing your password

Any user can change their own password from their **Profile** page. You are asked to enter your **current password** and then type the **new password twice** to confirm it. Once changed, the new password is required the next time you log in.

## REST API reference

All of these operations can also be performed programmatically with the [OpenVidu Meet REST API](https://openvidu.io/3.8/meet/embedded/reference/rest-api/index.md). See the [REST API specification](https://openvidu.io/3.8/meet/embedded/reference/api.html) for the full list of available endpoints, request bodies and response schemas.

| Operation               | HTTP Method | Reference                                                                                           |
| ----------------------- | ----------- | --------------------------------------------------------------------------------------------------- |
| Create a user           | POST        | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/createUser)        |
| List users              | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getUsers)          |
| Bulk delete users       | DELETE      | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/bulkDeleteUsers)   |
| Get a user              | GET         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/getUser)           |
| Delete a user           | DELETE      | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/deleteUser)        |
| Reset a user's password | PUT         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/resetUserPassword) |
| Update a user's role    | PUT         | [Reference](https://openvidu.io/3.8/meet/embedded/reference/api.html#/operations/updateUserRole)    |
