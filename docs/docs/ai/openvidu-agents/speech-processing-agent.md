# Speech Processing agent

The Speech Processing agent provides all the AI services related to transcribing audio speech to text and processing the results in various ways.

## List of provided AI services

- [**Live Captions**](../live-captions.md): transcribe the audio tracks of your Rooms in real time with great accuracy and display the results as live captions in your frontend.

## Enable the agent and configure AI services

### 1. SSH into an OpenVidu Node and go to configuration folder

Depending on your [OpenVidu deployment type](../../self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

    If you are using [OpenVidu Local (Development)](../../self-hosting/deployment-types.md#openvidu-local-development), simply navigate to the configuration folder of the project:

    ```bash
    # For OpenVidu Local COMMUNITY
    cd openvidu-local-deployment/community

    # For OpenVidu Local PRO
    cd openvidu-local-deployment/pro
    ```

=== "OpenVidu Single Node"

    If you are using [OpenVidu Single Node](../../self-hosting/deployment-types.md#openvidu-single-node), SSH into the only OpenVidu node and navigate to:

    ```bash
    cd /opt/openvidu/config
    ```

=== "OpenVidu Elastic"

    If you are using [OpenVidu Elastic](../../self-hosting/deployment-types.md#openvidu-elastic), SSH into the only Master Node and navigate to:

    ```bash
    cd /opt/openvidu/config/cluster/media_node
    ```

=== "OpenVidu High Availability"

    If you are using [OpenVidu High Availability](../../self-hosting/deployment-types.md#openvidu-high-availability), SSH into any of your Master Nodes (doesn't matter which one) and navigate to:

    ```bash
    cd /opt/openvidu/config/cluster/media_node
    ```

### 2. Modify file `agent-speech-processing.yaml`

Locate file `agent-speech-processing.yaml` in the [configuration folder](#1-ssh-into-an-openvidu-node-and-go-to-configuration-folder) of your OpenVidu node. Modify this file to enable the agent and configure the desired AI services.

#### Enable the agent

```yaml
enabled: true
```

#### Configure the desired AI services

You can set up the following AI services in this agent:

- **Live Captions**: see [Live Captions service](../live-captions.md#how-to-enable-live-captions-service-in-your-openvidu-deployment).

### 3. Restart OpenVidu

Depending on your [OpenVidu deployment type](../../self-hosting/deployment-types.md):

=== "OpenVidu Local (Development)"

    Run where `docker-compose.yaml` is located:

    ```bash
    docker compose restart
    ```

=== "OpenVidu Single Node"

    Run this command in your node:

    ```bash
    sudo systemctl restart openvidu
    ```

=== "OpenVidu Elastic"

    Run this command in your Master Node:

    ```bash
    sudo systemctl restart openvidu
    ```

=== "OpenVidu High Availability"

    Run this command in one of your Master Nodes:

    ```bash
    sudo systemctl restart openvidu
    ```

After restarting OpenVidu your agent will be up and running, ready to process new Rooms.

!!! warning

    If your agent container keeps restarting, there might be an error in your configuration. Check its logs to find out what is wrong.

## Configuration reference

Below is the full list of configuration properties available for the Speech Processing agent.

```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.3.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
# Docker image of the agent.
docker_image: docker.io/openvidu/agent-speech-processing:3.3.0

# Whether to run the agent or not.
enabled: false

live_captions:
  # How this agent will connect to Rooms [automatic, manual]
  # - automatic: the agent will automatically connect to new Rooms.
  # - manual: the agent will connect to new Rooms only when your application dictates it by using the Agent Dispatch API.
  processing: automatic

  # Which speech-to-text AI provider to use [aws, azure, google, openai, groq, deepgram, assemblyai, fal, clova, speechmatics, gladia, sarvam]
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
    # Prompt to guide the model's style or specify how to spell unfamiliar words. 224 tokens max.
    prompt:

  deepgram:
    # See https://console.deepgram.com/
    api_key:
    # See https://developers.deepgram.com/reference/speech-to-text-api/listen-streaming#request.query.model
    model:
    # See https://developers.deepgram.com/reference/speech-to-text-api/listen-streaming#request.query.language
    language:
    # Whether to enable automatic language detection. Defaults to false. See https://developers.deepgram.com/docs/language-detection
    detect_language: false
    # Whether to return interim (non-final) transcription results. Defaults to true. See https://developers.deepgram.com/docs/interim-results
    interim_results: true
    # Whether to apply smart formatting to numbers, dates, etc. Defaults to true. See https://developers.deepgram.com/docs/smart-format
    smart_format: true
    # When smart_format is used, ensures it does not wait for sequence to be complete before returning results. Defaults to true. See https://developers.deepgram.com/docs/smart-format#using-no-delay
    no_delay: true
    # Whether to add punctuations to the transcription. Defaults to true. Turn detector will work better with punctuations. See https://developers.deepgram.com/docs/punctuation
    punctuate: true
    # Whether to include filler words (um, uh, etc.) in transcription. Defaults to true. See https://developers.deepgram.com/docs/filler-words
    filler_words: true
    # Whether to filter profanity from the transcription. Defaults to false. See https://developers.deepgram.com/docs/profanity-filter
    profanity_filter: false
    # List of tuples containing keywords and their boost values for improved recognition. Each tuple should be (keyword: str, boost: float). Defaults to None. keywords does not work with Nova-3 models. Use keyterms instead.
    # keywords:
    #   - [OpenVidu, 1.5]
    #   - [WebRTC, 1]
    # List of key terms to improve recognition accuracy. Defaults to None. keyterms is supported by Nova-3 models.
    # Commented below is an example
    keyterms:
      # - "OpenVidu"
      # - "WebRTC"

  assemblyai:
    # API key for AssemblyAI. See https://www.assemblyai.com/dashboard/api-keys
    api_key:
    # Whether to return formatted final transcripts (proper punctuation, letter casing...). If enabled, formatted final transcripts are emitted shortly following an end-of-turn detection.
    format_turns: true

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
    # ISO 639-1 language code. All languages are global and can understand different dialects/accents. To see the list of all supported languages, see https://docs.speechmatics.com/introduction/supported-languages
    language:
    # Operating point to use for the transcription per required accuracy & complexity. To learn more, see https://docs.speechmatics.com/features/accuracy-language-packs#accuracy
    operating_point:
    # Partial transcripts allow you to receive preliminary transcriptions and update as more context is available until the higher-accuracy final transcript is returned. Partials are returned faster but without any post-processing such as formatting. See https://docs.speechmatics.com/features/realtime-latency#partial-transcripts
    enable_partials:
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

  sarvam:
    # API key for Sarvam. See https://dashboard.sarvam.ai/key-management
    api_key:
    # BCP-47 language code for supported Indian languages. See https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe#request.body.language_code.language_code
    language:
    # The Sarvam STT model to use. See https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe#request.body.model.model
    model:
```

