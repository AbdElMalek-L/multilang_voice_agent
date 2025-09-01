"""
speech-to-text providers package.
"""
from .whisper_stt import WhisperSTT

__all__ = ["WhisperSTT", "ProviderSTT"]