# Angular Components

## Introduction

Angular Components are the simplest way to create real-time videoconferencing apps with Angular. There's no need to manage state or low-level events; Angular Components from OpenVidu handle all the complexity for you.

This **Angular library**, offers developers a robust set of **powerful and comprehensive videoconferencing components**. These components are highly adaptable, extendable, and easily replaceable, allowing you to tailor them to your application's specific requirements.

Angular Components

The primary goal of the OpenVidu team is to minimize the developer's effort when creating videoconferencing applications. **Angular Components** significantly contribute to this objective for several reasons:

- **Rapid Development**

  ______________________________________________________________________

  Abstracts the complexity of videoconferencing applications, allowing you to focus on customizations

- **Flexible Customization**

  ______________________________________________________________________

  Offers maximum customization flexibility, allowing you to adapt, extend, and replace any component

- **Easy Maintenance**

  ______________________________________________________________________

  Ensures your code remains up to date, making it easier to update your application with each new OpenVidu release

## How to use

Using Angular Components in your application is straightforward. The official [Angular Components Tutorials](../../tutorials/angular-components/) cover everything Angular Components offers, from customizing colors and branding logos to injecting new custom features.

## Featured Components

- **Videoconference**

  ______________________________________________________________________

  The Videoconference component is the core of Angular Components. You can nest HTML and Angular components inside it or leave it empty to use the default setup.

  ______________________________________________________________________

  [See Reference](../../reference-docs/openvidu-components-angular/components/VideoconferenceComponent.html)

- **Panel**

  ______________________________________________________________________

  The Panel components is the root of side panels in the videoconference. You can nest HTML and Angular components inside it or leave it empty to use the default setup.

  ______________________________________________________________________

  [See Reference](../../reference-docs/openvidu-components-angular/components/PanelComponent.html)

## Prefabricated Components

**Angular Components** provides a wide range of prefabricated components that you can use to build your videoconferencing application in a matter of minutes. These components are designed for direct use without any extensions or modifications.

[Toolbar](../../reference-docs/openvidu-components-angular/components/ToolbarComponent.html) [Layout](../../reference-docs/openvidu-components-angular/components/LayoutComponent.html) [Stream](../../reference-docs/openvidu-components-angular/components/StreamComponent.html) [ChatPanel](../../reference-docs/openvidu-components-angular/components/ChatPanelComponent.html) [ParticipantsPanel](../../reference-docs/openvidu-components-angular/components/ParticipantsPanelComponent.html) [ParticipantPanelItem](../../reference-docs/openvidu-components-angular/components/ParticipantPanelItemComponent.html) [ActivitiesPanel](../../reference-docs/openvidu-components-angular/components/ActivitiesPanelComponent.html) [RecordingActivity](../../reference-docs/openvidu-components-angular/components/RecordingActivityComponent.html) [BroadcastingActivity](../../reference-docs/openvidu-components-angular/components/BroadcastingActivityComponent.html) [AdminLogin](../../reference-docs/openvidu-components-angular/components/AdminLoginComponent.html) [AdminDashboard](../../reference-docs/openvidu-components-angular/components/AdminDashboardComponent.html)

## Directives

Angular Components provides two types of directives: **Structural Directives** and **Attribute Directives**.

- **Structural Directives**: These directives manipulate the DOM by adding or removing elements from the view.

  They are distinguished by the asterisk (**\***) prefix and must be placed inside an HTML element within any [*Featured Component*](#featured-components).

  For example, the `*ovToolbar` directive allows you to add a custom toolbar to the videoconference, replacing the default one.

  You can check the list of available structural directives in the [Angular Components API Reference](../../reference-docs/openvidu-components-angular/modules/OpenViduComponentsDirectiveModule.html).

- **Attribute Directives**: Commonly known as **Components Inputs**, allow you to manipulate the appearance or behavior of an element.

  You can check the list of available structural directives in the [Angular Components API Reference](../../reference-docs/openvidu-components-angular/modules/OpenViduComponentsDirectiveModule.html).

## Events

Each component in **Angular Components** emits a set of events that you can listen to in your application to trigger specific actions.

These events are designed to provide you with the flexibility to customize your videoconferencing application according to your requirements.

You can check out all component events in the [Angular Components API Reference](../../reference-docs/openvidu-components-angular/).

## Applications

The [OpenVidu Components Demo App](../../tutorials/angular-components/openvidu-components-demo/) is a hands‑on example that shows how to build a complete videoconferencing UI with Angular Components. The demo walks you through running the app and inspecting how components, directives, events, and styles are composed and customized. It’s ideal for learning practical patterns such as custom toolbars, panel layouts and stream handling.

For a production‑grade reference, explore [**OpenVidu Meet**](../../../meet/). Built with the same Angular Components. It demonstrates real‑world concerns like theming, scalability, authentication, multi‑room management, and much more.

## References

- [Angular Components API Reference](../../reference-docs/openvidu-components-angular/)
