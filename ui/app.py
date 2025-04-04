import os
import dotenv
import gradio as gr
from omegaconf import OmegaConf

from src.image_processor import ImageProcessor
from src.scanner import HealthScanner


def get_training_recommendation(image_path):
    API_KEY = os.getenv("API_KEY")
    CONFIG_PATH = os.getenv("CONFIG_PATH")

    config = OmegaConf.load(CONFIG_PATH)

    image_processor = ImageProcessor(config["image_processing"])
    health_scanner = HealthScanner(API_KEY, config["health_scanner"], image_processor)

    response = health_scanner.get_image_description(image_path)
    print(response)
    return response


if __name__ == "__main__":
    dotenv.load_dotenv()
    interface = gr.Interface(
        fn=get_training_recommendation,
        inputs=gr.Image(type="filepath", label="Upload Your Photo"),
        outputs=gr.Textbox(label="Image Analysis and Training Recommendations"),
        title="SCULPD Health Scanner",
        description="Upload your photo to receive personalized training recommendations based on your image analysis."
    )

    interface.launch(share=True)
