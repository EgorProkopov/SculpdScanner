import os
import dotenv
import gradio as gr
from omegaconf import OmegaConf

from src.image_processor import ImageProcessor
from src.health_scanner import HealthScanner
from src.report_processing_expert import ReportProcessingExpert
from src.scanner_pipeline import ScannerPipeline


def get_training_recommendation(image_path: str, user_info: dict):
    API_KEY = os.getenv("API_KEY")
    SCANNER_CONFIG_PATH = os.getenv("SCANNER_CONFIG_PATH")
    REPORT_PROCESSING_CONFIG_PATH = os.getenv("REPORT_PROCESSING_CONFIG_PATH")

    scanner_config = OmegaConf.load(SCANNER_CONFIG_PATH)
    report_processing_config = OmegaConf.load(REPORT_PROCESSING_CONFIG_PATH)["health_expert"]

    image_processor = ImageProcessor(scanner_config["image_processing"])
    health_scanner = HealthScanner(API_KEY, scanner_config["health_scanner"], image_processor)

    report_processing_expert = ReportProcessingExpert(
        API_KEY=API_KEY,
        report_processing_config=report_processing_config
    )

    scanner_pipeline = ScannerPipeline(scanner=health_scanner, report_processing_expert=report_processing_expert)

    output = scanner_pipeline.run(image_path=image_path, user_info=user_info)
    print(output)
    return output

if __name__ == "__main__":
    dotenv.load_dotenv()
    interface = gr.Interface(
        fn=get_training_recommendation,
        inputs=[gr.Image(type="filepath", label="Upload Your Photo"), gr.TextArea(label='user information', placeholder='{"age": 35, "height_cm": 180, "weight_kg": 110}')],
        outputs=gr.Textbox(label="Image Analysis and Training Recommendations"),
        title="SCULPD Health Scanner",
        description="Upload your photo to receive personalized training recommendations based on your image analysis."
    )

    interface.launch(share=True)
