from __future__ import annotations

from typing import Any


class ImageProvider:
    def __init__(
        self,
        vision_qa_model_name: str = "dandelin/vilt-b32-finetuned-vqa",
        image_caption_model_name: str = "Salesforce/blip-image-captioning-base",
        default_prompt: str = "What is in this image?",
    ) -> None:
        self.vision_qa_model_name = vision_qa_model_name
        self.image_caption_model_name = image_caption_model_name
        self.default_prompt = default_prompt
        self._vqa_pipeline = None
        self._caption_pipeline = None

    def verify_image(self, image_path: str) -> None:
        from PIL import Image

        with Image.open(image_path) as image:
            image.verify()

    def _open_image(self, image_path: str):
        from PIL import Image

        with Image.open(image_path) as image:
            return image.convert("RGB")

    def _get_vqa_pipeline(self):
        if self._vqa_pipeline is None:
            from transformers import pipeline

            self._vqa_pipeline = pipeline(
                "visual-question-answering",
                model=self.vision_qa_model_name,
            )
        return self._vqa_pipeline

    def _get_caption_pipeline(self):
        if self._caption_pipeline is None:
            from transformers import pipeline

            self._caption_pipeline = pipeline(
                "image-to-text",
                model=self.image_caption_model_name,
            )
        return self._caption_pipeline

    def answer_question(self, image_path: str, prompt: str | None = None) -> str:
        image = self._open_image(image_path)
        question = prompt or self.default_prompt

        if prompt:
            vqa_pipeline = self._get_vqa_pipeline()
            result = vqa_pipeline(image=image, question=question)
            if isinstance(result, list) and result:
                top_result = result[0]
                answer = top_result.get("answer")
                if answer:
                    return answer
            raise RuntimeError("Vision Q&A model returned no answer.")

        caption_pipeline = self._get_caption_pipeline()
        result = caption_pipeline(image)
        if isinstance(result, list) and result:
            first_item: Any = result[0]
            if isinstance(first_item, dict):
                caption = first_item.get("generated_text")
                if caption:
                    return caption
        raise RuntimeError("Image captioning model returned no description.")
