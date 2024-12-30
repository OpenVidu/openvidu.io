The OpenVidu Components Angular library provides a set of CSS variables that you can use to customize the appearance of the components. You can define these variables in your application's global styles file (e.g. `styles.scss`).

```css
:root {
	--ov-primary-color: #303030; /* Primary interface color */
	--ov-secondary-color: #3e3f3f; /* Secondary interface color */
	--ov-tertiary-color: #598eff; /* Tertiary accent color for elements */
	--ov-warn-color: #eb5144; /* Warning color for alerts and notifications */
	--ov-light-color: #e6e6e6; /* Light color for elements */

	--ov-accent-color: #ffae35; /* Accent color for standout UI elements */

	--ov-logo-background-color: #3a3d3d; /* Background color for the logo area */
	--ov-text-color: #ffffff; /* Default text color */

	--ov-panel-text-color: #1d1d1d; /* Text color for panel elements */
	--ov-panel-background: #ffffff; /* Background color for panels */

	--ov-buttons-radius: 50%; /* Border-radius for circular buttons */
	--ov-leave-button-radius: 10px; /* Border-radius for the leave button */
	--ov-video-radius: 5px; /* Border-radius for video elements */
	--ov-panel-radius: 5px; /* Border-radius for panel elements */
}
```
