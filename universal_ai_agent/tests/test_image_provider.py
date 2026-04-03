from universal_ai_agent.providers.image import ImageProvider


def test_image_provider_uses_vqa_when_prompt_is_given(monkeypatch):
    provider = ImageProvider()

    monkeypatch.setattr(provider, "_open_image", lambda image_path: f"opened:{image_path}")
    monkeypatch.setattr(
        provider,
        "_get_vqa_pipeline",
        lambda: lambda image, question: [{"answer": f"vqa:{image}:{question}"}],
    )

    assert (
        provider.answer_question("image.jpg", prompt="What is this?")
        == "vqa:opened:image.jpg:What is this?"
    )


def test_image_provider_uses_captioning_without_prompt(monkeypatch):
    provider = ImageProvider(default_prompt="Describe the image.")

    monkeypatch.setattr(provider, "_open_image", lambda image_path: f"opened:{image_path}")
    monkeypatch.setattr(
        provider,
        "_get_caption_pipeline",
        lambda: lambda image: [{"generated_text": f"caption:{image}"}],
    )

    assert provider.answer_question("image.jpg") == "caption:opened:image.jpg"
