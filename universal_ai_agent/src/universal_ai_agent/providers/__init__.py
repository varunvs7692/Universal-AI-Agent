from universal_ai_agent.providers.device import DeviceActionProvider
from universal_ai_agent.providers.audio import SpeechRecognitionProvider
from universal_ai_agent.providers.huggingface import (
    HuggingFaceTextProvider,
    MultilingualTranslationProvider,
)
from universal_ai_agent.providers.image import ImageProvider
from universal_ai_agent.providers.tts import Pyttsx3Provider

__all__ = [
    "DeviceActionProvider",
    "HuggingFaceTextProvider",
    "ImageProvider",
    "MultilingualTranslationProvider",
    "Pyttsx3Provider",
    "SpeechRecognitionProvider",
]
