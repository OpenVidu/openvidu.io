---
title: OpenVidu Meet External Members Tutorial
description: Learn how to add external members with a fixed name and a unique access link to an OpenVidu Meet room using Node.js and JavaScript.
---

# OpenVidu Meet External Members Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.7.0/meet-external-members){ .md-button target=\_blank }

This tutorial extends the [basic OpenVidu Meet WebComponent tutorial](./webcomponent.md) to show how to add **external members** to an OpenVidu Meet room.

An external member is a participant with a **fixed name** and a **unique access link** that grants access to the room without any login. Each link is meant to be delivered privately to a single person and can be revoked individually.

Building on the basic tutorial, it adds the following features:

- Users can add an external member to a room by name, with a base role (`moderator` or `speaker`).
- Each external member gets a unique access link that can be copied and shared.
- Users can list and remove the members of a room, revoking their access.
- Anyone can join the meeting through a member's unique link, with no login required.

The application uses the [OpenVidu Meet API](../../embedded/reference/rest-api.md) to manage rooms and room members, and the [OpenVidu Meet WebComponent](../reference/webcomponent.md) to embed the meeting.

!!! info "Registered vs. external members"

    Room members can be either **registered members** (real OpenVidu Meet users, covered in the [Registered Members tutorial](./registered-members.md)) or **external members**. Registered members share the room's authenticated access URL and log in with their credentials; external members instead receive a **unique** access link that requires no authentication. See [Room Access :fontawesome-solid-external-link:{.external-link-icon}](../../features/rooms/access.md#room-members){:target="\_blank"} for the full picture.

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
cd openvidu-meet-tutorials/meet-external-members
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

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/external-members-home.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/external-members-home.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/external-members-members.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/external-members-members.png" loading="lazy"/></a></p></div>

</div>

## Understanding the code

This tutorial builds upon the [basic OpenVidu Meet WebComponent tutorial](./webcomponent.md), adding external member management. We'll focus on the new features and modifications related to external members.

---

### Backend modifications

Besides the usual room endpoints (`POST /rooms`, `GET /rooms`, `DELETE /rooms/:roomId`), the server exposes endpoints to manage external members:

- **`POST /rooms/:roomId/members`**: Add an external member to a room.
- **`GET /rooms/:roomId/members`**: List the external members of a room.
- **`DELETE /rooms/:roomId/members/:memberId`**: Remove an external member from a room.

---

#### Add external member

The `POST /rooms/:roomId/members` endpoint adds an external member to a room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/src/index.js#L77-L101' target='_blank'>index.js</a>" linenums="77"
// Add an external member to a room
app.post('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params; // (1)!
	const { name, baseRole } = req.body; // (2)!

	if (!name || !baseRole) {
		res.status(400).json({ message: `'name' and 'baseRole' are required` });
		return;
	}

	try {
		// Add an external member to the room.
		// Providing 'name' (and no 'userId') creates a member of type 'external':
		// the API generates a unique 'memberId' (ext-XXXX) and a unique 'accessUrl'
		// that grants access without any authentication.
		const member = await httpRequest('POST', `rooms/${roomId}/members`, {
			name, // (3)!
			baseRole // (4)!
		});

		console.log('External member added:', member);
		res.status(201).json({ message: `External member '${name}' added to room '${roomId}'`, member });
	} catch (error) {
		handleApiError(res, error, `Error adding external member '${name}' to room '${roomId}'`);
	}
});
```

1. The `roomId` is obtained from the request parameters.
2. The `name` of the external member and the `baseRole` are obtained from the request body.
3. The `name` is the fixed display name the participant will have in the meeting. Providing `name` (and **not** `userId`) is what tells the API to create a member of type `external`.
4. The `baseRole` (`moderator` or `speaker`) defines the default set of permissions for the member.

This endpoint adds the external member by sending a `POST` request to the `rooms/:roomId/members` endpoint. The API responds with the created member, which includes a generated `memberId` (in the form `ext-XXXX`) and a unique `accessUrl` such as `http://localhost:9080/meet/room/<roomId>?secret=ext-XXXX`. That URL is unique to this member and grants access to the room with no login required.

!!! info

    You can fine-tune the member's permissions beyond the base role by including a `customPermissions` object in the request. See the [`addRoomMember` operation :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="\_blank"} in the REST API reference for the full list of permissions.

---

#### List external members

The `GET /rooms/:roomId/members` endpoint lists the external members of a room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/src/index.js#L104-L114' target='_blank'>index.js</a>" linenums="104"
// List the external members of a room
app.get('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params;

	try {
		// List the external members of the room using the API (100 max)
		const { members } = await httpRequest('GET', `rooms/${roomId}/members?type=external&maxItems=100`); // (1)!
		res.status(200).json({ members });
	} catch (error) {
		handleApiError(res, error, `Error fetching members of room '${roomId}'`);
	}
});
```

1. List the room members by sending a `GET` request to the `rooms/:roomId/members` endpoint, filtering by `type=external` to retrieve only the external members.

---

#### Remove external member

The `DELETE /rooms/:roomId/members/:memberId` endpoint removes an external member, revoking their unique link:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/src/index.js#L117-L128' target='_blank'>index.js</a>" linenums="117"
// Remove an external member from a room
app.delete('/rooms/:roomId/members/:memberId', async (req, res) => {
	const { roomId, memberId } = req.params;

	try {
		// Removing a member revokes their unique access link immediately
		// (they are expelled if currently in a meeting)
		await httpRequest('DELETE', `rooms/${roomId}/members/${memberId}`); // (1)!
		res.status(200).json({ message: `Member '${memberId}' removed from room '${roomId}'` });
	} catch (error) {
		handleApiError(res, error, `Error removing member '${memberId}' from room '${roomId}'`);
	}
});
```

1. Remove the member by sending a `DELETE` request to the `rooms/:roomId/members/:memberId` endpoint. The member's unique link stops working immediately; if they are currently in the meeting, they are expelled from it.

---

### Frontend modifications

The client application now manages rooms from the home view and manages the external members of a room from a dedicated members view, where each member shows its unique access link. The main changes introduced in the frontend are in the `public/js/app.js` file, which now includes functions to render the members list, add a member, copy the access link and join the meeting through that link.

---

#### Rendering the members list

The `getMemberListItemTemplate()` function builds each member item, showing the name, the base role, the unique access link, and buttons to copy the link, join the meeting and remove the member:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/public/js/app.js#L187-L224' target='_blank'>app.js</a>" linenums="187"
function getMemberListItemTemplate(member) {
	return `
        <li class="member-container">
            <div class="member-info">
                <p class="member-name">
                    ${member.name}
                    <span class="badge ${member.baseRole === 'moderator' ? 'bg-primary' : 'bg-secondary'}">
                        ${member.baseRole}
                    </span>
                </p>
                <p class="member-url" title="${member.accessUrl}">${member.accessUrl}</p>
            </div>
            <div class="member-actions">
                <button 
					title="Copy access link" 
					class="icon-button" 
					onclick="copyAccessUrl('${member.memberId}', this)"
				>
                    <i class="fa-solid fa-copy"></i>
                </button>
                <button 
					title="Join" 
					class="icon-button" 
					onclick="joinRoom('${member.memberId}')"
				>
                    <i class="fa-solid fa-right-to-bracket"></i>
                </button>
                <button 
					title="Remove member" 
					class="icon-button delete-button" 
					onclick="removeMember('${member.memberId}')"
				>
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

Each item displays the member's fixed `name`, a badge with its `baseRole`, and its unique `accessUrl`. The three buttons call `copyAccessUrl()` to copy the link to the clipboard, `joinRoom()` to open the meeting in the app, and `removeMember()` to revoke the member.

---

#### Adding an external member

When the "Add member" form is submitted, the `addMember()` function creates the external member with the provided name and role:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/public/js/app.js#L226-L257' target='_blank'>app.js</a>" linenums="226"
async function addMember(e) {
	// Prevent the default form submission
	e.preventDefault();

	// Clear previous error message
	const errorDiv = document.querySelector('#add-member-error');
	errorDiv.textContent = '';
	errorDiv.hidden = true;

	try {
		const name = document.querySelector('#member-name').value; // (1)!
		const baseRole = document.querySelector('#member-role').value;

		const { member } = await httpRequest('POST', `/rooms/${currentRoom.roomId}/members`, {
			name,
			baseRole
		}); // (2)!

		// Add new member to the list
		members.set(member.memberId, member); // (3)!
		renderMembers();

		// Reset the form
		e.target.reset();
	} catch (error) {
		console.error('Error adding member:', error.message);

		// Show error message
		errorDiv.textContent = error.message || 'Error adding member';
		errorDiv.hidden = false;
	}
}
```

1. Get the member's `name` and the chosen `baseRole` from the form.
2. Make a `POST` request to the `/rooms/:roomId/members` endpoint to add the external member to the current room.
3. Add the returned member (including its generated `memberId` and unique `accessUrl`) to the local `members` map and re-render the list.

---

#### Copying the access link

The `copyAccessUrl()` function copies the member's unique link to the clipboard and briefly shows a confirmation:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/public/js/app.js#L271-L290' target='_blank'>app.js</a>" linenums="271"
async function copyAccessUrl(memberId, button) {
	const member = members.get(memberId);
	if (!member) {
		return;
	}

	try {
		await navigator.clipboard.writeText(member.accessUrl); // (1)!

		// Briefly show a confirmation icon
		const icon = button.querySelector('i');
		const previousClass = icon.className;
		icon.className = 'fa-solid fa-check'; // (2)!
		setTimeout(() => {
			icon.className = previousClass;
		}, 1500);
	} catch (error) {
		console.error('Error copying access link:', error.message);
	}
}
```

1. Copy the member's unique `accessUrl` to the clipboard using the Clipboard API.
2. Temporarily swap the copy icon for a check icon to confirm the link was copied. This unique link is what you would deliver privately to the intended participant.

---

#### Joining the room through a unique link

The `joinRoom()` function embeds the OpenVidu Meet WebComponent pointing to the member's unique `accessUrl`:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-external-members/public/js/app.js#L294-L329' target='_blank'>app.js</a>" linenums="294"
function joinRoom(memberId) {
	const member = members.get(memberId);
	if (!member) {
		return;
	}

	// Each external member has its own unique access URL. Opening it grants access
	// to the meeting as that member, with the fixed name and no login required.
	const roomUrl = member.accessUrl; // (1)!

	// Hide the members screen and show the room screen
	const membersScreen = document.querySelector('#members');
	membersScreen.hidden = true;
	const roomScreen = document.querySelector('#room');
	roomScreen.hidden = false;

	// Inject the OpenVidu Meet component into the meeting container specifying the member's unique URL
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

1. Get the member's unique `accessUrl`.
2. Inject the OpenVidu Meet WebComponent with the `room-url` attribute set to that URL. Because the URL already carries the member's secret, the participant enters the meeting directly with the fixed name and no login.
3. Add a listener for the `closed` event so that, when the component is closed, the meeting is cleared and the members view is shown again.

!!! info "Embedding vs. sharing the link"

    This tutorial embeds the meeting in the app for convenience while testing, but the main purpose of an external member is its **unique access link**. In a real application you would typically deliver each member's `accessUrl` privately (by email, message, etc.) instead of opening it yourself, and the participant would join directly through that link.

## Accessing this tutorial from other computers or phones

--8<-- "shared/tutorials/access-tutorial-from-other-devices.md"

## Connecting this tutorial to an OpenVidu Meet production deployment

--8<-- "shared/tutorials/connect-tutorial-to-production-deployment.md"
