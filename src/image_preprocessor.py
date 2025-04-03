import base64


class ImagePreprocessor:
    def __init__(self):
        pass

    def preprocess_image(self):
        pass

    def get_image_base64(self, image_path: str):
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        return image_base64

