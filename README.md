# AI-Powered Arabic Voice Assistant

## Overview
This project is an AI-powered Arabic voice assistant designed for real-time interactions. It integrates **speech-to-text (STT), text-to-speech (TTS), and natural language processing (LLM)**, ensuring smooth and efficient conversations with users.

## Features
- **Real-Time Speech Processing:** Uses LiveKit for WebRTC-based communication.
- **Speech-to-Text (STT):** Deepgram for accurate Arabic transcription.
- **Text-to-Speech (TTS):** ElevenLabs for high-quality Arabic voice output.
- **Language Model (LLM):** Together AI for Arabic-language NLP.
- **Voice Activity Detection (VAD):** Silero-based detection for seamless interactions.
- **Interruption Handling:** The agent intelligently ignores interruptions to maintain smooth conversation flow.

## Configuration
### 1. Environment Variables
Create a `.env.local` file in the root directory and add your API keys:
```
ELEVENLABS_API_KEY=
DEEPGRAM_API_KEY=
TOGETHER_API_KEY=
```

### 2. Voice and Language Settings
- **TTS:** Uses `eleven_multilingual_v2` for Arabic support. Change `voice_id` in `agent.py` if needed.
- **STT:** Set to Arabic (`language="ar"`) in Deepgram for accurate transcription.
- **LLM:** Configured with a system prompt in Arabic for consistency.

## Code Overview
### `agent.py`
- Initializes the **LiveKit worker** with pre-warming for VAD.
- Sets up the `VoicePipelineAgent` with:
  - **VAD:** Silero
  - **STT:** Deepgram (Arabic: `ar`)
  - **LLM:** Together AI
  - **TTS:** ElevenLabs (multilingual model for Arabic)
  - **Turn Detection:** Ensures proper conversation flow
- Includes event handlers for:
  - **Metrics collection**
  - **Transcripts logging**
  - **LLM responses processing**
- Starts with an Arabic greeting and maintains a keep-alive loop.

## How It Works
### 1. Speech-to-Text (STT)
- Converts user speech into text using **Deepgram**.
- Ensures accurate transcription of Arabic input.

### 2. Large Language Model (LLM)
- Processes the transcribed text using **Together AI**.
- Generates an appropriate Arabic response.

### 3. Text-to-Speech (TTS)
- Converts the AI-generated response into **spoken Arabic**.
- Uses **ElevenLabs multilingual voice model** for clear pronunciation.

### 4. Interruption Handling
- Detects interruptions but ignores them while generating a response.
- Ensures smooth and uninterrupted conversation flow.
- Interruptions like "Hello? Can you hear me?" are transcribed but do not interfere with the response generation.
- Once the response is completed, the agent resumes normal listening mode.

## Troubleshooting
### TTS Not Working
- Verify your **ElevenLabs API key**.
- Ensure you are within the **10,000-character free tier** limit.

### Arabic Not Recognized
- Confirm Deepgram’s `language="ar"` setting.
- Test with **clear Arabic audio input**.

### No Response
- Check logs for errors (e.g., **API key issues**).
- Ensure all services (**LiveKit, ElevenLabs, Deepgram, Together AI**) are reachable.

## Limitations
- **Free Tier Limits:** ElevenLabs limits free usage to **10,000 characters/month**.
- **Voice Quality:** Pre-made voices may not have perfect Arabic accents; custom voices require a paid plan.
- **Network Requirements:** Requires a stable connection to **LiveKit, ElevenLabs, Deepgram, and Together AI** servers.

## Contributing
Feel free to submit **issues** or **pull requests** to improve this project. Suggestions for **better Arabic support** or **additional features** are welcome!

## License
This project is licensed under the **MIT License**. See `LICENSE` for details.

## Acknowledgments
Special thanks to:
- **LiveKit** for the real-time agents framework.
- **ElevenLabs** for high-quality TTS with Arabic support.
- **Deepgram** for STT capabilities.
- **Together AI** for LLM processing.

