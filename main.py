import argparse
from typing import Generator, Tuple
import numpy as np 
import os
from longuru import logger
from detenv import load_dotenv

# TODO: Create speech service and import it here
# TODO: Create agent and import it

# TODO: lookup this generator function

from fastrtc import(
    AlgoOptions,
    ReplyOnPause,
    Stream,
)

#load env variables
load_dotenv()

#log
logger.remove()
logger.add(
    lambda msg: print(msg),
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{leve}</level> | <level>{message}</level>",
)

# initialize services with defaults from environment variables
speech_service = None
agent = Agent()

# get variables from .env
default_tts_provider = os.getenv("TTS_PROVIDER").lower()
default_stt_provider = os.getenv("STT_PROVIDER").lower()

def response(
    audio: tuple[int, np.ndarray],
) -> Generator[Tuple[int, np.ndarray], None, None]:
    """
    Process audio input, transcibe it, generate a response using the agent

    Args:
        audio: Tuple containing samle rate and audio data

    Yields:
        Tubles of (sample_rate, audio_array) for audio playback
    """

    logger.info("Received audio input")
    logger.debug("Transcribing audio...")


    transcript = speech_service.speech_to_text(audio, ) # stt_kworges here if needded
    
    logger.info(f'Transcribed: "{transcript}"')
    logger.debug("Running agent...")

    agent_response = agent.invoke(transcript)
    response_text = agent_response["messages"][-1]["content"]

    logger.infor(f'Response: "{response_text}"')
    logger.debug("Generating speec...")

    yield from speeck_service.text_to_speech(response_text, )# stt_kworges here if needded


# FreeRTC stream
def create_stream() -> Stream:
    """
    Create and configure a Stream instance with audio capabilities.

    Returns:
        Stream: Configured FastRTC Stream instance
    """
    return Stream(
        modality="audio",
        mode="send-receive",
        handler=ReplyOnPause(
            response,
            algo_options=AlgoOptions(
                speech_threshold=0.2,
            ),
        ),
    )




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastRTC Voice Agent")
    parser.add_argument(
        "--phone",
        action="store_true",
        help="Launch with FastRTC phone interface (automatically provides a temporary phone number)",
    )
    parser.add_argument(
        "--tts", 
        default=default_tts_provider,
        help="TTS provider to use",
    )
    parser.add_argument(
        "--stt", 
        default=default_stt_provider,
        help="STT provider to use",
    )
    parser.add_argument(
        "--voice", 
        type=str, 
        help="Voice ID/name to use",
        default=default_voice_id,
    )

    args = parser.parse_args()

    # configuration in global variables
    tts_provider = args.tts
    stt_provider = args.stt
    speed = args.speed
    
    speech_service = SpeechService(
        tts_provider=tts_provider, 
        stt_provider=stt_provider
    )
    
    # info about the configuration
    logger.info(f"Initialized speech service with {tts_provider} TTS provider")
    logger.info(f"Initialized speech service with {stt_provider} STT provider")
    logger.info(f"tts model preloaded during startup")
    
    stream = create_stream()
    logger.info("Stream handler configured")

    if args.phone:
        logger.info("Launching with FastRTC phone interface...")
        stream.fastphone()
    else:
        logger.info("Launching with Gradio UI...")
        stream.ui.launch()