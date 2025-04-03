import openai


class HealthScanner:
    def __init__(self, image_processor):
        self.image_processor = image_processor

    def analyze_image(self, image_path: str) -> str:
        image_base64 = self.image_processor.get_image_base64(image_path)

        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system",
                 "content": "Describe the health-related visual aspects of the person in the image, including posture, body composition, and skin conditions."},
                {"role": "user", "content": [{"type": "image", "image": image_base64}]}
            ],
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"]
