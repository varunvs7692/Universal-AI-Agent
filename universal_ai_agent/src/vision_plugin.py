from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class VisionPlugin:
    def __init__(self, model_name='Salesforce/blip-image-captioning-base'):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def image_qa(self, image_path, prompt=None):
        image = Image.open(image_path).convert('RGB')
        if prompt:
            inputs = self.processor(image, prompt, return_tensors="pt")
            out = self.model.generate(**inputs)
            return self.processor.decode(out[0], skip_special_tokens=True)
        else:
            inputs = self.processor(image, return_tensors="pt")
            out = self.model.generate(**inputs)
            return self.processor.decode(out[0], skip_special_tokens=True)
