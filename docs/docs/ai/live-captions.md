# :material-subtitles-outline:{ .ai-service-icon .middle } Live Captions

Transcribe the audio tracks of your Rooms in real time with great accuracy and display the results as live captions in your frontend.

## How to enable Live Captions service in your OpenVidu deployment

Live Captions service is provided by the **Speech Processing agent**:

[:octicons-arrow-right-24: Enable the Speech Processing agent](./openvidu-agents/speech-processing-agent.md#enable-the-agent-and-configure-ai-services){.ai-agent-link}

You configure the Live Captions service by setting up the following properties when [modifying file `agent-speech-processing.yaml`](./openvidu-agents/speech-processing-agent.md#2-modify-file-agent-speech-processingyaml):

```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
live_captions:
  # How this agent will connect to Rooms [manual, automatic]
  # - manual: the agent will connect to new Rooms only when your application dictates it by using the Agent Dispatch API.
  # - automatic: the agent will automatically connect to new Rooms.
  processing: manual

  # Which speech-to-text AI provider to use [aws, azure, google, openai, azure_openai, groq, deepgram, assemblyai, fal, clova, speechmatics, gladia, sarvam, mistralai, cartesia, soniox, nvidia, elevenlabs, simplismart, vosk, sherpa]
  # The custom configuration for the selected provider must be set below
  provider: YOUR_PROVIDER

  # Custom configuration for the selected provider
  YOUR_PROVIDER: ...
```

!!! info "Choosing a provider"

    You must set up a specific `provider` from the list of [supported providers](#supported-ai-providers). Each provider has its own **custom configuration**. Some of them provide advanced features such as integrated profanity filters or translation. Check out the [configuration reference](#configuration-reference) below for more details.

### Automatic vs Manual processing

You can decide when the Speech Processing agent will connect to Rooms to provide Live Captions service:

- **Automatic processing**: the agent will automatically connect to new Rooms as soon as they are created. All your Rooms will be transcribed without any additional action from your application.
  Set YAML property `live_captions.processing` to `automatic` in file [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment).
- **Manual processing**: the agent will connect to new Rooms only when your application dictates it with [explicit agent dispatch](./openvidu-agents/agent-dispatch.md#explicit-agent-dispatch). This allows you to toggle Live Captions service on demand for specific Rooms.
  Set YAML property `live_captions.processing` to `manual` in file [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment).

Learn more about [Automatic vs Manual processing](./openvidu-agents/agent-dispatch.md).

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

OpenVidu Live Captions service supports multiple AI providers for speech-to-text transcription. They are grouped into two categories:

- [Cloud providers](#cloud-providers): third-party providers that offer their services through cloud APIs. They provide easy setup, scalability and a wide range of features, but may have higher latency and costs depending on usage.
- [Local providers](#local-providers): these providers can be deployed on-premises along with your OpenVidu deployment. They offer lower latency, data privacy and third-party cost control, but they will require generous infrastructure resources (CPU and memory).

### Cloud providers

Third-party AI providers that offer their services through cloud APIs. They provide easy setup, scalability and a wide range of features, but may have higher latency and costs depending on usage.

The table below lists the cloud providers that can handle the Live Captions service. The columns in the table are described as follows:

- **YAML `provider` property**: the value to set in `live_captions.provider` property of [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) file to use that provider.
- **YAML `docker_image` property**: the value to set in `docker_image` property of [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) file to use that provider.
- **Interim results**: whether the provider supports interim (non-final) transcription results. See [Final vs Interim transcriptions](#final-vs-interim-transcriptions) for more details.

| AI provider   | YAML `provider` property :material-information-outline:{ title="Value to set in live_captions.provider property of file agent-speech-processing.yaml" } | YAML `docker_image` property :material-information-outline:{ title="Value to set in docker_image property of file agent-speech-processing.yaml" } | Service description | Interim results :material-information-outline:{ title="Whether the provider supports interim (non-final) transcription results" } |
| ------------------------------------------------------------------------------------- | -------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| ![AWS](../../assets/images/ai-providers/aws.svg){.ai-provider-icon}                   | `aws`          | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Amazon Transcribe :fontawesome-solid-external-link:{.external-link-icon}](https://aws.amazon.com/transcribe/){:target="\_blank"}                                                                                                          | :material-check: |
| ![Azure](../../assets/images/ai-providers/azure.svg){.ai-provider-icon}               | `azure`        | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Azure Speech service :fontawesome-solid-external-link:{.external-link-icon}](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text){:target="\_blank"}                                                        | :material-check: |
| ![Azure OpenAI](../../assets/images/ai-providers/azure.svg){.ai-provider-icon}        | `azure_openai` | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Azure OpenAI :fontawesome-solid-external-link:{.external-link-icon}](https://azure.microsoft.com/en-us/products/ai-services/openai-service/){:target="\_blank"}                                                                           | :material-close: |
| ![Google Cloud](../../assets/images/ai-providers/google.svg){.ai-provider-icon}       | `google`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Google Cloud Speech-to-Text :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/speech-to-text){:target="\_blank"}                                                                                           | :material-close: |
| ![OpenAI](../../assets/images/ai-providers/openai.svg){.ai-provider-icon}             | `openai`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [OpenAI Speech to text :fontawesome-solid-external-link:{.external-link-icon}](https://platform.openai.com/docs/guides/speech-to-text){:target="\_blank"}                                                                                  | :material-close: |
| ![Groq](../../assets/images/ai-providers/groq.svg){.ai-provider-icon}                 | `groq`         | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Groq Speech :fontawesome-solid-external-link:{.external-link-icon}](https://console.groq.com/docs/speech-to-text){:target="\_blank"}                                                                                                      | :material-close: |
| ![Deepgram](../../assets/images/ai-providers/deepgram.svg){.ai-provider-icon}         | `deepgram`     | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Deepgram Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://deepgram.com/product/speech-to-text){:target="\_blank"}                                                                                       | :material-check: |
| ![AssemblyAI](../../assets/images/ai-providers/assemblyai.svg){.ai-provider-icon}     | `assemblyai`   | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [AssemblyAI Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://www.assemblyai.com/products/speech-to-text){:target="\_blank"}                                                                              | :material-check: |
| ![Fal](../../assets/images/ai-providers/fal.svg){.ai-provider-icon}                   | `fal`          | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Fal Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.fal.ai/guides/convert-speech-to-text/){:target="\_blank"}                                                                                     | :material-close: |
| ![Clova](../../assets/images/ai-providers/clova.svg){.ai-provider-icon}               | `clova`        | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Naver Clova Speech Recognition :fontawesome-solid-external-link:{.external-link-icon}](https://api.ncloud-docs.com/docs/en/ai-naver-clovaspeechrecognition-stt){:target="\_blank"}. Specialized in Japanese, Korean and Chinese languages | :material-close: |
| ![Speechmatics](../../assets/images/ai-providers/speechmatics.svg){.ai-provider-icon} | `speechmatics` | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Speechmatics Real-Time API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.speechmatics.com/introduction/rt-guide){:target="\_blank"}                                                                                | :material-check: |
| ![Gladia](../../assets/images/ai-providers/gladia.svg){.ai-provider-icon}             | `gladia`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Gladia Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://www.gladia.io/product/async-transcription){:target="\_blank"}                                                                                   | :material-check: |
| ![Sarvam](../../assets/images/ai-providers/sarvam.svg){.ai-provider-icon}             | `sarvam`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Sarvam Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe){:target="\_blank"}. Optimized for Indian languages                                 | :material-close: |
| ![MistralAI](../../assets/images/ai-providers/mistralai.svg){.ai-provider-icon}       | `mistralai`    | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Voxtral :fontawesome-solid-external-link:{.external-link-icon}](https://mistral.ai/news/voxtral){:target="\_blank"}                                                                                                                       | :material-close: |
| ![Cartesia](../../assets/images/ai-providers/cartesia.svg){.ai-provider-icon}         | `cartesia`     | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Cartesia Ink-Whisper :fontawesome-solid-external-link:{.external-link-icon}](https://cartesia.ai/ink){:target="\_blank"}                                                                                                                  | :material-close: |
| ![Soniox](../../assets/images/ai-providers/soniox.svg){.ai-provider-icon}             | `soniox`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Soniox Speech-to-Text API :fontawesome-solid-external-link:{.external-link-icon}](https://soniox.com/speech-to-text){:target="\_blank"}                                                                                                   | :material-check: |
| ![Nvidia](../../assets/images/ai-providers/nvidia.svg){.ai-provider-icon}             | `nvidia`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [NVIDIA Riva ASR :fontawesome-solid-external-link:{.external-link-icon}](https://docs.nvidia.com/deeplearning/riva/user-guide/docs/asr/asr-overview.html){:target="\_blank"}  | :material-check: |
| ![Spitch](../../assets/images/ai-providers/spitch.svg){.ai-provider-icon}             | `spitch`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Spitch Speech To Text API :fontawesome-solid-external-link:{.external-link-icon}](https://docs.spitch.app/api/speech/stt){:target="\_blank"}. Specialized in African languages  | :material-close: |
| ![ElevenLabs](../../assets/images/ai-providers/elevenlabs.svg){.ai-provider-icon}             | `elevenlabs`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [ElevenLabs Speech To Text API :fontawesome-solid-external-link:{.external-link-icon}](https://elevenlabs.io/speech-to-text){:target="\_blank"} | :material-close: |
| ![Simplismart](../../assets/images/ai-providers/simplismart.svg){.ai-provider-icon}             | `simplismart`       | `docker.io/openvidu/agent-speech-processing-cloud:3.5.0` | Uses [Simplismart :fontawesome-solid-external-link:{.external-link-icon}](https://simplismart.ai/){:target="\_blank"}  | :material-close: |

!!! info

    - You will need an account in the provider's platform to get the necessary **credentials**.
    - Each provider has its own **custom configuration**. Some of them provide advanced features such as integrated profanity filters or translation. Check out the [configuration reference](#configuration-reference) below for more details.

### Local providers

These AI providers can be deployed on-premises along with your OpenVidu deployment. They offer lower latency, data privacy and third-party cost control, but they will require generous infrastructure resources (CPU and memory).

#### Vosk

[Vosk :fontawesome-solid-external-link:{.external-link-icon}](https://alphacephei.com/vosk/){:target="_blank"} is an open-source offline speech recognition toolkit. It supports multiple languages and can run on modest hardware. OpenVidu offers a dedicated Docker image that includes Vosk with some small-sized models for multiple languages, but you can also build your own images with larger models.

##### Enabling Vosk provider

To enable Live Captions service using Vosk:

1. In file [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) set properties `docker_image` and `live_captions.provider` as follows:

    ```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
    docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.5.0
    live_captions:
      provider: vosk
    ```

2. Configure additional Vosk settings under `live_captions.vosk`. Especially important is property `model` to select the desired language model.

    ```yaml
    live_captions:
      vosk:
        # Vosk language model. This provider requires docker_image "docker.io/openvidu/agent-speech-processing-vosk"
        # Below is the list of pre-installed models in the container (available at https://alphacephei.com/vosk/models):
        # - vosk-model-en-us-0.22-lgraph (English US)
        # - vosk-model-small-cn-0.22 (Chinese)
        # - vosk-model-small-de-0.15 (German)
        # - vosk-model-small-en-in-0.4 (English India)
        # - vosk-model-small-es-0.42 (Spanish)
        # - vosk-model-small-fr-0.22 (French)
        # - vosk-model-small-hi-0.22 (Hindi)
        # - vosk-model-small-it-0.22 (Italian)
        # - vosk-model-small-ja-0.22 (Japanese)
        # - vosk-model-small-nl-0.22 (Dutch)
        # - vosk-model-small-pt-0.3 (Portuguese)
        # - vosk-model-small-ru-0.22 (Russian)
        model: vosk-model-en-us-0.22-lgraph
        # Language code for reference. It has no effect other than observability purposes.
        # If a pre-installed "model" is declared, this will be set automatically if empty.
        language:
        # Audio sample rate in Hz. Default is 16000.
        sample_rate:
        # Whether to return interim/partial results during recognition. Default is true.
        partial_results:
    ```

##### Build a custom Vosk image

The default Docker image `docker.io/openvidu/agent-speech-processing-vosk:3.5.0` comes with small-sized models for multiple languages pre-installed. You can build your own Docker image with exactly the models you need ([https://alphacephei.com/vosk/models :fontawesome-solid-external-link:{.external-link-icon}](https://alphacephei.com/vosk/models){:target="_blank"}).

1. Create this two-line Dockerfile:

    ```Dockerfile
    FROM docker.io/openvidu/agent-speech-processing-vosk-base:3.5.0
    COPY --chown=appuser:appuser vosk-models /app/vosk-models
    ```

2. Download and unzip the [desired Vosk models :fontawesome-solid-external-link:{.external-link-icon}](https://alphacephei.com/vosk/models){:target="_blank"} into a local folder `vosk-models`. The folder structure should be like this:

    ```
    ├── Dockerfile
    └── vosk-models
        ├── vosk-model-small-en-us-0.15
        │   ├── am
        │   ├── conf
        │   ├── graph
        │   └── ...
        ├── vosk-model-small-cn-0.22
        │   ├── am
        │   ├── conf
        │   ├── graph
        │   └── ...
        │   
        └── ...
    ```

3. Build the Docker image and push it to your remote Docker repository:

    ```bash
    docker build -f Dockerfile -t <YOUR_DOCKERHUB_ACCOUNT>/agent-speech-processing-vosk:CUSTOM_TAG .
    ```

4. Update your OpenVidu deployment by setting property `docker_image` in file 
[`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment):

    ```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
    docker_image: <YOUR_DOCKERHUB_ACCOUNT>/agent-speech-processing-vosk:CUSTOM_TAG
    live_captions:
      provider: vosk
      vosk:
        model: vosk-model-en-us-0.22 # Or any other model you added in your custom image
    ```

#### Sherpa

[sherpa-onnx :fontawesome-solid-external-link:{.external-link-icon}](https://k2-fsa.github.io/sherpa/onnx/index.html){:target="_blank"} is an offline, cutting-edge speech recognition toolkit that offers competitive accuracy and performance.

!!! info
    
    Sherpa live captions provider is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag" style="font-size: 12px; vertical-align: top;">PRO</span>**. Before deploying, you need to [create an OpenVidu account](/account/){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

##### Sherpa vs Vosk

Sherpa offers multiple advantages compared to Vosk:

- It offers a wider, more modern, more maintained selection of pre-trained language models. You can fine-tune the sherpa agent with the exact model that best fit your use case.
- It offers superior performance, allowing for more concurrent transcriptions with the same hardware resources.
- It offers [GPU acceleration support](#gpu-acceleration-for-sherpa-provider). For nodes with NVIDIA GPUs, it will further improve performance and reduce latency.

##### Enabling Sherpa provider

To enable Live Captions service using Sherpa:

1. In file [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) set properties `docker_image` and `live_captions.provider` as follows:

    ```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
    docker_image: docker.io/openvidu/agent-speech-processing-sherpa:3.5.0
    live_captions:
      provider: sherpa
    ```

2. Configure additional Sherpa settings under `live_captions.sherpa`. Especially important is property `model` to select the desired language model.

    ```yaml
    live_captions:
      sherpa:
        # sherpa streaming model. This provider requires docker_image "docker.io/openvidu/agent-speech-processing-sherpa"
        # Below is the list of pre-installed models in the container (available at https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models):
        # - sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06 (English)
        # - sherpa-onnx-streaming-zipformer-es-kroko-2025-08-06 (Spanish)
        # - sherpa-onnx-streaming-zipformer-de-kroko-2025-08-06 (German)
        # - sherpa-onnx-streaming-zipformer-fr-kroko-2025-08-06 (French)
        # - sherpa-onnx-streaming-zipformer-ar_en_id_ja_ru_th_vi_zh-2025-02-10 (Multilingual: Arabic, English, Indonesian, Japanese, Russian, Thai, Vietnamese, Chinese)
        model: sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06
        # Language code for reference. Auto-detected from model name if not set.
        language:
        # Runtime provider for sherpa-onnx. Supported values: "cpu" or "cuda". Default is "cpu".
        # Learn about GPU acceleration at https://openvidu.io/docs/ai/live-captions/#gpu-acceleration-for-sherpa-provider
        provider:
        # Audio sample rate in Hz. Default is 16000.
        sample_rate:
        # Whether to return interim/partial results during recognition. Default is true.
        partial_results:
        # Number of threads for ONNX Runtime. Default is 2.
        num_threads:
        # Recognizer type ("transducer", "paraformer", "zipformer_ctc", "nemo_ctc", "t_one_ctc"). Auto-detected from model name if not set.
        recognizer_type:
        # Decoding method ("greedy_search", "modified_beam_search"). Default is "greedy_search".
        decoding_method:
        # Whether to override sherpa's built-in Voice Activity Detection (VAD) with Silero's VAD. Default is false.
        use_silero_vad: false
    ```

##### Build a custom Sherpa image

The default Docker image `docker.io/openvidu/agent-speech-processing-sherpa:3.5.0` comes with small-sized models for multiple languages pre-installed. You can build your own Docker image with exactly the models you need ([sherpa-onnx ASR models :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models){:target="_blank"}).

1. Create this two-line Dockerfile:

    ```Dockerfile
    FROM docker.io/openvidu/agent-speech-processing-sherpa-base:3.5.0
    COPY --chown=appuser:appuser sherpa-models /app/sherpa-models
    ```

    !!! info

        To build a custom Sherpa image [with GPU acceleration](#gpu-support-for-sherpa-provider), just change the FROM line to:
        
          - `FROM docker.io/openvidu/agent-speech-processing-sherpa-cuda11-base:3.5.0` if your GPU is compatible only with CUDA 11.
          - `FROM docker.io/openvidu/agent-speech-processing-sherpa-cuda12-base:3.5.0` if your GPU is compatible with CUDA 12 or higher.

2. Download and unzip the [desired sherpa-onnx streaming models :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models){:target="_blank"} into a local folder `sherpa-onnx-streaming-models`. The folder structure should be like this:

    ```
    ├── Dockerfile
    └── sherpa-onnx-streaming-models
        ├── sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06
        │   ├── encoder.onnx
        │   ├── decoder.onnx
        │   ├── joiner.onnx
        │   └── ...
        ├── sherpa-onnx-streaming-zipformer-de-kroko-2025-08-06
        │   ├── encoder.onnx
        │   ├── decoder.onnx
        │   ├── joiner.onnx
        │   └── ...
        │   
        └── ...
    ```

    !!! warning

        Look for the particle **`-streaming-`** in the name of the language models, as only those are able to produce real-time transcriptions.

3. Build the Docker image and push it to your remote Docker repository:

    ```bash
    docker build -f Dockerfile -t <YOUR_DOCKERHUB_ACCOUNT>/agent-speech-processing-sherpa:CUSTOM_TAG .
    ```

4. Update your OpenVidu deployment by setting property `docker_image` in file 
[`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment):

    ```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
    docker_image: <YOUR_DOCKERHUB_ACCOUNT>/agent-speech-processing-sherpa:CUSTOM_TAG
    live_captions:
      provider: sherpa
      sherpa:
        model: sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06 # Or any other model you added in your custom image
    ```

##### GPU acceleration for Sherpa provider

Sherpa provider supports GPU acceleration for faster, more efficient transcriptions.

**Prerequisites**

- The OpenVidu node running the Speech Processing agent must have a compatible **NVIDIA GPU (>= CUDA 11.0)**{.no-break} with the appropriate [NVIDIA Container Toolkit :fontawesome-solid-external-link:{.external-link-icon}](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html){:target="_blank" .no-break} installed.
- The OpenVidu node must have enough disk and memory to handle the large Docker containers with GPU support (+4GB).

    !!! info
        - Check your Nvidia GPU compatibility by running the following command, which must show a table with GPU info: `nvidia-smi`{.no-break}
        - Check your NVIDIA Container Toolkit installation with command: `nvidia-ctk --version`
        - You can run a smoke test to confirm that containers will have access to the GPU:
            - For CUDA >= 12: `docker run --rm --gpus all nvidia/cuda:12.9.1-base-ubuntu24.04 nvidia-smi`
            - For CUDA == 11: `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`

**Enable GPU acceleration**

Set the following properties in file [`agent-speech-processing.yaml`](#how-to-enable-live-captions-service-in-your-openvidu-deployment) to enable GPU acceleration for Sherpa provider:

```yaml title="<a href='https://github.com/OpenVidu/openvidu-agents/blob/3.5.0/speech-processing/agent-speech-processing.yaml' target='_blank'>agent-speech-processing.yaml</a>"
docker_image: docker.io/openvidu/agent-speech-processing-sherpa-cuda12:3.5.0 #(1)!

enabled: true #(2)!

docker_options: #(3)!
    gpus: all

live_captions:
  provider: sherpa
  sherpa:
    model: sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06 # Or any other model you want to use
    provider: cuda  #(4)!
```

1. **agent-speech-processing-sherpa-cuda12** image is compatible with NVIDIA GPUs with CUDA 12.0 or higher. **agent-speech-processing-sherpa-cuda11** image is compatible with NVIDIA GPUs with CUDA 11.x.
2. This property is necessary for the agent container to launch.
3. These Docker options are necessary to enable GPU access for the agent container.
4. This property is necessary to tell the agent to use the GPU-enabled runtime of Sherpa ONNX instead of CPU.

After setting those YAML properties restart your OpenVidu deployment:

```bash
sudo systemctl restart openvidu
```

The agent Docker image will be pulled if not already present in the node (it may take some time, as GPU-compatible images are +4GB). Once the agent is up and running, confirm that it is using the GPU by checking its startup logs, which should show:

```log
...
INFO:openvidu_unified.sherpa:Sherpa STT execution provider: 'cuda' (normalized: 'cuda') — running GPU readiness checks
INFO:openvidu_unified.sherpa:Host NVIDIA driver max CUDA version: 13.0
INFO:openvidu_unified.sherpa:NVIDIA GPU: 0, NVIDIA A10G, 23028 MiB, 0 MiB, 580.126.09
INFO:openvidu_unified.sherpa:Container CUDA toolkit version: 12.9.1
INFO:openvidu_unified.sherpa:CUDA compatibility OK: host driver supports up to CUDA 13.0 >= container toolkit 12.9.1
INFO:openvidu_unified.sherpa:CUDA runtime libraries found: cudart, cublas, cudnn (3/3)
INFO:openvidu_unified.sherpa:sherpa-onnx version: 1.12.27+cuda12.cudnn9
INFO:openvidu_unified.sherpa:sherpa-onnx CUDA wheel detected — GPU inference is available
INFO:openvidu_unified.sherpa:sherpa-onnx CUDA provider libraries found: ['libonnxruntime_providers_cuda.so', 'libonnxruntime_providers_tensorrt.so']
INFO:openvidu_unified.sherpa:sherpa-onnx CUDA generation matches container: cuda12
INFO:openvidu_unified.sherpa:All GPU readiness checks passed ✓
...
```

## Tutorial

Check out the [Live Captions tutorial](../tutorials/ai-services/openvidu-live-captions.md) for a complete example.

## Configuration reference

Below are the properties related to the Live Captions service available in the `agent-speech-processing.yaml` file.

```yaml
# Docker image of the agent.
docker_image: docker.io/openvidu/agent-speech-processing-vosk:3.5.0

live_captions:
  # How this agent will connect to Rooms [manual, automatic]
  # - manual: the agent will connect to new Rooms only when your application dictates it by using the Agent Dispatch API.
  # - automatic: the agent will automatically connect to new Rooms.
  processing: manual

  # Which speech-to-text AI provider to use [aws, azure, google, openai, azure_openai, groq, deepgram, assemblyai, fal, clova, speechmatics, gladia, sarvam, mistralai, cartesia, soniox, nvidia, elevenlabs, simplismart, vosk, sherpa]
  # The custom configuration for the selected provider must be set below
  provider: vosk

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

  nvidia:
    # API key for NVIDIA. See https://build.nvidia.com/explore/speech?integrate_nim=true&hosted_api=true&modal=integrate-nim
    # Required when using NVIDIA's cloud services. To use a self-hosted NVIDIA Riva server setup "server" and "use_ssl" instead.
    api_key:
    # The NVIDIA Riva ASR model to use. Default is "parakeet-1.1b-en-US-asr-streaming-silero-vad-sortformer"
    # See available models: https://build.nvidia.com/search/models?filters=usecase%3Ausecase_speech_to_text
    model:
    # The NVIDIA function ID for the model. Default is "1598d209-5e27-4d3c-8079-4751568b1081"
    function_id:
    # Whether to add punctuation to transcription results. Default is true.
    punctuate:
    # The language code for transcription. Default is "en-US"
    language_code:
    # Audio sample rate in Hz. Default is 16000.
    sample_rate:
    # The NVIDIA Riva server address. Default is "grpc.nvcf.nvidia.com:443"
    # For self-hosted NIM, use your server address (e.g., "localhost:50051")
    server:
    # Whether to use SSL for the connection. Default is true.
    # Set to false for locally hosted Riva NIM services without SSL.
    use_ssl:

  spitch:
    # API key for Spitch. See https://docs.spitch.app/keys
    api_key:
    # Language short code for the generated speech. For supported values, see https://docs.spitch.app/concepts/languages
    language:

  elevenlabs:
    # API key for ElevenLabs. See https://elevenlabs.io/app/settings/api-keys
    api_key:
    # The ElevenLabs STT model to use. Valid values are ["scribe_v1", "scribe_v2", "scribe_v2_realtime"]. See https://elevenlabs.io/docs/overview/models#models-overview
    model_id:
    # An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically
    language_code:
    # Custom base URL for the API. Optional.
    base_url:
    # Audio sample rate in Hz. Default is 16000.
    sample_rate:
    # Whether to tag audio events like (laughter), (footsteps), etc. in the transcription. Only supported for Scribe v1 model. Default is True
    tag_audio_events:
    # Whether to include word-level timestamps in the transcription. Default is false.
    include_timestamps:

  simplismart:
    # API key for SimpliSmart. See https://docs.simplismart.ai/model-suite/settings/api-keys
    api_key:
    # Model identifier for the backend STT model. One of ["openai/whisper-large-v2", "openai/whisper-large-v3", "openai/whisper-large-v3-turbo"]
    # Default is "openai/whisper-large-v3-turbo"
    model:
    # Language code for transcription (default: "en"). See https://docs.simplismart.ai/get-started/playground/transcription-models#supported-languages-with-their-codes
    language:
    # Operation to perform. "transcribe" converts speech to text in the original language, "translate" translates into English. Default is "transcribe".
    task:
    # If true, disables timestamp generation in transcripts. Default is true
    without_timestamps:
    # Minimum duration (ms) for a valid speech segment. Default is 0
    min_speech_duration_ms:
    # Decoding temperature (affects randomness). Default is 0.0
    temperature:
    # Whether to permit multilingual recognition. Default is false
    multilingual:

  vosk:
    # Vosk language model. This provider requires docker_image "docker.io/openvidu/agent-speech-processing-vosk"
    # Below is the list of pre-installed models in the container (available at https://alphacephei.com/vosk/models):
    # - vosk-model-en-us-0.22-lgraph (English US)
    # - vosk-model-small-cn-0.22 (Chinese)
    # - vosk-model-small-de-0.15 (German)
    # - vosk-model-small-en-in-0.4 (English India)
    # - vosk-model-small-es-0.42 (Spanish)
    # - vosk-model-small-fr-0.22 (French)
    # - vosk-model-small-hi-0.22 (Hindi)
    # - vosk-model-small-it-0.22 (Italian)
    # - vosk-model-small-ja-0.22 (Japanese)
    # - vosk-model-small-nl-0.22 (Dutch)
    # - vosk-model-small-pt-0.3 (Portuguese)
    # - vosk-model-small-ru-0.22 (Russian)
    model: vosk-model-en-us-0.22-lgraph
    # Language code for reference. It has no effect other than observability purposes.
    # If a pre-installed "model" is declared, this will be set automatically if empty.
    language:
    # Audio sample rate in Hz. Default is 16000.
    sample_rate:
    # Whether to return interim/partial results during recognition. Default is true.
    partial_results:
    # Whether to override Vosk's built-in Voice Activity Detection (VAD) with Silero's VAD. Default is false.
    use_silero_vad: false

  sherpa:
    # sherpa streaming model. This provider requires docker_image "docker.io/openvidu/agent-speech-processing-sherpa"
    # Below is the list of pre-installed models in the container (available at https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models):
    # - sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06 (English)
    # - sherpa-onnx-streaming-zipformer-es-kroko-2025-08-06 (Spanish)
    # - sherpa-onnx-streaming-zipformer-de-kroko-2025-08-06 (German)
    # - sherpa-onnx-streaming-zipformer-fr-kroko-2025-08-06 (French)
    # - sherpa-onnx-streaming-zipformer-ar_en_id_ja_ru_th_vi_zh-2025-02-10 (Multilingual: Arabic, English, Indonesian, Japanese, Russian, Thai, Vietnamese, Chinese)
    model: sherpa-onnx-streaming-zipformer-en-kroko-2025-08-06
    # Language code for reference. Auto-detected from model name if not set.
    language:
    # Runtime provider for sherpa-onnx. Supported values: "cpu" or "cuda". Default is "cpu".
    # Learn about GPU acceleration at https://openvidu.io/docs/ai/live-captions/#gpu-acceleration-for-sherpa-provider
    provider:
    # Audio sample rate in Hz. Default is 16000.
    sample_rate:
    # Whether to return interim/partial results during recognition. Default is true.
    partial_results:
    # Number of threads for ONNX Runtime. Default is 2.
    num_threads:
    # Recognizer type ("transducer", "paraformer", "zipformer_ctc", "nemo_ctc", "t_one_ctc"). Auto-detected from model name if not set.
    recognizer_type:
    # Decoding method ("greedy_search", "modified_beam_search"). Default is "greedy_search".
    decoding_method:
    # Whether to override sherpa's built-in Voice Activity Detection (VAD) with Silero's VAD. Default is false.
    use_silero_vad: false
```
