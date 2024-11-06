The OpenVidu Components Angular library provides a set of CSS variables that you can use to customize the appearance of the components. You can define these variables in your application's global styles file (e.g. `styles.scss`).

```css
:root {
	/* Basic colors */
	--ov-background-color: #303030; // Background color
	--ov-surface-color: #ffffff; // Surfaces colors (panels, dialogs)

	/* Text colors */
	--ov-text-primary-color: #ffffff; // Text color over primary background
	--ov-text-surface-color: #1d1d1d; // Text color over surface background

	/* Action colors */
	--ov-primary-action-color: #273235; // Primary color for buttons, etc.
	--ov-secondary-action-color: #f1f1f1; // Secondary color for buttons, etc.
	--ov-accent-action-color: #0089ab; // Color for highlighted elements

	/* Status colors */
	--ov-error-color: #eb5144; // Error color
	--ov-warn-color: #ffba53; // Warning color

	/* Radius */
	--ov-toolbar-buttons-radius: 50%; // Radius for toolbar buttons
	--ov-leave-button-radius: 10px; // Radius for leave button
	--ov-video-radius: 5px; // Radius for videos
	--ov-surface-radius: 5px; // Radius for surfaces
}
```
