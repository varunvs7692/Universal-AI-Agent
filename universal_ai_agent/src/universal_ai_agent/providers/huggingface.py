from __future__ import annotations


class HuggingFaceTextProvider:
    def __init__(self, model_name: str, max_length: int = 128) -> None:
        self.model_name = model_name
        self.max_length = max_length
        self._pipeline = None

    def _load_pipeline(self):
        if self._pipeline is None:
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self._pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
        return self._pipeline

    def generate(self, prompt: str) -> str:
        text_pipeline = self._load_pipeline()
        result = text_pipeline(prompt, max_length=self.max_length, do_sample=True)
        return result[0]["generated_text"]


class MultilingualTranslationProvider:
    DEFAULT_LANGUAGE_CODES = {
        "af", "am", "ar", "ast", "az", "ba", "be", "bg", "bn", "br", "bs", "ca",
        "ceb", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "ff", "fi",
        "fr", "fy", "ga", "gd", "gl", "gu", "ha", "he", "hi", "hr", "ht", "hu",
        "hy", "id", "ig", "ilo", "is", "it", "ja", "jv", "ka", "kk", "km", "kn",
        "ko", "lb", "lg", "ln", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr",
        "ms", "my", "ne", "nl", "no", "ns", "oc", "or", "pa", "pl", "ps", "pt",
        "ro", "ru", "sd", "si", "sk", "sl", "so", "sq", "sr", "ss", "su", "sv",
        "sw", "ta", "th", "tl", "tn", "tr", "uk", "ur", "uz", "vi", "wo", "xh",
        "yi", "yo", "zh", "zu",
    }
    LANGUAGE_ALIASES = {
        "arabic": "ar",
        "bengali": "bn",
        "chinese": "zh",
        "english": "en",
        "french": "fr",
        "german": "de",
        "gujarati": "gu",
        "hindi": "hi",
        "italian": "it",
        "japanese": "ja",
        "korean": "ko",
        "marathi": "mr",
        "portuguese": "pt",
        "punjabi": "pa",
        "russian": "ru",
        "spanish": "es",
        "swahili": "sw",
        "tamil": "ta",
        "telugu": "te",
        "turkish": "tr",
        "ukrainian": "uk",
        "urdu": "ur",
        "vietnamese": "vi",
    }

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None
        self._tokenizer = None

    def _load_components(self):
        if self._model is None or self._tokenizer is None:
            from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

            self._tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
            self._model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
        return self._model, self._tokenizer

    def _normalize_language_code(self, language: str) -> str:
        normalized = language.strip().lower().replace("_", "-")
        if normalized in self.LANGUAGE_ALIASES:
            return self.LANGUAGE_ALIASES[normalized]
        primary = normalized.split("-")[0]
        if primary in self.LANGUAGE_ALIASES:
            return self.LANGUAGE_ALIASES[primary]
        return primary

    def detect_language(self, text: str) -> str:
        try:
            from langdetect import detect

            detected = detect(text)
            return self._normalize_language_code(detected)
        except Exception:
            lowered = text.lower()
            if any("\u0900" <= char <= "\u097f" for char in text):
                return "hi"
            if any("\u0600" <= char <= "\u06ff" for char in text):
                return "ar"
            if any(word in lowered for word in ("hola", "gracias", "adios")):
                return "es"
            if any(word in lowered for word in ("bonjour", "merci", "salut")):
                return "fr"
            return "en"

    def get_supported_languages(self) -> set[str]:
        if self._tokenizer is not None and hasattr(self._tokenizer, "lang_code_to_id"):
            return set(self._tokenizer.lang_code_to_id.keys())
        return set(self.DEFAULT_LANGUAGE_CODES)

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
    ) -> str:
        normalized_target = self._normalize_language_code(target_language)
        if normalized_target not in self.get_supported_languages():
            raise ValueError(
                f"Unsupported target language '{target_language}'."
            )
        normalized_source = self._normalize_language_code(
            source_language or self.detect_language(text)
        )
        if normalized_source == normalized_target:
            return text
        model, tokenizer = self._load_components()
        tokenizer.src_lang = normalized_source
        batch = tokenizer(text, return_tensors="pt")
        generated = model.generate(
            **batch,
            forced_bos_token_id=tokenizer.get_lang_id(normalized_target),
        )
        decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
        return decoded[0]


MarianTranslationProvider = MultilingualTranslationProvider
