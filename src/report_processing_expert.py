import os
import json
import dotenv

import omegaconf
from omegaconf import DictConfig

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate


class ReportProcessingExpert:
    def __init__(self, API_KEY: str, report_processing_config: DictConfig):
        self.report_processing_config = report_processing_config
        model_name = self.report_processing_config["model"]
        expert_prompt_template = self.report_processing_config["expert_prompt_template"]

        self.llm = ChatOpenAI(api_key=API_KEY, model=model_name, temperature=0)
        self.prompt_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(expert_prompt_template)
        ])
        self.chain = self.prompt_template | self.llm

    def process_report_to_json_string(self, report_text: str, user_info: dict) -> str:
        user_info_str = json.dumps(user_info) if user_info else "{}"
        result = self.chain.invoke({"report_text": report_text, "user_info": user_info_str})
        processed_report = result.content.strip()
        return processed_report

    def __convert_processed_report_to_json(self, processed_report):
        if processed_report.startswith("```") and processed_report.endswith("```"):
            processed_report = "\n".join(processed_report.splitlines()[1:-1]).strip()

        try:
            structured_data = json.loads(processed_report)
        except json.JSONDecodeError as e:
            raise ValueError("Failed to decode JSON. Output received:\n" + processed_report) from e

        return structured_data

    def process_report(self, report_text: str, user_info: dict) -> dict:
        processed_report = self.process_report_to_json_string(report_text=report_text, user_info=user_info)
        structured_data = self.__convert_processed_report_to_json(processed_report=processed_report)
        return structured_data


if __name__ == "__main__":
    dotenv.load_dotenv()
    report_path = r"F:\SCULPD\SculpdScanner\data\test_images\scanner_outputs\normal_25-29_percents_report.txt"

    REPORT_PROCESSING_CONFIG_PATH = os.getenv("REPORT_PROCESSING_CONFIG_PATH")
    API_KEY = os.getenv("API_KEY")

    report_file = open(report_path, "r")
    health_scanner_report = report_file.read()
    report_file.close()

    report_processing_config = omegaconf.OmegaConf.load(REPORT_PROCESSING_CONFIG_PATH)["health_expert"]

    report_processing_expert = ReportProcessingExpert(
        API_KEY=API_KEY,
        report_processing_config=report_processing_config
    )

    user_info = {"age": 35, "height_cm": 180, "weight_kg": 110}

    output = report_processing_expert.process_report_to_json_string(health_scanner_report, user_info)

    print(output)

