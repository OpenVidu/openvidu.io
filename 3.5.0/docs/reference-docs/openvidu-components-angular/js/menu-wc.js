'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">OpenVidu Components Angular Documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                                <li class="link">
                                    <a href="overview.html" data-type="chapter-link">
                                        <span class="icon ion-ios-keypad"></span>Overview
                                    </a>
                                </li>

                            <li class="link">
                                <a href="index.html" data-type="chapter-link">
                                    <span class="icon ion-ios-paper"></span>
                                        README
                                </a>
                            </li>
                        <li class="link">
                            <a href="license.html"  data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>LICENSE
                            </a>
                        </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>

                    </ul>
                </li>
                    <li class="chapter modules">
                        <a data-type="chapter-link" href="modules.html">
                            <div class="menu-toggler linked" data-bs-toggle="collapse" ${ isNormalMode ?
                                'data-bs-target="#modules-links"' : 'data-bs-target="#xs-modules-links"' }>
                                <span class="icon ion-ios-archive"></span>
                                <span class="link-name">Modules</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                        </a>
                        <ul class="links collapse " ${ isNormalMode ? 'id="modules-links"' : 'id="xs-modules-links"' }>
                            <li class="link">
                                <a href="modules/ApiDirectiveModule.html" data-type="entity-link" >ApiDirectiveModule</a>
                                <li class="chapter inner">
                                    <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ?
                                        'data-bs-target="#directives-links-module-ApiDirectiveModule-ac0edf63304bd0aacb86cb2f9ebeb42d4b3161143de731cf951e09f6cee52730f6629e9bdd791e671710a5c589a442788dc15d48a985a49115232b83e2c4d797"' : 'data-bs-target="#xs-directives-links-module-ApiDirectiveModule-ac0edf63304bd0aacb86cb2f9ebeb42d4b3161143de731cf951e09f6cee52730f6629e9bdd791e671710a5c589a442788dc15d48a985a49115232b83e2c4d797"' }>
                                        <span class="icon ion-md-code-working"></span>
                                        <span>Directives</span>
                                        <span class="icon ion-ios-arrow-down"></span>
                                    </div>
                                    <ul class="links collapse" ${ isNormalMode ? 'id="directives-links-module-ApiDirectiveModule-ac0edf63304bd0aacb86cb2f9ebeb42d4b3161143de731cf951e09f6cee52730f6629e9bdd791e671710a5c589a442788dc15d48a985a49115232b83e2c4d797"' :
                                        'id="xs-directives-links-module-ApiDirectiveModule-ac0edf63304bd0aacb86cb2f9ebeb42d4b3161143de731cf951e09f6cee52730f6629e9bdd791e671710a5c589a442788dc15d48a985a49115232b83e2c4d797"' }>
                                        <li class="link">
                                            <a href="directives/ActivitiesPanelBroadcastingActivityDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ActivitiesPanelBroadcastingActivityDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ActivitiesPanelRecordingActivityDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ActivitiesPanelRecordingActivityDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AdminDashboardRecordingsListDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AdminDashboardRecordingsListDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AdminDashboardTitleDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AdminDashboardTitleDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AdminLoginErrorDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AdminLoginErrorDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AdminLoginTitleDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AdminLoginTitleDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AudioEnabledDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AudioEnabledDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LangDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LangDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LangOptionsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LangOptionsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LivekitUrlDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LivekitUrlDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/MinimalDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >MinimalDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantNameDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantNameDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantPanelItemMuteButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantPanelItemMuteButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/PrejoinDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >PrejoinDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/RecordingStreamBaseUrlDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >RecordingStreamBaseUrlDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ShowDisconnectionDialogDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ShowDisconnectionDialogDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/StreamDisplayAudioDetectionDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >StreamDisplayAudioDetectionDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/StreamDisplayParticipantNameDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >StreamDisplayParticipantNameDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/StreamVideoControlsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >StreamVideoControlsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/TokenDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >TokenDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/TokenErrorDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >TokenErrorDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarActivitiesPanelButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarActivitiesPanelButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarAdditionalButtonsPossitionDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarAdditionalButtonsPossitionDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarBackgroundEffectsButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarBackgroundEffectsButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarBroadcastingButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarBroadcastingButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarCameraButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarCameraButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarChatPanelButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarChatPanelButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarDisplayLogoDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarDisplayLogoDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarDisplayRoomNameDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarDisplayRoomNameDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarFullscreenButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarFullscreenButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarLeaveButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarLeaveButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarMicrophoneButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarMicrophoneButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarParticipantsPanelButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarParticipantsPanelButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarRecordingButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarRecordingButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarScreenshareButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarScreenshareButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarSettingsButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarSettingsButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/VideoEnabledDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >VideoEnabledDirective</a>
                                        </li>
                                    </ul>
                                </li>
                            </li>
                            <li class="link">
                                <a href="modules/OpenViduComponentsDirectiveModule.html" data-type="entity-link" >OpenViduComponentsDirectiveModule</a>
                                <li class="chapter inner">
                                    <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ?
                                        'data-bs-target="#directives-links-module-OpenViduComponentsDirectiveModule-45cf5803e8551f3edebf966d99065c6f534a9c016029e83e83efb636495bb5dc5f9e4e0a7d8207ffcba263c40823d94920c9b523c39bbad96fe17a4946419959"' : 'data-bs-target="#xs-directives-links-module-OpenViduComponentsDirectiveModule-45cf5803e8551f3edebf966d99065c6f534a9c016029e83e83efb636495bb5dc5f9e4e0a7d8207ffcba263c40823d94920c9b523c39bbad96fe17a4946419959"' }>
                                        <span class="icon ion-md-code-working"></span>
                                        <span>Directives</span>
                                        <span class="icon ion-ios-arrow-down"></span>
                                    </div>
                                    <ul class="links collapse" ${ isNormalMode ? 'id="directives-links-module-OpenViduComponentsDirectiveModule-45cf5803e8551f3edebf966d99065c6f534a9c016029e83e83efb636495bb5dc5f9e4e0a7d8207ffcba263c40823d94920c9b523c39bbad96fe17a4946419959"' :
                                        'id="xs-directives-links-module-OpenViduComponentsDirectiveModule-45cf5803e8551f3edebf966d99065c6f534a9c016029e83e83efb636495bb5dc5f9e4e0a7d8207ffcba263c40823d94920c9b523c39bbad96fe17a4946419959"' }>
                                        <li class="link">
                                            <a href="directives/ActivitiesPanelDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ActivitiesPanelDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/AdditionalPanelsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AdditionalPanelsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ChatPanelDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ChatPanelDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LayoutAdditionalElementsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LayoutAdditionalElementsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LayoutDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LayoutDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/LeaveButtonDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LeaveButtonDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/PanelDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >PanelDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantPanelAfterLocalParticipantDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantPanelAfterLocalParticipantDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantPanelItemDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantPanelItemDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantPanelItemElementsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantPanelItemElementsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantPanelParticipantBadgeDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantPanelParticipantBadgeDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ParticipantsPanelDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ParticipantsPanelDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/PreJoinDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >PreJoinDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/StreamDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >StreamDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarAdditionalButtonsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarAdditionalButtonsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarAdditionalPanelButtonsDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarAdditionalPanelButtonsDirective</a>
                                        </li>
                                        <li class="link">
                                            <a href="directives/ToolbarDirective.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ToolbarDirective</a>
                                        </li>
                                    </ul>
                                </li>
                            </li>
                </ul>
                </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#components-links"' :
                            'data-bs-target="#xs-components-links"' }>
                            <span class="icon ion-md-cog"></span>
                            <span>Components</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="components-links"' : 'id="xs-components-links"' }>
                            <li class="link">
                                <a href="components/ActivitiesPanelComponent.html" data-type="entity-link" >ActivitiesPanelComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/AdminDashboardComponent.html" data-type="entity-link" >AdminDashboardComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/AdminLoginComponent.html" data-type="entity-link" >AdminLoginComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BroadcastingActivityComponent.html" data-type="entity-link" >BroadcastingActivityComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ChatPanelComponent.html" data-type="entity-link" >ChatPanelComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LayoutComponent.html" data-type="entity-link" >LayoutComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PanelComponent.html" data-type="entity-link" >PanelComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ParticipantPanelItemComponent.html" data-type="entity-link" >ParticipantPanelItemComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ParticipantsPanelComponent.html" data-type="entity-link" >ParticipantsPanelComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/RecordingActivityComponent.html" data-type="entity-link" >RecordingActivityComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/StreamComponent.html" data-type="entity-link" >StreamComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ThemeSelectorComponent.html" data-type="entity-link" >ThemeSelectorComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ToolbarComponent.html" data-type="entity-link" >ToolbarComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ToolbarPanelButtonsComponent.html" data-type="entity-link" >ToolbarPanelButtonsComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/VideoconferenceComponent.html" data-type="entity-link" >VideoconferenceComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/VideoPosterComponent.html" data-type="entity-link" >VideoPosterComponent</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#classes-links"' :
                            'data-bs-target="#xs-classes-links"' }>
                            <span class="icon ion-ios-paper"></span>
                            <span>Classes</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="classes-links"' : 'id="xs-classes-links"' }>
                            <li class="link">
                                <a href="classes/ParticipantModel.html" data-type="entity-link" >ParticipantModel</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#injectables-links"' :
                                'data-bs-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/BroadcastingService.html" data-type="entity-link" >BroadcastingService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/E2eeService.html" data-type="entity-link" >E2eeService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/OpenViduService.html" data-type="entity-link" >OpenViduService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/PanelService.html" data-type="entity-link" >PanelService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ParticipantService.html" data-type="entity-link" >ParticipantService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/RecordingService.html" data-type="entity-link" >RecordingService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/TemplateManagerService.html" data-type="entity-link" >TemplateManagerService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/TranslateService.html" data-type="entity-link" >TranslateService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interfaces-links"' :
                            'data-bs-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/ActivitiesPanelStatusEvent.html" data-type="entity-link" >ActivitiesPanelStatusEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/AdminConfig.html" data-type="entity-link" >AdminConfig</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BestDimensions.html" data-type="entity-link" >BestDimensions</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BroadcastingEvent.html" data-type="entity-link" >BroadcastingEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BroadcastingStartRequestedEvent.html" data-type="entity-link" >BroadcastingStartRequestedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BroadcastingStatusInfo.html" data-type="entity-link" >BroadcastingStatusInfo</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/BroadcastingStopRequestedEvent.html" data-type="entity-link" >BroadcastingStopRequestedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ChatPanelStatusEvent.html" data-type="entity-link" >ChatPanelStatusEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ConfigItem.html" data-type="entity-link" >ConfigItem</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/DefaultTemplates.html" data-type="entity-link" >DefaultTemplates</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ElementDimensions.html" data-type="entity-link" >ElementDimensions</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ElementPosition.html" data-type="entity-link" >ElementPosition</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ExtendedLayoutOptions.html" data-type="entity-link" >ExtendedLayoutOptions</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ExternalDirectives.html" data-type="entity-link" >ExternalDirectives</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/GeneralConfig.html" data-type="entity-link" >GeneralConfig</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LangOption.html" data-type="entity-link" >LangOption</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutArea.html" data-type="entity-link" >LayoutArea</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutAreas.html" data-type="entity-link" >LayoutAreas</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutBox.html" data-type="entity-link" >LayoutBox</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutCalculationResult.html" data-type="entity-link" >LayoutCalculationResult</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutRow.html" data-type="entity-link" >LayoutRow</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/LayoutTemplateConfiguration.html" data-type="entity-link" >LayoutTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/PanelStatusEvent.html" data-type="entity-link" >PanelStatusEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/PanelStatusInfo.html" data-type="entity-link" >PanelStatusInfo</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/PanelTemplateConfiguration.html" data-type="entity-link" >PanelTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantLeftEvent.html" data-type="entity-link" >ParticipantLeftEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantPanelItemTemplateConfiguration.html" data-type="entity-link" >ParticipantPanelItemTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantProperties.html" data-type="entity-link" >ParticipantProperties</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantsPanelStatusEvent.html" data-type="entity-link" >ParticipantsPanelStatusEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantsPanelTemplateConfiguration.html" data-type="entity-link" >ParticipantsPanelTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ParticipantTrackPublication.html" data-type="entity-link" >ParticipantTrackPublication</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingActivityConfig.html" data-type="entity-link" >RecordingActivityConfig</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingControls.html" data-type="entity-link" >RecordingControls</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingDeleteRequestedEvent.html" data-type="entity-link" >RecordingDeleteRequestedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingDownloadClickedEvent.html" data-type="entity-link" >RecordingDownloadClickedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingEvent.html" data-type="entity-link" >RecordingEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingInfo.html" data-type="entity-link" >RecordingInfo</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingPlayClickedEvent.html" data-type="entity-link" >RecordingPlayClickedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingStartRequestedEvent.html" data-type="entity-link" >RecordingStartRequestedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingStatusInfo.html" data-type="entity-link" >RecordingStatusInfo</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/RecordingStopRequestedEvent.html" data-type="entity-link" >RecordingStopRequestedEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SessionTemplateConfiguration.html" data-type="entity-link" >SessionTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SettingsPanelStatusEvent.html" data-type="entity-link" >SettingsPanelStatusEvent</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/StreamConfig.html" data-type="entity-link" >StreamConfig</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/TemplateConfiguration.html" data-type="entity-link" >TemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ToolbarConfig.html" data-type="entity-link" >ToolbarConfig</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ToolbarTemplateConfiguration.html" data-type="entity-link" >ToolbarTemplateConfiguration</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/VideoconferenceStateInfo.html" data-type="entity-link" >VideoconferenceStateInfo</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#pipes-links"' :
                                'data-bs-target="#xs-pipes-links"' }>
                                <span class="icon ion-md-add"></span>
                                <span>Pipes</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="pipes-links"' : 'id="xs-pipes-links"' }>
                                <li class="link">
                                    <a href="pipes/RemoteParticipantTracksPipe.html" data-type="entity-link" >RemoteParticipantTracksPipe</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#miscellaneous-links"'
                            : 'data-bs-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/enumerations.html" data-type="entity-link">Enums</a>
                            </li>
                            <li class="link">
                                <a href="miscellaneous/typealiases.html" data-type="entity-link">Type aliases</a>
                            </li>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});