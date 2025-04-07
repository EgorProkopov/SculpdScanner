import io
import os
import dotenv

import cv2
import base64
import albumentations as A

from omegaconf import OmegaConf, DictConfig
from PIL import Image


class ImageProcessor:
    def __init__(self, image_processing_config: DictConfig):
        self.image_processing_config = image_processing_config

        clip_limit = self.image_processing_config["clip_limit"]
        tile_grid_size = self.image_processing_config["tile_grid_size"]
        gaussian_blur_limit = self.image_processing_config["gaussian_blur_limit"]

        self.transform = A.Compose([
            A.CLAHE(clip_limit=clip_limit, tile_grid_size=(tile_grid_size, tile_grid_size)),
            A.GaussianBlur(blur_limit=(gaussian_blur_limit, gaussian_blur_limit))
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

    def resize_image(self, image):
        config_image_width = self.image_processing_config["image_width"]
        config_image_height = self.image_processing_config["image_height"]

        save_aspect_ratio = self.image_processing_config["save_aspect_ratio"]
        do_not_resize_smaller_images = self.image_processing_config["do_not_resize_smaller_image"]

        # Check smaller image
        if do_not_resize_smaller_images:
            image_width = image.shape[1]
            if image_width < config_image_width:
                return image

        # Resize with respect to width-height ratio
        if save_aspect_ratio:
            image_width = image.shape[1]
            image_height = image.shape[0]
            new_image_height = int(image_height / image_width * config_image_width)
            resize_transform = A.Resize(new_image_height, config_image_width)
            resized_image = resize_transform(image=image)['image']
        else:
            resize_transform = A.Resize(config_image_height, config_image_width)
            resized_image = resize_transform(image=image)['image']

        return resized_image

    def transform_image(self, image):
        resized_image = self.resize_image(image)
        transformed_image = self.transform(image=resized_image)['image']
        return transformed_image

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
    dotenv.load_dotenv()

    image_path = r""
    CONFIG_PATH = os.getenv("CONFIG_PATH")

    image_processing_config = OmegaConf.load(CONFIG_PATH)["image_processing"]
    image_processor = ImageProcessor(image_processing_config)

    image = image_processor.read_image(image_path)
    transformed_image = image_processor.transform_image(image)
    image_processor.show_image(transformed_image)
    cv2.waitKey()

