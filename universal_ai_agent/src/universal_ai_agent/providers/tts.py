from __future__ import annotations


class Pyttsx3Provider:
    def __init__(self) -> None:
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            import pyttsx3

            self._engine = pyttsx3.init()
        return self._engine

    def speak(self, text: str) -> None:
        engine = self._get_engine()
        engine.say(text)
        engine.runAndWait()
