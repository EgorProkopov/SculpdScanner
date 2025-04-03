import openai

from src.image_preprocessor import ImagePreprocessor


class HealthScanner:
    def __init__(self, image_processor: ImagePreprocessor):
        self.image_processor = image_processor

    def analyze_image(self, image_path: str) -> str:
        pass
