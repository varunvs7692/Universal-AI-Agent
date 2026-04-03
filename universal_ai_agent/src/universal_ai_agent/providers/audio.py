from __future__ import annotations


class SpeechRecognitionProvider:
    def __init__(self, language: str = "en") -> None:
        self.language = language
        self._recognizer = None

    def _get_recognizer(self):
        if self._recognizer is None:
            import speech_recognition as sr

            self._recognizer = sr.Recognizer()
        return self._recognizer

    def transcribe(self, audio_path: str) -> str:
        import speech_recognition as sr

        recognizer = self._get_recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=self.language)
