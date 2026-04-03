import os
import sys
from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, MarianMTModel, MarianTokenizer
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from PIL import Image
import pyttsx3
from .vision_plugin import VisionPlugin

class UniversalAIAgent:
    """
    Modular, plugin-ready Universal AI Agent for text, voice, image, translation, and device integration.
    """
    def __init__(self, language: str = 'en', model_name: str = 'google/gemma-2b-it'):
        self.language = language
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.text_pipeline = None
        self.speech_recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.vision_model = None
        self.translation_model = None
        self.translation_tokenizer = None
        self.plugins = {}
        self._init_modules()

    def _init_modules(self):
        # Load Gemma 4 (or similar) model for text
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.text_pipeline = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            print(f"[Warning] Could not load Gemma model: {e}")
            self.text_pipeline = None
        # Load translation model (MarianMT as example)
        try:
            translation_model_name = 'Helsinki-NLP/opus-mt-en-ROMANCE'
            self.translation_tokenizer = MarianTokenizer.from_pretrained(translation_model_name)
            self.translation_model = MarianMTModel.from_pretrained(translation_model_name)
        except Exception as e:
            print(f"[Warning] Could not load translation model: {e}")
            self.translation_model = None
        # Load vision model (BLIP)
        try:
            self.vision_model = VisionPlugin()
        except Exception as e:
            print(f"[Warning] Could not load vision model: {e}")
            self.vision_model = None

    def register_plugin(self, name: str, func):
        self.plugins[name] = func

    def text_chat(self, prompt: str) -> str:
        if self.text_pipeline:
            result = self.text_pipeline(prompt, max_length=128, do_sample=True)
            return result[0]['generated_text']
        return f"[Gemma4] (text) You said: {prompt}"

    def voice_chat(self, audio_path: str) -> str:
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.speech_recognizer.record(source)
            text = self.speech_recognizer.recognize_google(audio, language=self.language)
            return self.text_chat(text)
        except Exception as e:
            return f"[Gemma4] (voice) Error: {e}"

    def image_chat(self, image_path: str, prompt: Optional[str] = None) -> str:
        if self.vision_model:
            try:
                return self.vision_model.image_qa(image_path, prompt)
            except Exception as e:
                return f"[Gemma4] (image) Vision model error: {e}"
        else:
            return f"[Gemma4] (image) Vision model not available."

    def translate(self, text: str, target_language: str) -> str:
        if self.translation_model and self.translation_tokenizer:
            batch = self.translation_tokenizer([text], return_tensors="pt", padding=True)
            gen = self.translation_model.generate(**batch, forced_bos_token_id=self.translation_tokenizer.lang_code_to_id.get(target_language, None))
            out = self.translation_tokenizer.batch_decode(gen, skip_special_tokens=True)
            return out[0]
        return f"[Gemma4] (translate) {text} -> {target_language} (translation model integration needed)"

    def speak(self, text: str):
        if self.tts_engine:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        else:
            print("[Gemma4] (tts) TTS engine not available.")

    def call_local_function(self, function_name: str, *args, **kwargs):
        if function_name in self.plugins:
            return self.plugins[function_name](*args, **kwargs)
        return f"[Gemma4] (function) Called {function_name} with {args} {kwargs} (plugin not found)"

if __name__ == "__main__":
    agent = UniversalAIAgent(language='en')
    print(agent.text_chat("Hello, world!"))
    print(agent.voice_chat("sample_audio.wav"))
    print(agent.image_chat("sample_image.jpg", prompt="What do you see?"))
    print(agent.translate("Hello", "fr"))
    agent.speak("This is a test of the text-to-speech system.")
    print(agent.call_local_function("send_sms", "+1234567890", message="Test"))
