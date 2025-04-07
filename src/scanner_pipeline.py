import os
import dotenv
from omegaconf import OmegaConf

from src.image_processor import ImageProcessor
from src.health_scanner import HealthScanner
from src.report_processing_expert import ReportProcessingExpert


class ScannerPipeline:
    def __init__(self, scanner: HealthScanner, report_processing_expert: ReportProcessingExpert):
        self.scanner = scanner
        self.report_processing_expert = report_processing_expert

    def run(self, image_path: str, user_info: dict):
        scanner_report = self.scanner.get_image_description(image_path)
        output = report_processing_expert.process_report_to_json_string(scanner_report, user_info)

        return output


if __name__ == "__main__":
    dotenv.load_dotenv()

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

    image_path = r"F:\SCULPD\SculpdScanner\data\test_images\normal_images\20-24_percents.jpg"
    user_info = {"age": 35, "height_cm": 180, "weight_kg": 110}

    print(scanner_pipeline.run(image_path=image_path, user_info=user_info))
