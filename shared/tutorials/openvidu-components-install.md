To use OpenVidu Components Angular in your application, you need to install the library and import the `OpenViduComponentsModule` in your Angular module. Let's see how to do this:

1.	Create an Angular Project (version 17 or higher)

	To begin, you will need to create a new Angular project if you haven't already. Ensure you have Node.js and the Angular CLI installed. Then, run the following command to create a new Angular project:

	```bash
	ng new your-project-name
	```

	Replace `your-project-name` with the desired name for your project.

2.	Add Angular Material to your project

	OpenVidu Components Angular needs Angular Material, which provides a range of UI components. To add Angular Material to your project, navigate to your project directory and run:

	```bash
	ng add @angular/material
	```

3. 	Install OpenVidu Components Angular

	With your Angular project set up, it's time to add videoconferencing capabilities with OpenVidu Components Angular. Install the library using npm:

	```bash
	npm install openvidu-components-angular
	```

4.	Import and use OpenVidu Components Angular

	To use OpenVidu Components Angular in your application, you need to:

 	 1.	Import the `OpenViduComponentsModule` in your Angular application.
	 2. Configure the module with the `OpenViduComponentsConfig` object.
	 3. Add the component to your template file.
	 4. Assign the OpenVidu token and LiveKit URL to the component.
	 5. Customize the appearance of the components using CSS variables.

<!-- To use OpenVidu Components Angular in your application, you need to import the `OpenViduComponentsModule` in your Angular application. As you can use modules or standalone components, the import process will vary slightly depending on your application structure.

=== "Angular Standalone Components-based Application"

    In your main application file (commonly main.ts), import the OpenViduComponentsModule and configure it as follows:


    ```typescript title="<a href='#' target='_blank'>main.ts</a>" linenums="6"
    // Other imports ...

    import { OpenViduComponentsModule, OpenViduComponentsConfig } from 'openvidu-components-angular';

    const config: OpenViduComponentsConfig = {
    	production: true,
    };

    bootstrapApplication(AppComponent, {
    	providers: [
    		importProvidersFrom(
    			OpenViduComponentsModule.forRoot(config)
    			// Other imports ...
    		),
    		provideAnimations(),
    	],
    }).catch((err) => console.error(err));

    ```

=== "Angular Module-based Application"

    For module-based applications, you need to import the `OpenViduComponentsModule` in your Angular module. This module provides all the components and services required to build a videoconferencing application.

    ```typescript title="<a href='#' target='_blank'>app.module.ts</a>" linenums="6"
    // Other imports ...

    import { OpenViduComponentsModule, OpenViduComponentsConfig } from 'openvidu-components-angular';

    const config: OpenViduComponentsConfig = {
    	production: true,
    };

    @NgModule({
    	declarations: [
    		AppComponent,
    		// Other components ...
    	],
    	imports: [
    		BrowserModule,
    		OpenViduComponentsModule.forRoot(config),
    		// Other modules ...
    	],
    	providers: [],
    	bootstrap: [AppComponent],
    })
    export class AppModule {}
    ``` -->
