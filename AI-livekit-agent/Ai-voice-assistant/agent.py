import logging
import os
import asyncio

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import cartesia, openai, deepgram, silero, turn_detector, elevenlabs
from livekit.plugins.openai import LLM

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def keep_alive(ctx):
    while True:
        await asyncio.sleep(30)  # Ping every 30 seconds
        logger.debug("Sending keep-alive ping")
        # await ctx.room.send_data({"type": "ping"})

async def entrypoint(ctx: JobContext):
    # adding arabic for using both eng and arabic cool
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
"أنت مساعد صوتي تم إنشاؤه بواسطة LiveKit. واجهتك مع المستخدمين ستكون صوتية."
            "استخدم ردودًا قصيرة وواضحة، وتجنب استخدام علامات ترقيم غير قابلة للنطق. "
            "تم إنشاؤك كعرض توضيحي لإظهار قدرات إطار عمل وكلاء LiveKit."
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    tllm = LLM.with_together(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K",
        api_key=os.getenv("TOGETHER_API_KEY")
    )
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
    if not elevenlabs_api_key:
        logger.error("ELEVENLABS_API_KEY not found in environment variables")
        raise ValueError("ELEVENLABS_API_KEY is required")
    # switching from cartesia no longer workin ..
    ttse = elevenlabs.TTS(
        api_key=elevenlabs_api_key,
        model_id="eleven_multilingual_v2",
    )
    
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=tllm,
        tts=ttse,
        turn_detector=turn_detector.EOUModel(),
        min_endpointing_delay=1.0,
        max_endpointing_delay=3.0,
        chat_ctx=initial_ctx,
    )

    usage_collector = metrics.UsageCollector()

    # Synchronous callback for metrics collected
    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)
        logger.debug(f"Metrics collected: {agent_metrics.__dict__}")

    @agent.stt.on("transcript")
    def on_transcript(transcript, is_final):
        logger.debug(f"STT transcript: {transcript}, final: {is_final}")
        asyncio.create_task(handle_transcript_async(transcript, is_final))

    async def handle_transcript_async(transcript, is_final):
        # async logic like  saving to a database for later
        logger.debug(f"Async handling of transcript: {transcript}, final: {is_final}")

    @agent.llm.on("response")
    def on_llm_response(response):
        logger.debug(f"LLM response: {response}")
        asyncio.create_task(handle_llm_response_async(response))


    async def handle_llm_response_async(response):
        logger.debug(f"Async handling of LLM response: {response}")


    try:
        agent.start(ctx.room, participant)
        logger.info("Agent started successfully")

        await agent.say("Hey, how can I help you today?", allow_interruptions=False)

        asyncio.create_task(keep_alive(ctx))
    except Exception as e:
        logger.error(f"Failed to start or run agent: {str(e)}")
        raise

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )