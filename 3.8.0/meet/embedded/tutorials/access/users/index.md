# Users Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.8.0/access/meet-users)

This tutorial extends the [Identified Guests tutorial](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/identified-guests/index.md) to show how to create **OpenVidu Meet users** with the Users API and add them to a room as **members**.

A user is a real OpenVidu Meet account. Whereas an identified guest accesses the room through a unique link without an account, all user members share the room's user access URL and prove their identity by logging in with their own OpenVidu Meet credentials. A room can therefore admit both users and identified guests as members, in addition to the anonymous access kept from the previous tutorials.

Building on the Identified Guests tutorial, it adds the following:

- Create, list and delete OpenVidu Meet users.
- Add a **user** (in addition to identified guests) as a member of a room.
- A user member accesses the room by logging in with their OpenVidu Meet credentials.

The application uses the [OpenVidu Meet API](https://openvidu.io/3.8.0/meet/embedded/reference/rest-api/index.md) to manage users, rooms and room members, and the [OpenVidu Meet WebComponent](https://openvidu.io/3.8.0/meet/embedded/reference/webcomponent/index.md) to embed the meeting.

Users, identified guests and anonymous guests

A room member can be a **user** (a real OpenVidu Meet account that authenticates with its credentials) or an **identified guest** (no account, accesses the room through a unique link). On top of explicit members, a room also accepts **anonymous guests** through the shared moderator/speaker links. See the [Room Members](https://openvidu.io/3.8.0/meet/features/room-members/overview/index.md) feature for the full picture.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.8.0 up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](https://openvidu.io/3.8.0/meet/deployment/local/index.md) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.8.0
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/access/meet-users
```

1. Install dependencies

```bash
npm install
```

1. Run the application

```bash
npm start
```

Once the server is up and running, you can test the application by visiting [`http://localhost:6080`](http://localhost:6080). You should see a screen like this:

## Understanding the code

This tutorial builds upon the [Identified Guests tutorial](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/identified-guests/index.md): the room management, the anonymous access, the identified-guest handling, the application views and the shared helper functions are the same. Here we focus only on what is new — the **Users API** — and on the **changes** needed so a room can admit both users and identified guests.

______________________________________________________________________

### Backend modifications

This tutorial adds three endpoints to manage users, and adapts two of the existing member endpoints:

- **`POST /users`**: Create a new OpenVidu Meet user. *(new)*
- **`GET /users`**: List the available users. *(new)*
- **`DELETE /users/:userId`**: Delete a user. *(new)*
- **`POST /rooms/:roomId/members`**: now adds either a **user** (`userId`) or an **identified guest** (`name`).
- **`GET /rooms/:roomId/members`**: now lists **all** members, without filtering by type.

The room endpoints (`POST /rooms`, `GET /rooms`, `DELETE /rooms/:roomId`) and the `DELETE /rooms/:roomId/members/:memberId` endpoint are identical to the [Identified Guests tutorial](https://openvidu.io/3.8.0/meet/embedded/tutorials/access/identified-guests/index.md).

______________________________________________________________________

#### Create user

The `POST /users` endpoint creates a new OpenVidu Meet user:

```javascript
// Create a new user
app.post('/users', async (req, res) => {
    const { userId, name, password } = req.body; // (1)!

    if (!userId || !name || !password) {
        res.status(400).json({ message: `'userId', 'name' and 'password' are required` }); // (2)!
        return;
    }

    try {
        // Create a new OpenVidu Meet user using the API.
        // The 'room_member' role lets the user access only the rooms where they are added as a member;
        // they cannot create or manage rooms (that would be the 'room_manager' or 'admin' roles).
        const user = await httpRequest('POST', 'users', {
            userId,
            name,
            password,
            role: 'room_member' // (3)!
        });

        console.log('User created:', user);
        res.status(201).json({ message: `User '${userId}' created successfully`, user }); // (4)!
    } catch (error) {
        handleApiError(res, error, `Error creating user '${userId}'`);
    }
});
```

1. The `userId`, `name` and `password` are obtained from the request body.
1. If any of them is missing, the server returns a `400 Bad Request` response.
1. The user is created with the `room_member` role. Among the available roles (`admin`, `room_manager` and `room_member`), `room_member` is the most restricted: it can only access the rooms where it has been explicitly added as a member, and cannot create or manage rooms.
1. The server returns a `201 Created` response with the created user object.

This endpoint creates a user with the OpenVidu Meet API by sending a `POST` request to the `users` endpoint, including the `userId`, `name`, `password` and `role`. The `userId` must be between 5 and 20 characters and contain only lowercase letters, numbers and underscores (this is validated in the frontend form).

______________________________________________________________________

#### List users

The `GET /users` endpoint retrieves the list of users:

```javascript
// List users
app.get('/users', async (_req, res) => {
    try {
        // List OpenVidu Meet users using the API (100 max).
        // We only list 'room_member' users, because they are the ones this tutorial creates.
        const { users } = await httpRequest('GET', 'users?role=room_member&maxItems=100'); // (1)!
        res.status(200).json({ users });
    } catch (error) {
        handleApiError(res, error, 'Error fetching users');
    }
});
```

1. Fetch the users by sending a `GET` request to the `users` endpoint, filtering by the `room_member` role (with a maximum of 100 users).

This endpoint lists only the `room_member` users. This keeps the tutorial focused on the users it creates and, in particular, excludes `admin` users, which cannot be added as room members.

______________________________________________________________________

#### Delete user

The `DELETE /users/:userId` endpoint deletes a user:

```javascript
// Delete a user
app.delete('/users/:userId', async (req, res) => {
    const { userId } = req.params; // (1)!

    try {
        // Delete the OpenVidu Meet user using the API.
        await httpRequest('DELETE', `users/${userId}`); // (2)!
        res.status(200).json({ message: `User '${userId}' deleted successfully` });
    } catch (error) {
        handleApiError(res, error, `Error deleting user '${userId}'`);
    }
});
```

1. The `userId` is obtained from the request parameters.
1. Delete the user by sending a `DELETE` request to the `users/:userId` endpoint.

______________________________________________________________________

#### Adapting the member endpoints

Adding a member uses the **same** `POST /rooms/:roomId/members` endpoint as the Identified Guests tutorial, but now accepts a `userId` (to add a user) in addition to a `name` (to add an identified guest). The field provided selects the member type:

```javascript
// Add a member to a room (either a user or an identified guest)
app.post('/rooms/:roomId/members', async (req, res) => {
    const { roomId } = req.params;
    const { userId, name, baseRole } = req.body; // (1)!

    if (!baseRole || (!userId && !name)) {
        res.status(400).json({
            message: `'baseRole' and either 'userId' (for a user) or 'name' (for an identified guest) are required`
        });
        return;
    }

    try {
        // Add a member to the room. The member type depends on which field is provided:
        // - 'userId' (and no 'name') adds a Meet user, creating a member of type 'user'.
        // - 'name' (and no 'userId') adds an identified guest, creating a member of type 'identified_guest'.
        const memberOptions = userId ? { userId, baseRole } : { name, baseRole }; // (2)!
        const member = await httpRequest('POST', `rooms/${roomId}/members`, memberOptions);

        console.log('Member added:', member);
        res.status(201).json({ message: `Member added to room '${roomId}'`, member });
    } catch (error) {
        handleApiError(res, error, `Error adding member to room '${roomId}'`);
    }
});
```

1. The request body now carries either a `userId` (the user to add) or a `name` (the identified guest to add), plus the `baseRole`.
1. If a `userId` is provided, the member is created as a `user` (linked to a user account); otherwise the `name` creates an `identified_guest`. Both are added through the same `rooms/:roomId/members` endpoint.

Listing members no longer filters by type, so both users and identified guests are returned:

```javascript
// List the members of a room (both users and identified guests)
app.get('/rooms/:roomId/members', async (req, res) => {
    const { roomId } = req.params;

    try {
        // List all the members of the room using the API (100 max)
        const { members } = await httpRequest('GET', `rooms/${roomId}/members?maxItems=100`); // (1)!
        res.status(200).json({ members });
    } catch (error) {
        handleApiError(res, error, `Error fetching members of room '${roomId}'`);
    }
});
```

1. The `type` filter from the Identified Guests tutorial is removed, so the endpoint returns every member of the room regardless of its type.

Removing a member (`DELETE /rooms/:roomId/members/:memberId`) is exactly the same as in the Identified Guests tutorial.

______________________________________________________________________

### Frontend modifications

The frontend adds a panel to manage users, lets the members view add **either a user or an identified guest**, and adds a **Access as user** action. The rooms management (including the anonymous access), the identified-guest handling and the shared helpers are unchanged from the Identified Guests tutorial.

______________________________________________________________________

#### Managing users

When the "Create User" form is submitted, the `createUser()` function is called:

```javascript
async function createUser(e) {
    // Prevent the default form submission
    e.preventDefault(); // (1)!

    // Clear previous error message
    const errorDiv = document.querySelector('#create-user-error');
    errorDiv.textContent = '';
    errorDiv.hidden = true;

    try {
        const userId = document.querySelector('#user-id').value; // (2)!
        const name = document.querySelector('#user-name').value;
        const password = document.querySelector('#user-password').value;

        const { user } = await httpRequest('POST', '/users', {
            userId,
            name,
            password
        }); // (3)!

        // Add the new user to the start (the API returns users newest first)
        prependToMap(users, user.userId, user); // (4)!
        renderUsers();

        // Reset the form
        e.target.reset();
    } catch (error) {
        console.error('Error creating user:', error.message);

        // Show error message
        errorDiv.textContent = error.message || 'Error creating user'; // (5)!
        errorDiv.hidden = false;
    }
}
```

1. Prevent the default form submission so the page is not reloaded.
1. Get the `userId`, `name` and `password` from the form inputs. The `user-id` input enforces the format constraints (5-20 characters, lowercase letters, numbers and underscores) through HTML validation attributes.
1. Make a `POST` request to the `/users` endpoint to create the user.
1. Add the new user to the start of the local `users` map (with the `prependToMap` helper, so newly created users appear first) and re-render the list.
1. If the request fails (for example, a duplicated `userId`), the error message returned by the API is shown in the form.

The `renderUsers()` and `deleteUser()` functions follow the same pattern as their room counterparts (`renderRooms()` and `deleteRoom()`): one renders the list of users from the `users` map, and the other calls `DELETE /users/:userId` and removes the user from the list.

______________________________________________________________________

#### Adding a member (user or identified guest)

The members view now has two add forms. The identified-guest form (and its `addGuest()` handler) is inherited from the previous tutorial. The new user form is populated from a dropdown of the users that are not already members of the room:

```javascript
// Populate the "add user" select with the users that are not already members of the room
function renderMemberUserOptions() {
    const select = document.querySelector('#member-user');
    const availableUsers = Array.from(users.values()).filter((user) => !members.has(user.userId)); // (1)!

    if (availableUsers.length === 0) {
        select.innerHTML = `<option value="" disabled selected>No users available</option>`;
        return;
    }

    select.innerHTML =
        `<option value="" disabled selected>Select a user</option>` +
        availableUsers.map((user) => `<option value="${user.userId}">${user.name} (${user.userId})</option>`).join(''); // (2)!
}
```

1. Filter out the users that are already members of the room (a user member's `memberId` equals the user's `userId`).
1. Build one `<option>` per available user, using the `userId` as the option value.

When the user form is submitted, the `addUser()` function adds the selected user as a member:

```javascript
async function addUser(e) {
    // Prevent the default form submission
    e.preventDefault();

    // Clear previous error message
    const errorDiv = document.querySelector('#add-member-error');
    errorDiv.textContent = '';
    errorDiv.hidden = true;

    try {
        const userId = document.querySelector('#member-user').value; // (1)!
        const baseRole = document.querySelector('#member-user-role').value;

        // Providing 'userId' adds a Meet user (member of type 'user')
        const { member } = await httpRequest('POST', `/rooms/${currentRoom.roomId}/members`, {
            userId,
            baseRole
        }); // (2)!

        // Add the new member to the start (the API returns members newest first)
        prependToMap(members, member.memberId, member);
        renderMembers();

        // Reset the form
        e.target.reset();
    } catch (error) {
        console.error('Error adding user:', error.message);

        // Show error message
        errorDiv.textContent = error.message || 'Error adding user';
        errorDiv.hidden = false;
    }
}
```

1. Get the selected `userId` from the dropdown and the chosen `baseRole`.
1. Make a `POST` request to the `/rooms/:roomId/members` endpoint with the `userId`, which adds the member as a `user`.

______________________________________________________________________

#### Rendering members of both types

The `getMemberListItemTemplate()` function now distinguishes the two member types: identified guests keep their unique link and copy/access buttons, while users only show a remove button (they access through the room's **Access as user** action):

```javascript
function getMemberListItemTemplate(member) {
    // A member can be a user (accesses the room by logging in) or an identified guest (accesses the room through a unique link)
    const isGuest = member.type === 'identified_guest'; // (1)!
    const typeLabel = isGuest ? 'Guest' : 'User';
    // For guests we show their unique access link; for users we show their member id (their user ID)
    const subtitle = isGuest ? member.accessUrl : member.memberId;

    // Guests have buttons to copy their unique link and to access the room through it.
    // Users access through the room's "Access as user" button instead, so they only have a remove button.
    const guestActions = isGuest // (2)!
        ? `
                <button
                    type="button"
                    title="Copy access link"
                    class="ov-icon-btn"
                    onclick="copyAccessUrl('${member.memberId}', this)"
                >
                    <span class="material-symbols-outlined">content_copy</span>
                </button>
                <button
                    type="button"
                    title="Access as ${member.name}"
                    class="ov-icon-btn"
                    onclick="accessRoom('${member.accessUrl}', '#members')"
                >
                    <span class="material-symbols-outlined">login</span>
                </button>`
        : '';

    return `
        <li class="ov-member">
            <div class="ov-member__info">
                <p class="ov-member__name">
                    ${member.name}
                    <span class="ov-badge ov-badge--${isGuest ? 'guest' : 'user'}">
                        <span class="material-symbols-outlined">${isGuest ? 'person' : 'verified_user'}</span>
                        ${typeLabel}
                    </span>
                    <span class="ov-badge ov-badge--${member.baseRole === 'moderator' ? 'moderator' : 'speaker'}">
                        <span class="material-symbols-outlined">${member.baseRole === 'moderator' ? 'shield_person' : 'record_voice_over'}</span>
                        ${member.baseRole}
                    </span>
                </p>
                <p class="ov-member__url" title="${subtitle}">${subtitle}</p>
            </div>
            <div class="ov-member__actions">
                ${guestActions}
                <button
                    type="button"
                    title="Remove member"
                    class="ov-icon-btn ov-icon-btn--danger"
                    onclick="removeMember('${member.memberId}')"
                >
                    <span class="material-symbols-outlined">delete</span>
                </button>
            </div>
        </li>
    `;
}
```

1. Detect the member type. `member.type` is `'identified_guest'` or `'user'`.
1. Only identified guests get the copy-link and access buttons (their access is the unique link). Users get just the remove button, plus a `User`/`Guest` badge so both types are easy to tell apart in the list.

______________________________________________________________________

#### Accessing the room as a user

All user members of a room share the same user access URL, available in the `access.user.url` property of the room object. The `accessAsUser()` function accesses the room through that URL, reusing the shared `accessRoom()` function from the previous tutorial:

```javascript
// Access the room as a user: all users share the same authenticated access URL.
// OpenVidu Meet shows its own login form inside the component until the user logs in.
function accessAsUser() {
    accessRoom(currentRoom.access.user.url, '#members');
}
```

`accessRoom()` is unchanged from the Identified Guests tutorial: it embeds the OpenVidu Meet WebComponent for the given URL and returns to the members view when the meeting is closed.

User members log in inside the meeting

The authenticated access URL (`access.user.url`) does not carry any secret. When the WebComponent loads it, OpenVidu Meet renders its **own login form inside the component**, and the user logs in with their OpenVidu Meet credentials (the `userId` and password created earlier). After logging in, OpenVidu Meet verifies that the user is a member of the room and lets them access the room with the permissions of their base role. Your application never handles the user's password: identity is proven through OpenVidu Meet's login, while membership and permissions are managed through the Room Members API.

## Accessing this tutorial from other computers or phones

To access this tutorial from other computers or phones, follow these steps:

1. **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

1. **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones](https://openvidu.io/3.8.0/meet/deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones) section.

1. **Update the OpenVidu Meet server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in your `.env` file to match the URL shown when OpenVidu Meet starts.

   ```text
   # Example for IP address 192.168.1.100
   OV_MEET_SERVER_URL=https://192-168-1-100.openvidu-local.dev:9443/meet
   ```

1. **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

   ```html
   <script src="http://192-168-1-100.openvidu-local.dev:9443/meet/v1/openvidu-meet.js"></script>
   ```

1. **Restart the tutorial** to apply the changes:

   ```bash
   npm start
   ```

1. **Access the tutorial**: Open your browser and navigate to `https://192-168-1-100.openvidu-local.dev:6443` (replacing `192-168-1-100` with your actual private IP) on the computer where you started the tutorial or any device in the same network.

## Connecting this tutorial to an OpenVidu Meet production deployment

If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps](https://openvidu.io/3.8.0/meet/deployment/basic/index.md) ), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

   ```text
   # Example for a production deployment
   OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com/meet
   ```

1. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key](https://openvidu.io/3.8.0/meet/embedded/reference/rest-api/#generate-an-api-key) section to learn how to obtain it.

   ```text
   OV_MEET_API_KEY=your-production-api-key
   ```

1. **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

   ```html
   <script src="https://your-openvidu-meet-domain.com/meet/v1/openvidu-meet.js"></script>
   ```

1. **Restart the tutorial** to apply the changes:

   ```bash
   npm start
   ```

Make this tutorial accessible from other computers or phones

By default, this tutorial runs on `http://localhost:6080` and is only accessible from the local machine. If you want to access it from other computers or phones, you have the following options:

- **Use tunneling tools**: Configure tools like [VS Code port forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding) , [ngrok](https://ngrok.com/) , [localtunnel](https://localtunnel.github.io/www/) , or similar services to expose this tutorial to the internet with a secure (HTTPS) public URL.
- **Deploy to a server**: Upload this tutorial to a web server and configure it to be accessible with a secure (HTTPS) public URL. This can be done by updating the source code to manage SSL certificates or configuring a reverse proxy (e.g., Nginx, Apache) to serve it.
