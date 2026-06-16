---
title: OpenVidu Meet User Members Tutorial
description: Learn how to create OpenVidu Meet users with the Users API and grant them access to a room as user members using Node.js and JavaScript.
---

# OpenVidu Meet User Members Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.7.0/meet-registered-members){ .md-button target=\_blank }

This tutorial extends the [Identified Guest Members tutorial](./external-members.md) to show how to create **OpenVidu Meet users** with the Users API and grant them access to a room as **user members**.

Whereas an identified guest joins through a unique link without an account, a user member is a real OpenVidu Meet user added to a specific room: all user members share the room's authenticated access URL and prove their identity by logging in with their own OpenVidu Meet credentials.

Building on the Identified Guest Members tutorial, it adds the following:

- Create, list and delete OpenVidu Meet users.
- Add a **user** (instead of a guest) as a member of a room.
- A user member joins the room by logging in with their OpenVidu Meet credentials.

The application uses the [OpenVidu Meet API](../../embedded/reference/rest-api.md) to manage users, rooms and room members, and the [OpenVidu Meet WebComponent](../reference/webcomponent.md) to embed the meeting.

!!! info "Anonymous guests vs. explicit members"

    OpenVidu Meet rooms can be accessed either through **shared anonymous links** (used by the other tutorials) or by adding **explicit room members** with personalized access and permissions. User members are one of the two kinds of explicit room members (the other being [identified guests](./external-members.md)). See the [Room Members :fontawesome-solid-external-link:{.external-link-icon}](../../features/room-members/overview.md){:target="\_blank"} feature for the full picture.

## Running this tutorial

#### 1. Run OpenVidu Meet

--8<-- "shared/tutorials/run-openvidu-meet.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.7.0
```

### 3. Run the application

To run this application, you need [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/en/download){:target="\_blank"} (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-registered-members
```

2. Install dependencies

```bash
npm install
```

3. Run the application

```bash
npm start
```

Once the server is up and running, you can test the application by visiting [`http://localhost:6080`](http://localhost:6080){:target="\_blank"}. You should see a screen like this:

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/registered-members-home.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/registered-members-home.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/registered-members-members.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/registered-members-members.png" loading="lazy"/></a></p></div>

</div>

## Understanding the code

This tutorial builds upon the [Identified Guest Members tutorial](./external-members.md): the room and member management, the application views and the shared helper functions are the same. Here we focus only on what is new — the **Users API** — and on the **small changes** needed to manage **user** members instead of guests.

---

### Backend modifications

This tutorial adds three endpoints to manage users, and slightly changes two of the existing member endpoints:

- **`POST /users`**: Create a new OpenVidu Meet user. _(new)_
- **`GET /users`**: List the available users. _(new)_
- **`DELETE /users/:userId`**: Delete a user. _(new)_
- **`POST /rooms/:roomId/members`**: now adds a **user** member, identified by `userId` instead of `name`.
- **`GET /rooms/:roomId/members`**: now filters by `type=registered`.

The room endpoints (`POST /rooms`, `GET /rooms`, `DELETE /rooms/:roomId`) and the `DELETE /rooms/:roomId/members/:memberId` endpoint are identical to the [Identified Guest Members tutorial](./external-members.md).

---

#### Create user

The `POST /users` endpoint creates a new OpenVidu Meet user:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/src/index.js#L28-L52' target='_blank'>index.js</a>" linenums="28"
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
		// they cannot create or manage rooms.
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
2. If any of them is missing, the server returns a `400 Bad Request` response.
3. The user is created with the `room_member` role. Among the available roles (`admin`, `room_manager` and `room_member`), `room_member` is the most restricted: it can only access the rooms where it has been explicitly added as a member, and cannot create or manage rooms.
4. The server returns a `201 Created` response with the created user object.

This endpoint creates a user with the OpenVidu Meet API by sending a `POST` request to the `users` endpoint, including the `userId`, `name`, `password` and `role`. The `userId` must be between 5 and 20 characters and contain only lowercase letters, numbers and underscores (this is validated in the frontend form). The `role` is set to `room_member`. Among the available roles (`admin`, `room_manager` and `room_member`), `room_member` is the most restricted: it can only access the rooms where it has been explicitly added as a member, and cannot create or manage rooms.

---

#### List users

The `GET /users` endpoint retrieves the list of users:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/src/index.js#L54-L64' target='_blank'>index.js</a>" linenums="54"
// List users
app.get('/users', async (_req, res) => {
	try {
		// List OpenVidu Meet users using the API (100 max).
		// We only list 'room_member' users, because they are the ones this tutorial creates
		const { users } = await httpRequest('GET', 'users?role=room_member&maxItems=100'); // (1)!
		res.status(200).json({ users });
	} catch (error) {
		handleApiError(res, error, 'Error fetching users');
	}
});
```

1. Fetch the users by sending a `GET` request to the `users` endpoint, filtering by the `room_member` role (with a maximum of 100 users).

This endpoint lists only the `room_member` users. This keeps the tutorial focused on the users it creates and, in particular, excludes the root `admin` user, which cannot be deleted nor added as a room member.

---

#### Delete user

The `DELETE /users/:userId` endpoint deletes a user:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/src/index.js#L66-L76' target='_blank'>index.js</a>" linenums="66"
// Delete a user
app.delete('/users/:userId', async (req, res) => {
	const { userId } = req.params; // (1)!

	try {
		await httpRequest('DELETE', `users/${userId}`); // (2)!
		res.status(200).json({ message: `User '${userId}' deleted successfully` });
	} catch (error) {
		handleApiError(res, error, `Error deleting user '${userId}'`);
	}
});
```

1. The `userId` is obtained from the request parameters.
2. Delete the user by sending a `DELETE` request to the `users/:userId` endpoint.

Deleting a user removes their account from OpenVidu Meet. Note that this will automatically remove the user from rooms where they are a member

---

#### Adapting the member endpoints

Adding a member uses the **same** `POST /rooms/:roomId/members` endpoint as the Identified Guest Members tutorial, but provides a `userId` instead of a `name`. This is the only difference, and it is what tells the API to create a member of type `registered` (linked to a user account) instead of `external`:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/src/index.js#L130-L153' target='_blank'>index.js</a>" linenums="130"
// Add a registered user as a member of a room
app.post('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params;
	const { userId, baseRole } = req.body; // (1)!

	if (!userId || !baseRole) {
		res.status(400).json({ message: `'userId' and 'baseRole' are required` });
		return;
	}

	try {
		// Add the registered user as a member of the room.
		// Providing 'userId' (and no 'name') creates a member of type 'registered':
		// the member is linked to the user account and identified through authentication.
		const member = await httpRequest('POST', `rooms/${roomId}/members`, {
			userId, // (2)!
			baseRole
		});

		console.log('Member added:', member);
		res.status(201).json({ message: `User '${userId}' added to room '${roomId}'`, member });
	} catch (error) {
		handleApiError(res, error, `Error adding user '${userId}' to room '${roomId}'`);
	}
});
```

1. The request body now carries a `userId` (the user to add) instead of a `name`.
2. Providing `userId` (and **not** `name`) is what tells the API to create a member of type `registered`. The member is linked to the user account, identified through authentication, and shares the same authenticated room access URL with the rest of the user members.

!!! info

    As in the Identified Guest Members tutorial, you can fine-tune the member's permissions beyond the base role by including a `customPermissions` object in the request. See the [`addRoomMember` operation :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="\_blank"} in the REST API reference for the full list of permissions.

Listing members works the same way, but filters by `type=registered` instead of `type=external`:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/src/index.js#L156-L166' target='_blank'>index.js</a>" linenums="156"
// List the members of a room (only registered members)
app.get('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params;

	try {
		// List the registered members of the room using the API (100 max)
		const { members } = await httpRequest('GET', `rooms/${roomId}/members?type=registered&maxItems=100`); // (1)!
		res.status(200).json({ members });
	} catch (error) {
		handleApiError(res, error, `Error fetching members of room '${roomId}'`);
	}
});
```

1. The only change from the Identified Guest Members tutorial is the `type=registered` filter, which retrieves the user members instead of the identified guests.

Removing a member (`DELETE /rooms/:roomId/members/:memberId`) is exactly the same as in the Identified Guest Members tutorial: it revokes the member's access immediately and expels them if they are currently in the meeting.

---

### Frontend modifications

The frontend adds a panel to manage users and adapts the members view to add **existing users** as members. The `joinRoom()` function also changes to join through the room's authenticated URL. The rest (rooms management, view switching and the `httpRequest()` wrapper) is unchanged from the Identified Guest Members tutorial.

---

#### Managing users

When the "Create User" form is submitted, the `createUser()` function is called:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/public/js/app.js#L71-L104' target='_blank'>app.js</a>" linenums="71"
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

		// Add new user to the list
		users.set(user.userId, user); // (4)!
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
2. Get the `userId`, `name` and `password` from the form inputs. The `user-id` input enforces the format constraints (5-20 characters, lowercase letters, numbers and underscores) through HTML validation attributes.
3. Make a `POST` request to the `/users` endpoint to create the user.
4. Add the new user to the local `users` map and re-render the list.
5. If the request fails (for example, a duplicated `userId`), the error message returned by the API is shown in the form.

The `renderUsers()` and `deleteUser()` functions follow the same pattern as their room counterparts in the Identified Guest Members tutorial (`renderRooms()` and `deleteRoom()`): one renders the list of users from the `users` map, and the other calls `DELETE /users/:userId` and removes the user from the list.

---

#### Adapting the members view

In the Identified Guest Members tutorial you typed a free-text name to add a member. Here you instead pick one of the existing users from a dropdown, which is populated with the users that are not yet members of the room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/public/js/app.js#L297-L309' target='_blank'>app.js</a>" linenums="297"
// Populate the "add member" select with the users that are not already members of the room
function renderMemberUserOptions() {
	const select = document.querySelector('#member-user');
	const availableUsers = Array.from(users.values()).filter((user) => !members.has(user.userId)); // (1)!

	if (availableUsers.length === 0) {
		select.innerHTML = `<option value="" disabled selected>No users available</option>`;
		return;
	}

	select.innerHTML =
		`<option value="" disabled selected>Select a user</option>` +
		availableUsers.map((user) => `<option value="${user.userId}">${user.userId} · ${user.name}</option>`).join(''); // (2)!
}
```

1. Filter out the users that are already members of the room (a user member's `memberId` equals the user's `userId`).
2. Build one `<option>` per available user, using the `userId` as the option value.

When the form is submitted, the `addMember()` function sends the selected `userId` (instead of a `name`) to the backend:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/public/js/app.js#L336-L364' target='_blank'>app.js</a>" linenums="336"
async function addMember(e) {
	// Prevent the default form submission
	e.preventDefault();

	// Clear previous error message
	const errorDiv = document.querySelector('#add-member-error');
	errorDiv.textContent = '';
	errorDiv.hidden = true;

	try {
		const userId = document.querySelector('#member-user').value; // (1)!
		const baseRole = document.querySelector('#member-role').value;

		const { member } = await httpRequest('POST', `/rooms/${currentRoom.roomId}/members`, {
			userId,
			baseRole
		}); // (2)!

		// Add new member to the list
		members.set(member.memberId, member); // (3)!
		renderMembers();
	} catch (error) {
		console.error('Error adding member:', error.message);

		// Show error message
		errorDiv.textContent = error.message || 'Error adding member';
		errorDiv.hidden = false;
	}
}
```

1. Get the selected `userId` from the dropdown and the chosen `baseRole`.
2. Make a `POST` request to the `/rooms/:roomId/members` endpoint to add the member to the current room (`currentRoom` is the room whose members are being managed).
3. Add the returned member to the local `members` map and re-render the list.

The way each member is rendered also changes slightly: since user members do not have an individual access link, the `getMemberListItemTemplate()` function shows the member's id (its `userId`) and a single button to remove them — there is no copy-link or per-member join button like in the Identified Guest Members tutorial. Instead, joining is done once per room, as shown next.

---

#### Joining the room as a user member

All user members of a room share the same authenticated access URL, available in the `access.registered.url` property of the room object. The `joinRoom()` function embeds the OpenVidu Meet WebComponent pointing to that URL:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-registered-members/public/js/app.js#L380-L413' target='_blank'>app.js</a>" linenums="380"
function joinRoom() {
	// All registered members share the same authenticated access URL for the room.
	// Each member proves their identity by logging in with their OpenVidu Meet credentials.
	const roomUrl = currentRoom.access.registered.url; // (1)!
	console.log(`Joining room through URL: ${roomUrl}`);

	// Hide the members screen and show the room screen
	const membersScreen = document.querySelector('#members');
	membersScreen.hidden = true;
	const roomScreen = document.querySelector('#room');
	roomScreen.hidden = false;

	// Inject the OpenVidu Meet component into the meeting container specifying the room URL.
	// Since this URL requires authentication, OpenVidu Meet will show its own login form
	// inside the component until the member logs in.
	const meetingContainer = document.querySelector('#meeting-container');
	meetingContainer.innerHTML = `
        <openvidu-meet
            room-url="${roomUrl}"
        >
        </openvidu-meet>
    `; // (2)!

	// Add event listener for when the OpenVidu Meet component is closed
	const meet = document.querySelector('openvidu-meet');
	meet.once('closed', () => {
		// (3)!
		console.log('OpenVidu Meet component closed');

		// Clear the component and go back to the members screen
		meetingContainer.innerHTML = '';
		roomScreen.hidden = true;
		membersScreen.hidden = false;
	});
}
```

1. Get the room's authenticated access URL from the `access.registered.url` property. Unlike the Identified Guest Members tutorial (where each member had its own unique URL), this URL is the same for all user members.
2. Inject the OpenVidu Meet WebComponent with the `room-url` attribute set to that URL.
3. Add a listener for the `closed` event so that, when the component is closed, the meeting is cleared and the members view is shown again.

!!! info "Registered members log in inside the meeting"

    The authenticated access URL does not carry any secret. When the WebComponent loads it, OpenVidu Meet renders its **own login form inside the component**, and the member logs in with their OpenVidu Meet credentials (the `userId` and password created earlier). After logging in, OpenVidu Meet verifies that the user is a member of the room and lets them join with the permissions of their base role. Your application never handles the member's password: identity is proven through OpenVidu Meet's login, while membership and permissions are managed through the Room Members API.

## Accessing this tutorial from other computers or phones

--8<-- "shared/tutorials/access-tutorial-from-other-devices.md"

## Connecting this tutorial to an OpenVidu Meet production deployment

--8<-- "shared/tutorials/connect-tutorial-to-production-deployment.md"
