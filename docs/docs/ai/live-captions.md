# :material-subtitles-outline:{ .ai-service-icon .middle } Live Captions

Transcribe the audio tracks of your Rooms in real time with great accuracy and display the results as live captions in your frontend.

## How to enable Live Captions service in your OpenVidu deployment

Live Captions service is provided by the **Speech Processing agent**:

[:octicons-arrow-right-24: Enable the Speech Processing agent](./openvidu-agents/speech-processing-agent.md#enable-the-agent-and-configure-ai-services){.ai-agent-link}

You configure the Live Captions service by setting up the following properties when [modifying file `agent-speech-processing.yaml`](./openvidu-agents/speech-processing-agent.md#2-modify-file-agent-speech-processingyaml):

```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.4.1/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
live_captions:
  # How this agent will connect to Rooms [automatic, manual]
  # - automatic: the agent will automatically connect to new Rooms.
  # - manual: the agent will connect to new Rooms only when your application dictates it by using the Agent Dispatch API.
  processing: automatic

  # Which speech-to-text AI provider to use [aws, azure, google, opeanai, groq, deepgram, assemblyai, fal, clova, speechmatics, gladia, sarvam]
  # The custom configuration for the selected provider must be set below
  provider: YOUR_PROVIDER

  # Custom configuration for the selected provider
  YOUR_PROVIDER: ...
```

!!! info "Choosing a provider"

    You must set up a specific `provider` from the list of [supported providers](#supported-ai-providers). Each provider has its own **custom configuration**. Some of them provide advanced features such as integrated profanity filters or translation. Check out the [configuration reference](#configuration-reference) below for more details.

## How to receive Live Captions in your frontend application

Live Captions are received in your frontend application using the [Text Stream API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/home/client/data/text-streams/#handling-incoming-streams){:target="\_blank"} of LiveKit client SDKs. You must specifically subscribe to the Room topic **`lk.transcription`** to automatically receive transcription events. For example, in JavaScript:

```javascript {#live-captions-js}
room.registerTextStreamHandler("lk.transcription", async (reader, participantInfo) => {
    const message = await reader.readAll();
    const isFinal = reader.info.attributes["lk.transcription_final"] === "true";
    const trackId = reader.info.attributes["lk.transcribed_track_id"];
    if (isFinal) {
      console.log(`Participant ${participantInfo.identity} and track ${trackId} said: ${message}`);
    } else {
      console.log(`Participant ${participantInfo.identity} and track ${trackId} is saying: ${message}`);
    }
  }
);
```

!!! info

    Refer to [LiveKit documentation :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/agents/voice-agent/transcriptions/#frontend-integration){:target="\_blank"} to see how to handle transcription events in other frontend platforms.

- From the `participantInfo` object of the text stream handler you can get the participant's `identity` that originated the transcription event.
- From the `reader.info.attributes` you can get the following properties:

    - `lk.transcription_final`: string that is `"true"` if the transcription is final or `"false"` if it is an interim. See [Final vs Interim transcriptions](#final-vs-interim-transcriptions) section for more details.
    - `lk.transcribed_track_id`: string with the ID of the audio track that was transcribed. This can be used to identify the exact source of the transcription in case the participant is publishing multiple audio tracks.

### Final vs Interim transcriptions

When receiving transcription events from [the **`lk.transcription`** text stream topic](#how-to-receive-live-captions-in-your-frontend-application), you may receive two types of transcriptions:

- **Interim transcription**: partial transcription that may be updated in future events with more accurate results. They are marked with `lk.transcription_final` set to string `"false"` in the event attributes.
- **Final transcriptions**: transcription for which the AI provider is confident enough to consider it completed for that portion of the speech. They are final and will not be updated with more interim transcriptions. They are marked with `lk.transcription_final` set to string `"true"` in the event attributes.

The difference between interim and final transcriptions is important: interim results allow you to display live captions in your frontend application **while the user is actively speaking**, instead of having to wait for the user to finish its sentence to receive a final transcription result.

!!! warning
    Not all AI providers support interim transcriptions (see the [Supported AI providers](#supported-ai-providers) table). All providers will actually generate at least one interim transcription before a final transcription, but the ones marked with :material-close: in the table will simply generate a single interim result just before each final result, that will completely match its content.

## Supported AI providers

Below is the list of cloud providers that can handle the Live Captions service.

| AI provider                                                                           | YAML property  | Service description                                                                                                                                                                                                                             | Interim results  |
| ------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| ![AWS](../../assets/images/ai-providers/aws.svg){.ai-provider-icon}                   | `aws`          | Uses [Amazon Transcribe :fontawesome-solid-external-link:{.external-link-icon}](https://aws.amazon.com/transcribe/){:target="\_blank"}                                                                                                          | :material-check: |
| ![Azure](../../assets/images/ai-providers/azure.svg){.ai-provider-icon}               | `azure`        | Uses [Azure Speech service :fontawesome-solid-external-link:{.external-link-icon}](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text){:target="\_blank"}                                                        | :material-check: |
| ![Azure OpenAI](../../assets/images/ai-providers/azure.svg){.ai-provider-icon}        | `azure_openai` | Uses [Azure OpenAI :fontawesome-solid-external-link:{.external-link-icon}](https://azure.microsoft.com/en-us/products/ai-services/openai-service/){:target="\_blank"}                                                                           | :material-close: |
| ![Google Cloud](../../assets/images/ai-providers/google.svg){.ai-provider-icon}       | `google`       | Uses [Google Cloud Speech-to-Text :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/speech-to-text){:target="\_blank"}                                                                                           | :material-close: |
| ![OpenAI](../../assets/images/ai-providers/openai.svg){.ai-provider-icon}             | `openai`       | Uses [OpenAI Speech to text :fontawesome-solid-external-link:{.external-link-icon}](https://platform.openai.com/docs/guides/speech-to-text){:target="\_blank"}                                                                                  | :material-close: |
| ![Groq](../../assets/images/ai-providers/groq.svg){.ai-provider-icon}                 | `groq`         | Uses [Groq Speech :fontawesome-solid-external-link:{.external-link-icon}](https://console.groq.com/docs/speech-to-text){:target="\_blank"}                                                                                                      | :material-close: |
| ![Deepgram](../../assets/images/ai-providers/deepgram.svg){.ai-provider-icon}         | `deepgram`     | Uses [Deepgram Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://deepgram.com/product/speech-to-text){:target="\_blank"}                                                                                       | :material-check: |
| ![AssemblyAI](../../assets/images/ai-providers/assemblyai.svg){.ai-provider-icon}     | `assemblyai`   | Uses [AssemblyAI Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://www.assemblyai.com/products/speech-to-text){:target="\_blank"}                                                                              | :material-check: |
| ![Fal](../../assets/images/ai-providers/fal.svg){.ai-provider-icon}                   | `fal`          | Uses [Fal Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.fal.ai/guides/convert-speech-to-text/){:target="\_blank"}                                                                                     | :material-close: |
| ![Clova](../../assets/images/ai-providers/clova.svg){.ai-provider-icon}               | `clova`        | Uses [Naver Clova Speech Recognition :fontawesome-solid-external-link:{.external-link-icon}](https://api.ncloud-docs.com/docs/en/ai-naver-clovaspeechrecognition-stt){:target="\_blank"}. Specialized in Japanese, Korean and Chinese languages | :material-close: |
| ![Speechmatics](../../assets/images/ai-providers/speechmatics.svg){.ai-provider-icon} | `speechmatics` | Uses [Speechmatics Real-Time API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.speechmatics.com/introduction/rt-guide){:target="\_blank"}                                                                                | :material-check: |
| ![Gladia](../../assets/images/ai-providers/gladia.svg){.ai-provider-icon}             | `gladia`       | Uses [Gladia Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://www.gladia.io/product/async-transcription){:target="\_blank"}                                                                                   | :material-check: |
| ![Sarvam](../../assets/images/ai-providers/sarvam.svg){.ai-provider-icon}             | `sarvam`       | Uses [Sarvam Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe){:target="\_blank"}. Optimized for Indian languages                                 | :material-close: |
| ![MistralAI](../../assets/images/ai-providers/mistralai.svg){.ai-provider-icon}       | `mistralai`    | Uses [Voxtral :fontawesome-solid-external-link:{.external-link-icon}](https://mistral.ai/news/voxtral){:target="\_blank"}                                                                                                                       | :material-close: |
| ![Cartesia](../../assets/images/ai-providers/cartesia.svg){.ai-provider-icon}         | `cartesia`     | Uses [Cartesia Ink-Whisper :fontawesome-solid-external-link:{.external-link-icon}](https://cartesia.ai/ink){:target="\_blank"}                                                                                                                  | :material-close: |
| ![Soniox](../../assets/images/ai-providers/soniox.svg){.ai-provider-icon}             | `soniox`       | Uses [Soniox Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://soniox.com/speech-to-text){:target="\_blank"}                                                                                                   | :material-check: |

This is the description of the columns in the table above:

- **YAML property**: set this value as the `provider` property in the [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) file to use that provider.
- **Interim results**: whether the provider supports interim (non-final) transcription results. See [Final vs Interim transcriptions](#final-vs-interim-transcriptions) for more details.

!!! info

    - You will need an account in the provider's platform to get the necessary **credentials**.
    - Each provider has its own **custom configuration**. Some of them provide advanced features such as integrated profanity filters or translation. Check out the [configuration reference](#configuration-reference) below for more details.

## Tutorial

Check out the [Live Captions tutorial](../tutorials/ai-services/openvidu-live-captions.md) for a complete example.

## Configuration reference

Below are the properties related to the Live Captions service available in the `agent-speech-processing.yaml` file.

```yaml
live_captions:
  # How this agent will connect to Rooms [automatic, manual]
  # - automatic: the agent will automatically connect to new Rooms.
  # - manual: the agent will connect to new Rooms only when your application dictates it by using the Agent Dispatch API.
  processing: automatic

  # Which speech-to-text AI provider to use [aws, azure, google, openai, azure_openai, groq, deepgram, assemblyai, fal, clova, speechmatics, gladia, sarvam, mistralai, cartesia, soniox]
  # The custom configuration for the selected provider must be set below
  provider:

  aws:
    # Credentials for AWS Transcribe. See https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html
    aws_access_key_id:
    aws_secret_access_key:
    aws_default_region:
    # See https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html
    language:
    # The name of the custom vocabulary you want to use.
    # See https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html
    vocabulary_name:
    # The name of the custom language model you want to use.
    # See https://docs.aws.amazon.com/transcribe/latest/dg/custom-language-models-using.html
    language_model_name:
    # Whether or not to enable partial result stabilization. Partial result stabilization can reduce latency in your output, but may impact accuracy.
    # See https://docs.aws.amazon.com/transcribe/latest/dg/streaming-partial-results.html#streaming-partial-result-stabilization
    enable_partial_results_stabilization:
    # Specify the level of stability to use when you enable partial results stabilization (enable_partial_results_stabilization: true). Valid values: high | medium | low
    # See https://docs.aws.amazon.com/transcribe/latest/dg/streaming-partial-results.html#streaming-partial-result-stabilization
    partial_results_stability:
    # The name of the custom vocabulary filter you want to use to mask or remove words.
    # See https://docs.aws.amazon.com/transcribe/latest/dg/vocabulary-filtering.html
    vocab_filter_name:
    # The method used to filter the vocabulary. Valid values: mask | remove | tag
    # See https://docs.aws.amazon.com/transcribe/latest/dg/vocabulary-filtering.html
    vocab_filter_method:

  azure:
    # Credentials for Azure Speech Service.
    # One of these combinations must be set:
    #  - speech_host
    #  - speech_key + speech_region
    #  - speech_auth_token + speech_region
    # See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=macos%2Cterminal&pivots=programming-language-python#prerequisites
    speech_host:
    speech_key:
    speech_auth_token:
    speech_region:
    # Azure handles multiple languages and can auto-detect the language used. It requires the candidate set to be set. E.g. ["en-US", "es-ES"]
    # See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt#supported-languages
    language:
    # Removes profanity (swearing), or replaces letters of profane words with stars. Valid values: Masked | Removed | Raw
    # See https://learn.microsoft.com/en-us/azure/ai-services/translator/profanity-filtering
    profanity:
    # List of words or phrases to boost recognition accuracy. Azure will give higher priority to these phrases during recognition.
    phrase_list:
    # Controls punctuation behavior. If True, enables explicit punctuation mode where punctuation marks are added explicitly. If False (default), uses Azure's default punctuation behavior.
    explicit_punctuation: 

  azure_openai:
    # Credentials for Azure OpenAI APIs. See https://learn.microsoft.com/en-us/azure/api-management/api-management-authenticate-authorize-azure-openai
    # Azure OpenAI API key
    azure_api_key:
    # Azure Active Directory token
    azure_ad_token:
    # Azure OpenAI endpoint in the following format: https://{your-resource-name}.openai.azure.com. Mandatory value.
    azure_endpoint:
    # Name of your model deployment. If given with `azure_endpoint`, sets the base client URL to include `/deployments/{azure_deployment}`.
    azure_deployment:
    # OpenAI REST API version used for the request. Mandatory value.
    api_version:
    # OpenAI organization ID.
    organization:
    # OpenAI project ID.
    project:
    # The language code to use for transcription (e.g., "en" for English).
    language:
    # Whether to automatically detect the language.
    detect_language:
    # ID of the model to use for speech-to-text.
    model:
    # Initial prompt to guide the transcription.
    prompt:

  google:
    # Credentials for Google Cloud. This is the content of a Google Cloud credential JSON file.
    # Below is a dummy example for a credential type of "Service Account" (https://cloud.google.com/iam/docs/service-account-creds#key-types)
    credentials_info: |
      {
        "type": "service_account",
        "project_id": "my-project",
        "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n-----END PRIVATE KEY-----\n",
        "client_email": "my-email@my-project.iam.gserviceaccount.com",
        "client_id": "xxxxxxxxxxxxxxxxxxxxx",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-email%40my-project.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
      }
    # Which model to use for recognition. If not set, uses the default model for the selected language.
    # See https://cloud.google.com/speech-to-text/docs/transcription-model
    model:
    # The location to use for recognition. Default is "us-central1". Latency will be best if the location is close to your users.
    # Check supported languages and locations at https://cloud.google.com/speech-to-text/v2/docs/speech-to-text-supported-languages
    location:
    # List of language codes to recognize. Default is ["en-US"].
    # See https://cloud.google.com/speech-to-text/v2/docs/speech-to-text-supported-languages
    languages:
    # Whether to detect the language of the audio. Default is true.
    detect_language:
    # If 'true', adds punctuation to recognition result hypotheses. This feature is only available in select languages. Setting this
    # for requests in other languages has no effect at all. The default 'false' value does not add punctuation to result hypotheses.
    # See https://cloud.google.com/speech-to-text/docs/automatic-punctuation
    punctuate:
    # The spoken punctuation behavior for the call. If not set, uses default behavior based on model of choice.
    # e.g. command_and_search will enable spoken punctuation by default. If 'true', replaces spoken punctuation
    # with the corresponding symbols in the request. For example, "how are you question mark" becomes "how are you?".
    # See https://cloud.google.com/speech-to-text/docs/spoken-punctuation for support. If 'false', spoken punctuation is not replaced.
    spoken_punctuation:
    # Whether to return interim (non-final) transcription results. Defaults to true.
    interim_results:

  openai:
    # API key for OpenAI. See https://platform.openai.com/api-keys
    api_key:
    # The OpenAI model to use for transcription. See https://platform.openai.com/docs/guides/speech-to-text
    model:
    # The language of the input audio. Supplying the input language in ISO-639-1 format
    # (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) will improve accuracy and latency.
    language:
    # Whether to automatically detect the language.
    detect_language:
    # Optional text prompt to guide the transcription. Only supported for whisper-1.
    prompt:

  groq:
    # API key for Groq. See https://console.groq.com/keys
    api_key:
    # See https://console.groq.com/docs/speech-to-text
    model:
    # The language of the input audio. Supplying the input language in ISO-639-1 format
    # (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) will improve accuracy and latency.
    language:
    # Whether to automatically detect the language.
    detect_language:
    # Prompt to guide the model's style or specify how to spell unfamiliar words. 224 tokens max.
    prompt:
    # Base URL for the Groq API. By default "https://api.groq.com/openai/v1"
    base_url:

  deepgram:
    # See https://console.deepgram.com/
    api_key:
    # See https://developers.deepgram.com/reference/speech-to-text-api/listen-streaming#request.query.model
    model:
    # See https://developers.deepgram.com/reference/speech-to-text-api/listen-streaming#request.query.language
    language:
    # Whether to enable automatic language detection. See https://developers.deepgram.com/docs/language-detection
    detect_language: false
    # Whether to return interim (non-final) transcription results. See https://developers.deepgram.com/docs/interim-results
    interim_results: true
    # Whether to apply smart formatting to numbers, dates, etc. See https://developers.deepgram.com/docs/smart-format
    smart_format: false
    # When smart_format is used, ensures it does not wait for sequence to be complete before returning results. See https://developers.deepgram.com/docs/smart-format#using-no-delay
    no_delay: true
    # Whether to add punctuations to the transcription. Turn detector will work better with punctuations. See https://developers.deepgram.com/docs/punctuation
    punctuate: true
    # Whether to include filler words (um, uh, etc.) in transcription. See https://developers.deepgram.com/docs/filler-words
    filler_words: true
    # Whether to filter profanity from the transcription. See https://developers.deepgram.com/docs/profanity-filter
    profanity_filter: false
    # Whether to transcribe numbers as numerals. See https://developers.deepgram.com/docs/numerals
    numerals: false
    # List of tuples containing keywords and their boost values for improved recognition. Each tuple should be (keyword: str, boost: float). keywords does not work with Nova-3 models. Use keyterms instead.
    # keywords:
    #   - [OpenVidu, 1.5]
    #   - [WebRTC, 1]
    # List of key terms to improve recognition accuracy. keyterms is supported by Nova-3 models.
    # Commented below is an example
    keyterms:
      # - "OpenVidu"
      # - "WebRTC"

  assemblyai:
    # API key for AssemblyAI. See https://www.assemblyai.com/dashboard/api-keys
    api_key:
    # The confidence threshold (0.0 to 1.0) to use when determining if the end of a turn has been reached.
    end_of_turn_confidence_threshold:
    # The minimum amount of silence in milliseconds required to detect end of turn when confident.
    min_end_of_turn_silence_when_confident:
    # The maximum amount of silence in milliseconds allowed in a turn before end of turn is triggered.
    max_turn_silence:
    # Whether to return formatted final transcripts (proper punctuation, letter casing...). If enabled, formatted final transcripts are emitted shortly following an end-of-turn detection.
    format_turns: true
    # List of keyterms to improve recognition accuracy for specific words and phrases.
    keyterms_prompt:
      # - "OpenVidu"
      # - "WebRTC"

  fal:
    # API key for fal. See https://fal.ai/dashboard/keys
    api_key:
    # See https://fal.ai/models/fal-ai/wizper/api#schema
    language:

  clova:
    # Secret key issued when registering the app
    api_key:
    # API Gateway's unique invoke URL created in CLOVA Speech Domain.
    # See https://guide.ncloud-docs.com/docs/en/clovaspeech-domain#create-domain
    invoke_url:
    # See https://api.ncloud-docs.com/docs/en/ai-application-service-clovaspeech-longsentence
    language:
    # Value between 0 and 1 indicating the threshold for the confidence score of the transcribed text. Default is 0.5.
    # If the confidence score is lower than the threshold, the transcription event is not sent to the client.
    # For a definition of the confidence score see https://api.ncloud-docs.com/docs/en/ai-application-service-clovaspeech-grpc
    threshold:

  speechmatics:
    # API key for Speechmatics. See https://portal.speechmatics.com/manage-access/
    api_key:
    # ISO 639-1 language code. All languages are global and can understand different dialects/accents. To see the list of all supported languages, see https://docs.speechmatics.com/speech-to-text/languages#transcription-languages
    language:
    # Operating point to use for the transcription per required accuracy & complexity. To learn more, see https://docs.speechmatics.com/speech-to-text/languages#operating-points
    operating_point:
    # Partial transcripts allow you to receive preliminary transcriptions and update as more context is available until the higher-accuracy final transcript is returned. Partials are returned faster but without any post-processing such as formatting. See https://docs.speechmatics.com/speech-to-text/realtime/output#partial-transcripts
    enable_partials:
    # Enable speaker diarization. When enabled, the STT engine will determine and attribute words to unique speakers. The speaker_sensitivity parameter can be used to adjust the sensitivity of diarization
    enable_diarization:
    # RFC-5646 language code to make spelling rules more consistent in the transcription output. See https://docs.speechmatics.com/features/word-tagging#output-locale
    output_locale:
    # The delay in seconds between the end of a spoken word and returning the final transcript results. See https://docs.speechmatics.com/features/realtime-latency#configuration-example
    max_delay:
    # See https://docs.speechmatics.com/features/realtime-latency#configuration-example
    max_delay_mode:
    # Configuration for speaker diarization. See https://docs.speechmatics.com/features/diarization
    speaker_diarization_config:
      # See https://docs.speechmatics.com/features/diarization#max-speakers
      max_speakers:
      # See https://docs.speechmatics.com/features/diarization#speaker-sensitivity
      speaker_sensitivity:
      # See https://docs.speechmatics.com/features/diarization#prefer-current-speaker
      prefer_current_speaker:
    # Permitted punctuation marks for advanced punctuation. See https://docs.speechmatics.com/features/punctuation-settings
    # Commented is an example of punctuation settings
    punctuation_overrides:
      # permitted_marks: [ ".", "," ]
      # sensitivity: 0.4
    # See https://docs.speechmatics.com/features/custom-dictionary
    # Commented below is an example of a custom dictionary
    additional_vocab:
      # - content: financial crisis
      # - content: gnocchi
      #   sounds_like:
      #     - nyohki
      #     - nokey
      #     - nochi
      # - content: CEO
      #   sounds_like:
      #     - C.E.O.

  gladia:
    # API key for Gladia. See https://app.gladia.io/account
    api_key:
    # Whether to return interim (non-final) transcription results. Defaults to True
    interim_results:
    # List of language codes to use for recognition. Defaults to None (auto-detect). See https://docs.gladia.io/chapters/limits-and-specifications/languages
    languages:
    # Whether to allow switching between languages during recognition. Defaults to True
    code_switching:
    # https://docs.gladia.io/api-reference/v2/live/init#body-pre-processing-audio-enhancer
    pre_processing_audio_enhancer:
    # https://docs.gladia.io/api-reference/v2/live/init#body-pre-processing-speech-threshold
    pre_processing_speech_threshold:

  sarvam:
    # API key for Sarvam. See https://dashboard.sarvam.ai/key-management
    api_key:
    # BCP-47 language code for supported Indian languages. See https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe#request.body.language_code.language_code
    language:
    # The Sarvam STT model to use. See https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe#request.body.model.model
    model:

  mistralai:
    # API key for Mistral AI. See https://console.mistral.ai/api-keys
    api_key:
    # Name of the Voxtral STT model to use. Default to voxtral-mini-latest. See https://docs.mistral.ai/capabilities/audio/
    model:
    # The language code to use for transcription (e.g., "en" for English)
    language:

  cartesia:
    # API key for Cartesia. See https://play.cartesia.ai/keys
    api_key:
    # The Cartesia STT model to use
    model:
    # The language code to use for transcription (e.g., "en" for English)
    language:

  soniox:
    # API key for Soniox. See https://console.soniox.com/
    api_key:
    # Set language hints when possible to significantly improve accuracy. See: https://soniox.com/docs/stt/concepts/language-hints
    language_hints:
      # - "en"
      # - "es"
    # Set context to improve recognition of difficult and rare words. Context is a string and can include words, phrases, sentences, or summaries (limit: 10K chars). See https://soniox.com/docs/stt/concepts/context
    context:
```
