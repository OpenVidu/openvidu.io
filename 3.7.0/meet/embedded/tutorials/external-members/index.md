# OpenVidu Meet External Members Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.7.0/meet-external-members)

This tutorial extends the [basic OpenVidu Meet WebComponent tutorial](https://openvidu.io/3.7.0/meet/embedded/tutorials/webcomponent/index.md) to show how to add **external members** to an OpenVidu Meet room.

An external member is a participant with a **fixed name** and a **unique access link** that grants access to the room without any login. Each link is meant to be delivered privately to a single person and can be revoked individually.

Building on the basic tutorial, it adds the following features:

- Users can add an external member to a room by name, with a base role (`moderator` or `speaker`).
- Each external member gets a unique access link that can be copied and shared.
- Users can list and remove the members of a room, revoking their access.
- Anyone can join the meeting through a member's unique link, with no login required.

The application uses the [OpenVidu Meet API](https://openvidu.io/3.7.0/meet/embedded/reference/rest-api/index.md) to manage rooms and room members, and the [OpenVidu Meet WebComponent](https://openvidu.io/3.7.0/meet/embedded/reference/webcomponent/index.md) to embed the meeting.

Registered vs. external members

Room members can be either **registered members** (real OpenVidu Meet users, covered in the [Registered Members tutorial](https://openvidu.io/3.7.0/meet/embedded/tutorials/registered-members/index.md)) or **external members**. Registered members share the room's authenticated access URL and log in with their credentials; external members instead receive a **unique** access link that requires no authentication. See [Room Access](https://openvidu.io/3.7.0/meet/features/rooms/access/#room-members) for the full picture.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.7.0 up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](https://openvidu.io/3.7.0/meet/deployment/local/index.md) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.7.0
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-external-members
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

This tutorial builds upon the [basic OpenVidu Meet WebComponent tutorial](https://openvidu.io/3.7.0/meet/embedded/tutorials/webcomponent/index.md), adding external member management. We'll focus on the new features and modifications related to external members.

______________________________________________________________________

### Backend modifications

Besides the usual room endpoints (`POST /rooms`, `GET /rooms`, `DELETE /rooms/:roomId`), the server exposes endpoints to manage external members:

- **`POST /rooms/:roomId/members`**: Add an external member to a room.
- **`GET /rooms/:roomId/members`**: List the external members of a room.
- **`DELETE /rooms/:roomId/members/:memberId`**: Remove an external member from a room.

______________________________________________________________________

#### Add external member

The `POST /rooms/:roomId/members` endpoint adds an external member to a room:

```javascript
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
1. The `name` of the external member and the `baseRole` are obtained from the request body.
1. The `name` is the fixed display name the participant will have in the meeting. Providing `name` (and **not** `userId`) is what tells the API to create a member of type `external`.
1. The `baseRole` (`moderator` or `speaker`) defines the default set of permissions for the member.

This endpoint adds the external member by sending a `POST` request to the `rooms/:roomId/members` endpoint. The API responds with the created member, which includes a generated `memberId` (in the form `ext-XXXX`) and a unique `accessUrl` such as `http://localhost:9080/meet/room/<roomId>?secret=ext-XXXX`. That URL is unique to this member and grants access to the room with no login required.

Info

You can fine-tune the member's permissions beyond the base role by including a `customPermissions` object in the request. See the [`addRoomMember` operation](https://openvidu.io/3.7.0/meet/embedded/reference/api.html#/operations/addRoomMember) in the REST API reference for the full list of permissions.

______________________________________________________________________

#### List external members

The `GET /rooms/:roomId/members` endpoint lists the external members of a room:

```javascript
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

______________________________________________________________________

#### Remove external member

The `DELETE /rooms/:roomId/members/:memberId` endpoint removes an external member, revoking their unique link:

```javascript
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

______________________________________________________________________

### Frontend modifications

The client application now manages rooms from the home view and manages the external members of a room from a dedicated members view, where each member shows its unique access link. The main changes introduced in the frontend are in the `public/js/app.js` file, which now includes functions to render the members list, add a member, copy the access link and join the meeting through that link.

______________________________________________________________________

#### Rendering the members list

The `getMemberListItemTemplate()` function builds each member item, showing the name, the base role, the unique access link, and buttons to copy the link, join the meeting and remove the member:

```javascript
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

______________________________________________________________________

#### Adding an external member

When the "Add member" form is submitted, the `addMember()` function creates the external member with the provided name and role:

```javascript
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
1. Make a `POST` request to the `/rooms/:roomId/members` endpoint to add the external member to the current room.
1. Add the returned member (including its generated `memberId` and unique `accessUrl`) to the local `members` map and re-render the list.

______________________________________________________________________

#### Copying the access link

The `copyAccessUrl()` function copies the member's unique link to the clipboard and briefly shows a confirmation:

```javascript
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
1. Temporarily swap the copy icon for a check icon to confirm the link was copied. This unique link is what you would deliver privately to the intended participant.

______________________________________________________________________

#### Joining the room through a unique link

The `joinRoom()` function embeds the OpenVidu Meet WebComponent pointing to the member's unique `accessUrl`:

```javascript
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
1. Inject the OpenVidu Meet WebComponent with the `room-url` attribute set to that URL. Because the URL already carries the member's secret, the participant enters the meeting directly with the fixed name and no login.
1. Add a listener for the `closed` event so that, when the component is closed, the meeting is cleared and the members view is shown again.

Embedding vs. sharing the link

This tutorial embeds the meeting in the app for convenience while testing, but the main purpose of an external member is its **unique access link**. In a real application you would typically deliver each member's `accessUrl` privately (by email, message, etc.) instead of opening it yourself, and the participant would join directly through that link.

## Accessing this tutorial from other computers or phones

To access this tutorial from other computers or phones, follow these steps:

1. **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

1. **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones](https://openvidu.io/3.7.0/meet/deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones) section.

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

If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps](https://openvidu.io/3.7.0/meet/deployment/basic/index.md) ), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

   ```text
   # Example for a production deployment
   OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com/meet
   ```

1. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key](https://openvidu.io/3.7.0/meet/embedded/reference/rest-api/#generate-an-api-key) section to learn how to obtain it.

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
