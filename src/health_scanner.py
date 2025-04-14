import os
import dotenv

from omegaconf import OmegaConf, DictConfig
from openai import OpenAI

from src.image_processor import ImageProcessor


class HealthScanner:
    def __init__(self, API_KEY: str, scanner_config: DictConfig, image_processor: ImageProcessor):
        self.scanner_config = scanner_config
        self.image_processor = image_processor

        self.llm = OpenAI(api_key=API_KEY)

    def get_image_description(self, image_path: str) -> str:
        image = self.image_processor.read_image(image_path)
        image_base64 = self.image_processor.process_image(image)

        prompt = self.scanner_config["scanner_prompt"]
        model = self.scanner_config["model"]
        response = self.llm.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_base64}"}
                    ]
                }
            ]
        )

        return response.output_text


if __name__ == "__main__":
    dotenv.load_dotenv()

    # image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\5-9_percents.jpg"
    image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\10-14_percents_1.jpeg"
    # image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\15-19_percents.jpg"
    # image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\20-24_percents.jpg"
    # image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\25-29_percents.jpg"
    # image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\30-34_percents.jpg"

    SCANNER_CONFIG_PATH = os.getenv("SCANNER_CONFIG_PATH")
    API_KEY = os.getenv("API_KEY")

    config = OmegaConf.load(SCANNER_CONFIG_PATH)
    image_processor = ImageProcessor(config["image_processing"])
    health_scanner = HealthScanner(API_KEY, config["health_scanner"], image_processor)

    print(health_scanner.get_image_description(image_path))
