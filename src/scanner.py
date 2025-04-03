import openai

from src.image_processor import ImageProcessor


class HealthScanner:
    def __init__(self, image_processor: ImageProcessor):
        self.image_processor = image_processor

    def analyze_image(self, image_path: str) -> str:
        image = self.image_processor.read_image(image_path)
        image_base64 = self.image_processor.process_image(image_path)

