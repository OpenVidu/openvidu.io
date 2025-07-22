# Web Component

## Overview

A comprehensive guide to integrating and using the web component in your applications.

## Installation

To use the OpenVidu Meet web component, include the following script in your HTML:

```html
<script src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet.js"></script>
```

## Quick Start

### Basic Usage

To use the OpenVidu Meet web component, simply add the `<openvidu-meet>` tag to your HTML. This will create a basic meeting interface.

```html
<openvidu-meet room-url="{{ my-room-url }}"></openvidu-meet>
```

### With Configuration

```html
<openvidu-meet
	room-url="{{ my-room-url }}"
	participant-name="John Doe"
></openvidu-meet>
```

## API Reference

### Properties

--8<-- "shared/meet/webcomponent-attributes.md"

### Commands

--8<-- "shared/meet/webcomponent-commands.md"

### Events

--8<-- "shared/meet/webcomponent-events.md"

## Examples

TODO: INCLUDE EXAMPLES HERE

- Basic Example
- Advanced Example with Customization
- Listen for events and handle them accordingly.
- Sending commands to the component.
