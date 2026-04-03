from universal_ai_agent.providers.huggingface import MultilingualTranslationProvider


def test_translation_provider_detects_and_normalizes_language(monkeypatch):
    provider = MultilingualTranslationProvider("fake-model")

    assert provider.detect_language("Hola amigo") == "es"
    assert provider._normalize_language_code("French") == "fr"


def test_translation_provider_translates_with_detected_source(monkeypatch):
    provider = MultilingualTranslationProvider("fake-model")

    monkeypatch.setattr(provider, "detect_language", lambda text: "en")

    class FakeTokenizer:
        def __init__(self):
            self.src_lang = None

        def __call__(self, text, return_tensors="pt"):
            return {"input_ids": [1, 2, 3]}

        def get_lang_id(self, language):
            return 7

        def batch_decode(self, generated, skip_special_tokens=True):
            return ["bonjour"]

    class FakeModel:
        def generate(self, **kwargs):
            return [[101, 102]]

    monkeypatch.setattr(provider, "_load_components", lambda: (FakeModel(), FakeTokenizer()))

    assert provider.translate("hello", "fr") == "bonjour"
