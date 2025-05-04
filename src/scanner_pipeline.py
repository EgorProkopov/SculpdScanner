import os
import dotenv
import logging
from omegaconf import OmegaConf

from src.image_processor import ImageProcessor
from src.health_scanner import HealthScanner
from src.report_processing_expert import ReportProcessingExpert
from src.logger import get_logger


class ScannerPipeline:
    def __init__(self, scanner: HealthScanner, report_processing_expert: ReportProcessingExpert, max_attempts: int = 6):
        self.scanner = scanner
        self.report_processing_expert = report_processing_expert

        self.max_attempts = max_attempts

        self.logger = get_logger(name=self.__class__.__name__, level=logging.DEBUG)

    def is_valide_report(self, report_text: str) -> bool:
        unsatisfactory_phrases = [
            "I'm sorry",
            "I'm unable",
            "I can't"
        ]
        is_valide_text = not any(phrase in report_text for phrase in unsatisfactory_phrases)
        is_valide_length = len(report_text) > 200
        is_valide = is_valide_text or is_valide_length
        return is_valide

    def run(self, image_path: str, user_info: dict, is_url=True):
        attempt = 0
        scanner_report = None
        while attempt < self.max_attempts:
            scanner_report = self.scanner.get_image_description(image_path, is_url=is_url)
            self.logger.debug(f"Scanner report (attempt {attempt + 1}): {scanner_report}")
            if self.is_valide_report(scanner_report):
                self.logger.info(f"The scanner report was accepted on the {attempt + 1} attempt")
                break

            else:
                self.logger.warning(f"Invalid report on the {attempt + 1} attempt. Trying again.")
                attempt += 1
        else:
            self.logger.error(f"Maximum number of attempts (max_attempts = {self.max_attempts}) is reached")

        output = self.report_processing_expert.process_report_to_json_string(scanner_report, user_info)
        self.logger.debug(f"Final processed output: {output}")
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

    image_path = r"F:\SCULPD\data\bodyfats\35\IMG_3515.jpeg"
    user_info = {"age": 35, "height_cm": 180, "weight_kg": 60}

    scanner_pipeline.run(image_path, user_info)
