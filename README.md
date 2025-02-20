# AI Voice Assistant with LiveKit and ElevenLabs (Arabic Support)

This project implements a real-time voice assistant using the LiveKit Agents framework, powered by ElevenLabs for text-to-speech (TTS) with Arabic language support. It integrates Deepgram for speech-to-text (STT) and Together AI's LLM for natural language processing. The assistant can listen to user input, process it, and respond via voice, with a focus on supporting Arabic.

## Features
- Real-time voice interaction using LiveKit Agents.
- Arabic language support for TTS via ElevenLabs' `eleven_multilingual_v2` model.
- Speech recognition with Deepgram, configured for Arabic (`ar` language code).
- LLM-powered responses using Together AI's `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K`.
- Voice activity detection (VAD) with Silero.
- Configurable endpointing for natural conversation flow.

## Prerequisites
- Python 3.11 or higher.
- A LiveKit server setup (or access to a hosted instance).
- API keys for:
  - ElevenLabs (TTS)
  - Deepgram (STT)
  - Together AI (LLM)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/omar-xy/AI-Voice-assistant-LiveKit-agent.git
   cd ai-voice-assistant
   Set Up a Virtual Environment:
2. **Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. install Dependencies:
pip install -r requirements.txt
pip install livekit-agents livekit-plugins-elevenlabs livekit-plugins-deepgram livekit-plugins-silero livekit-plugins-openai python-dotenv

4. configure Environment Variables: Create a .env.local file in the root directory and add your API keys:
ELEVENLABS_API_KEY=<your-elevenlabs-api-key>
DEEPGRAM_API_KEY=<your-deepgram-api-key>
TOGETHER_API_KEY=<your-together-api-key>

Code Overview
agent.py:
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

--------------Acknowledgments-------------------

LiveKit for the real-time agents framework.
ElevenLabs for high-quality TTS with Arabic support.
Deepgram for STT capabilities.
Together AI for LLM processing.
