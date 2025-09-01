
# This file defines the Agent class, which orchestrates the interaction between STT, LLM, and TTS services.

# Import necessary modules
from src.llm_service import LLMService
from src.speech.stt.provider import STTProvider
from src.speech.tts.provider import TTSProvider
from src.chat_history import ChatHistory

class Agent:
    """
    The Agent class is responsible for handling the overall flow of the voice agent.
    It takes audio input, transcribes it, sends it to an LLM, and then synthesizes the LLM's response into audio.
    """
    def __init__(self, llm_service: LLMService, stt_service: STTProvider, tts_service: TTSProvider, chat_history: ChatHistory):
        """
        Initializes the Agent with instances of LLMService, STTProvider, and TTSProvider.

        Args:
            llm_service (LLMService): An instance of the Large Language Model service.
            stt_service (STTProvider): An instance of the Speech-to-Text service.
            tts_service (TTSProvider): An instance of the Text-to-Speech service.
            chat_history (ChatHistory): An instance of the ChatHistory service for managing conversation context.
        """
        self.llm_service = llm_service
        self.stt_service = stt_service
        self.tts_service = tts_service
        self.chat_history = chat_history

    async def process_audio(self, audio_data: bytes) -> bytes:
        """
        Processes the incoming audio, transcribes it, gets a response from the LLM, and synthesizes the response to audio.

        Args:
            audio_data (bytes): The raw audio data from the user.

        Returns:
            bytes: The synthesized audio response from the agent.
        """
        # 1. Transcribe the audio input using the STT service
        user_transcript = await self.stt_service.transcribe(audio_data)
        print(f"User: {user_transcript}")

        # 2. Add user's message to chat history
        self.chat_history.add_message("user", user_transcript)

        # 3. Get response from the LLM service based on the chat history
        llm_response_text = await self.llm_service.get_response(self.chat_history.get_history())
        print(f"Agent: {llm_response_text}")

        # 4. Add agent's message to chat history
        self.chat_history.add_message("assistant", llm_response_text)

        # 5. Synthesize the LLM's text response into audio using the TTS service
        agent_audio_response = await self.tts_service.synthesize(llm_response_text)

        return agent_audio_response
