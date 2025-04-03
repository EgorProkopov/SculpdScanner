from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import openai


class HealthAssistant:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

        self.template = PromptTemplate(
            input_variables=["image_description"],
            template="""
            You are a health expert. Based on the following visual analysis:
            "{image_description}"
            Generate a health report assessing potential health conditions, posture issues, and overall well-being.
            Suggest recommendations for improvement if necessary.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def generate_health_report(self, image_path: str):
        image_description = self.analyze_image(image_path)
        prompt_input = {"image_description": image_description}
        return self.chain.run(prompt_input)


if __name__ == "__main__":
    OPENAI_API_KEY = ""
    assistant = HealthAssistant(openai_api_key=OPENAI_API_KEY)

    image_path = ""
    report = assistant.generate_health_report(image_path)
    print("\nHealth Report:\n", report)
