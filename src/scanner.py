import openai
from omegaconf import OmegaConf, DictConfig
from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

from src.image_processor import ImageProcessor


class HealthScanner:
    def __init__(self, openai_api_key, scanner_config: DictConfig, image_processor: ImageProcessor):
        self.scanner_config = scanner_config
        self.image_processor = image_processor

        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
        self.image_analysis_tool = Tool(
            name="HealthScanner",
            func=self.get_image_description,
            description="User health analysis tool by photo"
        )
        self.agent = initialize_agent([self.image_analysis_tool], self.llm, agent_type="zero-shot-react-description", verbose=True)

    def get_image_description(self, image_path: str) -> str:
        image = self.image_processor.read_image(image_path)
        image_base64 = self.image_processor.process_image(image)

        prompt = self.scanner_config["scanner_prompt"]
        response = openai.Image.create(
            prompt=prompt,
            image=image_base64,
            n=1
        )

        image_description = response['data'][0]['text']
        return image_description

    def run_agent(self, image_path: str) -> str:
        result = self.agent.invoke(image_path)
        return result


if __name__ == "__main__":

    config = OmegaConf.load(config_path)
    image_processor = ImageProcessor(config["image_processing"])
    health_scanner = HealthScanner(openai_api_key, config["health_scanner"], image_processor)

    print(health_scanner.run_agent(image_path))

