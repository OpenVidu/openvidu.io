
In your `main.ts` application file, import the it and configure it as follows:

```typescript
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
