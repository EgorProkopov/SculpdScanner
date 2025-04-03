import io

import cv2
import base64
import albumentations as A

from omegaconf import OmegaConf, DictConfig
from PIL import Image


class ImageProcessor:
    def __init__(self, image_processing_config: DictConfig):
        self.image_processing_config = image_processing_config

        image_width = self.image_processing_config["image_width"]
        image_height = self.image_processing_config["image_height"]
        clip_limit = self.image_processing_config["clip_limit"]
        tile_grid_size = self.image_processing_config["tile_grid_size"]
        self.transform = A.Compose([
            A.Resize(image_width, image_height),
            A.CLAHE(clip_limit=clip_limit, tile_grid_size=(tile_grid_size, tile_grid_size))
        ])

    def process_image(self, image):
        transformed_image = self.transform_image(image)
        image_base64 = self.get_image_base64(transformed_image)
        return image_base64

    def read_image(self, image_path: str):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read from path: " + image_path)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def transform_image(self, image):
        transformed = self.transform(image=image)
        return transformed['image']

    def show_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Transformed image", image)

    def get_image_base64(self, image):
        pil_image = Image.fromarray(image)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64


if __name__ == "__main__":

    image_processing_config = OmegaConf.load(config_path)["image_processing"]
    image_processor = ImageProcessor(image_processing_config)

    image = image_processor.read_image(image_path)
    transformed_image = image_processor.transform_image(image)
    image_processor.show_image(transformed_image)
    cv2.waitKey()

