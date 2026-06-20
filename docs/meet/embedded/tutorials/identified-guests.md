---
title: Identified Guests Tutorial
description: Learn how to add identified guests with a fixed name and a unique access link to an OpenVidu Meet room using Node.js and JavaScript.
---

# Identified Guests Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.7.0/meet-identified-guests){ .md-button target=\_blank }

This tutorial extends the [Anonymous Access tutorial](./anonymous-access.md) to show how to add **identified guests** to an OpenVidu Meet room.

An identified guest is a room member with a **fixed name** and a **unique access link** that grants access to the room without any login. Each link is meant to be delivered privately to a single person and can be revoked individually.

Building on the Anonymous Access tutorial, it keeps the shared anonymous access links (access as `moderator` or `speaker`) and adds the following features:

- Add an identified guest to a room by name, with a base role (`moderator` or `speaker`).
- Each identified guest gets a unique access link that can be copied and shared.
- List and remove the members of a room, revoking their access.
- Access the room through a guest's unique link, with no login required.

The application uses the [OpenVidu Meet API](../../embedded/reference/rest-api.md) to manage rooms and room members, and the [OpenVidu Meet WebComponent](../reference/webcomponent.md) to embed the meeting.

!!! info "Anonymous guests vs. explicit members"

    OpenVidu Meet rooms can be accessed either through **shared anonymous links** (the moderator/speaker links from the [Anonymous Access tutorial](./anonymous-access.md)) or by adding **explicit room members** with personalized access and permissions. Identified guests are one of the two kinds of explicit room members (the other being [users](./users.md)). See the [Room Members :fontawesome-solid-external-link:{.external-link-icon}](../../features/room-members/overview.md){:target="\_blank"} feature for the full picture.

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
cd openvidu-meet-tutorials/meet-identified-guests
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

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/identified-guests-home.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/identified-guests-home.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/identified-guests-members.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/identified-guests-members.png" loading="lazy"/></a></p></div>

</div>

## Understanding the code

This tutorial builds upon the [Anonymous Access tutorial](./anonymous-access.md), adding identified guest management. We'll focus on the new features and modifications related to identified guests; the room creation/listing/deletion, the anonymous access links and the WebComponent embedding are inherited from the Anonymous Access tutorial.

---

### Backend modifications

Besides the usual room endpoints (`POST /rooms`, `GET /rooms`, `DELETE /rooms/:roomId`), the server exposes endpoints to manage the room members:

- **`POST /rooms/:roomId/members`**: Add an identified guest to a room.
- **`GET /rooms/:roomId/members`**: List the identified guests of a room.
- **`DELETE /rooms/:roomId/members/:memberId`**: Remove a member from a room.

---

#### Add an identified guest

The `POST /rooms/:roomId/members` endpoint adds an identified guest to a room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/src/index.js#L76-L101' target='_blank'>index.js</a>" linenums="76"
// Add an identified guest to a room
app.post('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params; // (1)!
	const { name, baseRole } = req.body; // (2)!

	if (!name || !baseRole) {
		res.status(400).json({ message: `'name' and 'baseRole' are required` });
		return;
	}

	try {
		// Add an identified guest to the room.
		// Providing 'name' (and no 'userId') creates a member of type 'identified_guest':
		// the API generates a unique 'memberId' (guest-XXXX) and a unique 'accessUrl'
		// that grants access to the room without any authentication.
		const member = await httpRequest('POST', `rooms/${roomId}/members`, {
			name, // (3)!
			baseRole // (4)!
		});

		console.log('Identified guest added:', member);
		res.status(201).json({ message: `Identified guest '${name}' added to room '${roomId}'`, member });
	} catch (error) {
		handleApiError(res, error, `Error adding identified guest '${name}' to room '${roomId}'`);
	}
});
```

1. The `roomId` is obtained from the request parameters.
2. The `name` of the identified guest and the `baseRole` are obtained from the request body.
3. The `name` is the fixed display name the participant will have in the meeting. Providing `name` (and **not** `userId`) is what tells the API to create a member of type `identified_guest`.
4. The `baseRole` (`moderator` or `speaker`) defines the default set of permissions for the member.

This endpoint adds the identified guest by sending a `POST` request to the `rooms/:roomId/members` endpoint. The API responds with the created member, which includes a generated `memberId` (in the form `guest-XXXX`) and a unique `accessUrl` such as `http://localhost:9080/meet/room/<roomId>?secret=guest-XXXX`. That URL is unique to this member and grants access to the room with no login required.

!!! info

    You can fine-tune the member's permissions beyond the base role by including a `customPermissions` object in the request. See the [`addRoomMember` operation :fontawesome-solid-external-link:{.external-link-icon}](../../embedded/reference/api.html#/operations/addRoomMember){:target="\_blank"} in the REST API reference for the full list of permissions.

---

#### List identified guests

The `GET /rooms/:roomId/members` endpoint lists the identified guests of a room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/src/index.js#L103-L114' target='_blank'>index.js</a>" linenums="103"
// List the identified guests of a room
app.get('/rooms/:roomId/members', async (req, res) => {
	const { roomId } = req.params;

	try {
		// List the identified guests of the room using the API (100 max)
		const { members } = await httpRequest('GET', `rooms/${roomId}/members?type=identified_guest&maxItems=100`); // (1)!
		res.status(200).json({ members });
	} catch (error) {
		handleApiError(res, error, `Error fetching members of room '${roomId}'`);
	}
});
```

1. List the room members by sending a `GET` request to the `rooms/:roomId/members` endpoint, filtering by `type=identified_guest` to retrieve only the identified guests.

---

#### Remove a member

The `DELETE /rooms/:roomId/members/:memberId` endpoint removes a member, revoking their unique link:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/src/index.js#L116-L128' target='_blank'>index.js</a>" linenums="116"
// Remove a member from a room
app.delete('/rooms/:roomId/members/:memberId', async (req, res) => {
	const { roomId, memberId } = req.params;

	try {
		// Removing a member revokes their access immediately
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

The home view keeps the shared anonymous access (access as moderator or speaker) and adds a **Members** button per room, which opens a dedicated members view to manage the room's identified guests.

---

#### The room list

The `getRoomListItemTemplate()` function renders each room with the inherited anonymous access buttons plus a new **Members** button:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/public/js/app.js#L55-L88' target='_blank'>app.js</a>" linenums="55"
function getRoomListItemTemplate(room) {
	return `
        <li class="list-group-item">
            <span>${room.roomName}</span>
            <div class="room-actions">
                <button
                    class="btn btn-primary btn-sm"
                    onclick="accessRoom('${room.access.anonymous.moderator.url}', '#home');"
                >
                    Access as Moderator
                </button>
                <button
                    class="btn btn-secondary btn-sm"
                    onclick="accessRoom('${room.access.anonymous.speaker.url}', '#home');"
                >
                    Access as Speaker
                </button>
                <button
					class="btn btn-success btn-sm"
					onclick="manageMembers('${room.roomId}');"
				>
                    Members
                </button>
                <button
                    title="Delete room"
                    class="icon-button delete-button"
                    onclick="deleteRoom('${room.roomId}');"
                >
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

The **Access as Moderator** and **Access as Speaker** buttons use the room's shared anonymous links (`room.access.anonymous.moderator.url` and `room.access.anonymous.speaker.url`) and are inherited from the Anonymous Access tutorial. The new **Members** button calls `manageMembers()`, which opens the members view for that room.

---

#### Rendering the members list

The `getMemberListItemTemplate()` function builds each member item, showing the name, the base role, the unique access link, and buttons to copy the link, access the room and remove the member:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/public/js/app.js#L198-L237' target='_blank'>app.js</a>" linenums="198"
function getMemberListItemTemplate(member) {
	// In this tutorial every member is an identified guest, so each one has a unique
	// access link and buttons to copy it, access the room through it and remove the member.
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
					title="Access as ${member.name}"
					class="icon-button"
					onclick="accessRoom('${member.accessUrl}', '#members')"
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

Each item displays the member's fixed `name`, a badge with its `baseRole`, and its unique `accessUrl`. The three buttons call `copyAccessUrl()` to copy the link to the clipboard, `accessRoom()` to access the room in the app through that link, and `removeMember()` to revoke the member.

---

#### Adding an identified guest

When the "Add guest" form is submitted, the `addGuest()` function creates the identified guest with the provided name and role:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/public/js/app.js#L239-L271' target='_blank'>app.js</a>" linenums="239"
async function addGuest(e) {
	// Prevent the default form submission
	e.preventDefault();

	// Clear previous error message
	const errorDiv = document.querySelector('#add-member-error');
	errorDiv.textContent = '';
	errorDiv.hidden = true;

	try {
		const name = document.querySelector('#guest-name').value; // (1)!
		const baseRole = document.querySelector('#guest-role').value;

		// Providing 'name' adds an identified guest (member of type 'identified_guest')
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
		console.error('Error adding guest:', error.message);

		// Show error message
		errorDiv.textContent = error.message || 'Error adding guest';
		errorDiv.hidden = false;
	}
}
```

1. Get the guest's `name` and the chosen `baseRole` from the form.
2. Make a `POST` request to the `/rooms/:roomId/members` endpoint to add the identified guest to the current room.
3. Add the returned member (including its generated `memberId` and unique `accessUrl`) to the local `members` map and re-render the list.

---

#### Copying the access link

The `copyAccessUrl()` function copies the member's unique link to the clipboard and briefly shows a confirmation:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/public/js/app.js#L285-L304' target='_blank'>app.js</a>" linenums="285"
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

#### Accessing the room

The `accessRoom()` function embeds the OpenVidu Meet WebComponent for a given room URL. It is shared by the anonymous access buttons and the per-guest access button:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.7.0/meet-identified-guests/public/js/app.js#L308-L337' target='_blank'>app.js</a>" linenums="308"
// Embed the OpenVidu Meet component for the given room URL.
// 'returnViewId' is the view to show again when the meeting is closed
// (the home screen for anonymous access, the members screen for an identified guest).
function accessRoom(roomUrl, returnViewId) {
	// Hide the home and members screens and show the room screen
	document.querySelector('#home').hidden = true;
	document.querySelector('#members').hidden = true;
	const roomScreen = document.querySelector('#room');
	roomScreen.hidden = false;

	// Inject the OpenVidu Meet component into the meeting container specifying the room URL
	const meetingContainer = document.querySelector('#meeting-container');
	meetingContainer.innerHTML = `
        <openvidu-meet
            room-url="${roomUrl}"
        >
        </openvidu-meet>
    `; // (1)!

	// Add event listener for when the OpenVidu Meet component is closed
	const meet = document.querySelector('openvidu-meet');
	meet.once('closed', () => {
		// (2)!
		console.log('OpenVidu Meet component closed');

		// Clear the component and go back to the view we came from
		meetingContainer.innerHTML = '';
		roomScreen.hidden = true;
		document.querySelector(returnViewId).hidden = false;
	});
}
```

1. Inject the OpenVidu Meet WebComponent with the `room-url` attribute set to the given URL. For an identified guest this is their unique `accessUrl`, which already carries the member's secret, so the participant enters the meeting directly with the fixed name and no login.
2. Add a listener for the `closed` event so that, when the component is closed, the meeting is cleared and the previous view is shown again (`returnViewId` is `#home` for anonymous access or `#members` for an identified guest).

!!! info "Embedding vs. sharing the link"

    This tutorial embeds the meeting in the app for convenience while testing, but the main purpose of an identified guest is its **unique access link**. In a real application you would typically deliver each member's `accessUrl` privately (by email, message, etc.) instead of opening it yourself, and the participant would access the room directly through that link.

## Accessing this tutorial from other computers or phones

--8<-- "shared/tutorials/access-tutorial-from-other-devices.md"

## Connecting this tutorial to an OpenVidu Meet production deployment

--8<-- "shared/tutorials/connect-tutorial-to-production-deployment.md"
