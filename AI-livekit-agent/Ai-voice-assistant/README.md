<a href="https://livekit.io/">
  <img src="./.github/assets/livekit-mark.png" alt="LiveKit logo" width="100" height="100">
</a>

# Python Voice Agent

<p>
  <a href="https://cloud.livekit.io/projects/p_/sandbox"><strong>Deploy a sandbox app</strong></a>
  •
  <a href="https://docs.livekit.io/agents/overview/">LiveKit Agents Docs</a>
  •
  <a href="https://livekit.io/cloud">LiveKit Cloud</a>
  •
  <a href="https://blog.livekit.io/">Blog</a>
</p>

A basic example of a voice agent using LiveKit and Python.

## Dev Setup

Clone the repository and install dependencies to a virtual environment:

```console
# Linux/macOSAI Voice Assistant with LiveKit and ElevenLabs (Arabic Support)
This project implements a real-time voice assistant using the LiveKit Agents framework, powered by ElevenLabs for text-to-speech (TTS) with Arabic language support. It integrates Deepgram for speech-to-text (STT) and Together AI's LLM for natural language processing. The assistant can listen to user input, process it, and respond via voice, with a focus on supporting Arabic.

Features
Real-time voice interaction using LiveKit Agents.
Arabic language support for TTS via ElevenLabs' eleven_multilingual_v2 model.
Speech recognition with Deepgram, configured for Arabic (ar language code).
LLM-powered responses using Together AI's meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K.
Voice activity detection (VAD) with Silero.
Configurable endpointing for natural conversation flow.
Prerequisites
Python 3.11 or higher.
A LiveKit server setup (or access to a hosted instance).
API keys for:
ElevenLabs (TTS)
Deepgram (STT)
Together AI (LLM)
Installation
Clone the Repository:
bash
Wrap
Copy
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
Set Up a Virtual Environment:
bash
Wrap
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:
bash
Wrap
Copy
pip install -r requirements.txt
If you don’t have a requirements.txt yet, install these packages:
bash
Wrap
Copy
pip install livekit-agents livekit-plugins-elevenlabs livekit-plugins-deepgram livekit-plugins-silero livekit-plugins-openai python-dotenv
Configure Environment Variables: Create a .env.local file in the root directory and add your API keys:
text
Wrap
Copy
ELEVENLABS_API_KEY=<your-elevenlabs-api-key>
DEEPGRAM_API_KEY=<your-deepgram-api-key>
TOGETHER_API_KEY=<your-together-api-key>
Get ELEVENLABS_API_KEY from ElevenLabs.
Get DEEPGRAM_API_KEY from Deepgram.
Get TOGETHER_API_KEY from Together AI.
Usage
Run the Voice Assistant:
bash
Wrap
Copy
python main.py
This starts the LiveKit worker, which connects to a room and begins the voice assistant pipeline.
Join the LiveKit Room:
Use a LiveKit client (e.g., the LiveKit Web SDK or a mobile app) to join the same room as a participant.
The assistant will greet you in Arabic: "مرحباً، كيف يمكنني مساعدتك اليوم؟" ("Hello, how can I help you today?").
Interact:
Speak in Arabic, and the assistant will transcribe your speech, process it with the LLM, and respond in Arabic via ElevenLabs TTS.
Example: Say "ما هو الطقس اليوم؟" ("What’s the weather today?"), and the assistant will respond accordingly (if the LLM has weather data).
Project Structure
text
Wrap
Copy
ai-voice-assistant/
├── main.py           # Main script with VoicePipelineAgent setup
├── .env.local        # Environment variables (not tracked by git)
├── requirements.txt  # Python dependencies (optional)
└── README.md         # This file
Code Overview
main.py:
Initializes the LiveKit worker with pre-warming for VAD.
Sets up the VoicePipelineAgent with:
VAD: Silero
STT: Deepgram (Arabic: ar)
LLM: Together AI
TTS: ElevenLabs (multilingual model for Arabic)
Includes event handlers for metrics, transcripts, and LLM responses.
Starts with an Arabic greeting and maintains a keep-alive loop.
Configuration
TTS: Uses eleven_multilingual_v2 for Arabic support. Change voice_id in main.py if you prefer a different voice (see ElevenLabs dashboard for IDs).
STT: Set to Arabic (language="ar") in Deepgram. Adjust if auto-detection is preferred.
LLM: Configured with a system prompt in Arabic for consistency.
Troubleshooting
TTS Not Working: Verify your ElevenLabs API key and ensure you’re within the 10,000-character free tier limit.
Arabic Not Recognized: Confirm Deepgram’s language="ar" setting and test with clear Arabic audio input.
No Response: Check logs for errors (e.g., API key issues) and ensure all services are reachable.
Limitations
Free Tier: ElevenLabs’ free plan limits you to 10,000 characters/month. Upgrade for more usage or custom Arabic voices.
Voice Quality: Pre-made voices might not have a perfect Arabic accent; custom voices require a paid plan.
Network: Requires a stable connection to LiveKit, ElevenLabs, Deepgram, and Together AI servers.
Contributing
Feel free to submit issues or pull requests to improve this project. Suggestions for better Arabic support or additional features are welcome!

License
This project is licensed under the MIT License. See LICENSE for details (create this file if needed).

Acknowledgments
LiveKit for the real-time agents framework.
ElevenLabs for high-quality TTS with Arabic support.
Deepgram for STT capabilities.
Together AI for LLM processing.
cd voice-pipeline-agent-python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 agent.py download-files
```

<details>
  <summary>Windows instructions (click to expand)</summary>
  
```cmd
:: Windows (CMD/PowerShell)
cd voice-pipeline-agent-python
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
</details>


Set up the environment by copying `.env.example` to `.env.local` and filling in the required values:

- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `OPENAI_API_KEY`
- `CARTESIA_API_KEY`
- `DEEPGRAM_API_KEY`

You can also do this automatically using the LiveKit CLI:

```console
lk app env
```

Run the agent:

```console
python3 agent.py dev
```

This agent requires a frontend application to communicate with. You can use one of our example frontends in [livekit-examples](https://github.com/livekit-examples/), create your own following one of our [client quickstarts](https://docs.livekit.io/realtime/quickstarts/), or test instantly against one of our hosted [Sandbox](https://cloud.livekit.io/projects/p_/sandbox) frontends.
