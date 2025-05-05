import io
import os
import dotenv
import requests
import base64
import numpy as np

import cv2
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

    def read_image_url(self, image_url: str, timeout=10.0):
        resp = requests.get(image_url, timeout=timeout)
        if resp.status_code != 200:
            raise ValueError(f"Failed to fetch image, status code = {resp.status_code}")

        buf = np.frombuffer(resp.content, dtype=np.uint8)

        image_bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if image_bgr is None:
            raise ValueError(f"Unable to decode image from URL: {image_url}")

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        return image_rgb


    def resize_image(self, image):
        config_image_width = self.image_processing_config["image_width"]
        config_image_height = self.image_processing_config["image_height"]

        save_aspect_ratio = self.image_processing_config["save_aspect_ratio"]
        do_not_resize_smaller_images = self.image_processing_config["do_not_resize_smaller_image"]

        if do_not_resize_smaller_images:
            image_width = image.shape[1]
            if image_width < config_image_width:
                return image

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

    image_url = r"https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/640px-PNG_transparency_demonstration_1.png"
    CONFIG_PATH = os.getenv("SCANNER_CONFIG_PATH")

    image_processing_config = OmegaConf.load(CONFIG_PATH)["image_processing"]
    image_processor = ImageProcessor(image_processing_config)

    image = image_processor.read_image_url(image_url)
    transformed_image = image_processor.transform_image(image)
    image_processor.show_image(transformed_image)
    cv2.waitKey()

