import logging
import os
import asyncio
from livekit import agents, rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)

from livekit.plugins import (
    cartesia,
    openai,
    deepgram,
    silero,
    turn_detector,
    elevenlabs,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins.openai import LLM
from livekit.plugins.rime import TTS

# from livekit.agents.utils import cache
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")

def prewarm(proc: JobProcess):
    try:
        logger.info("Running prewarm")
        proc.userdata["vad"] = silero.VAD.load()
    except Exception as e:
        logging.error(f"Failed to load VAD: {str(e)}")
        raise
  
    # tts = cartesia.TTS()
    # await tts.synthesize("One moment please...")
    
    

async def keep_alive(ctx):
    while True:
        await asyncio.sleep(30)
        logger.debug("Sending keep-alive ping")
        try:
            await ctx.room.send_data({"type": "ping"})
        except Exception as e:
            logger.warning(f"Keep-alive failed: {str(e)}")

async def entrypoint(ctx: JobContext):
    
    # adding arabic for using both eng and arabic cool
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice."
            "Use short, clear responses, and avoid using unpronounceable punctuation."
            "Created as a demo to demonstrate the capabilities of the LiveKit agent framework."
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    tllm = LLM.with_together(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K",
        api_key=os.getenv("TOGETHER_API_KEY"),
        # timeout=30,#
        # max_retries=3,
    )
    
    

    # tllm = cache(tllm, ttl=300)

    from typing import AsyncIterable    
    
    async def process_track(ctx: JobContext, track: rtc.Track, agent: VoicePipelineAgent):
        stt = deepgram.STT(
            model="nova-2-general",
            interim_results=True,
            sample_rate=16000,
       )
        stt_stream = stt.stream()
        audio_stream = rtc.AudioStream(track)
        asyncio.create_task(process_text_from_speech(stt_stream, agent))
        async for audio_event in audio_stream:
            stt_stream.push_frame(audio_event.frame)
        stt_stream.end_input()
    
    async def process_text_from_speech(stream: AsyncIterable[agents.stt.SpeechEvent], agent: VoicePipelineAgent):
        try:
            async for event in stream:
                if event.type == agents.stt.SpeechEventType.FINAL_TRANSCRIPT:
                    text = event.alternatives[0].text
                    logger.info(f"Final transcript received: {text}")
                    await agent.say(f"You said: {text}", allow_interruptions=True)  
                elif event.type == agents.stt.SpeechEventType.INTERIM_TRANSCRIPT:
                    logger.debug(f"Interim transcript: {event.alternatives[0].text}")
                elif event.type == agents.stt.SpeechEventType.START_OF_SPEECH:
                    logger.debug("Start of speech detected")
                    agent.interrupt()  
                elif event.type == agents.stt.SpeechEventType.END_OF_SPEECH:
                    logger.debug("End of speech detected") 
        except Exception as e:
            logger.error(f"Error in process_text_from_speech: {str(e)}") 
        finally:
            await stream.aclose()
    
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(
            model="nova-2-general",
            interim_results=True,
            sample_rate=16000,       
        ),
        llm=tllm,
        tts=TTS(  
            model="mist",
            speaker="rainforest",
            speed_alpha=0.9,
            reduce_latency=True,
        ),
        turn_detector=turn_detector.EOUModel(),
        min_endpointing_delay=0.5, 
        max_endpointing_delay=2.0,  
        chat_ctx=initial_ctx,
    )

    usage_collector = metrics.UsageCollector()

    # Synchronous callback for metrics collected
    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)
        logger.debug(f"Metrics collected: {agent_metrics.__dict__}")


    @agent.llm.on("response")
    def on_llm_response(response):
        logger.debug(f"LLM response: {response}")
        asyncio.create_task(handle_llm_response_async(response))

    async def handle_llm_response_async(response):
        try:
            logger.debug(f"Async handling of LLM response: {response}")
        except Exception as e:
            logger.error(f"Error handling LLM response: {str(e)}")


    @agent.stt.on("transcript")
    def on_transcript(transcript, is_final):
        logger.debug(f"STT transcript: {transcript}, final: {is_final}")
        asyncio.create_task(handle_transcript_async(transcript, is_final))

    async def handle_transcript_async(transcript, is_final):
        # async logic like  saving to a database for later
        logger.debug(f"Async handling of transcript: {transcript}, final: {is_final}")


    try:
        @ctx.room.on("track_subscribed")
        def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.RemoteParticipant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                logger.info(f"Audio track subscribed for participant {participant.identity}")
                asyncio.create_task(process_track(ctx, track, agent))
        
        agent.start(ctx.room, participant)
        logger.info("Agent started successfully")

        # Initial greeting no need to check tracks here
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
    
    
    
    # elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")      
    # if not elevenlabs_api_key:
    #     logger.error("ELEVENLABS_API_KEY not found in environment variables")
    #     raise ValueError("ELEVENLABS_API_KEY is required")
    # # switching from cartesia no longer workin ..
    # ttse = elevenlabs.TTS(
    #     api_key=elevenlabs_api_key,
    #     model_id="eleven_multilingual_v2",
    # )