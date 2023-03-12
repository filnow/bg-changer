import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from utils import readb64
from typing import Tuple


class ImageProcessor:
    def __init__(self, image: str) -> None:
        self.image = readb64(image)
        self.seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
        self.results = self.seg.process(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        self.condition = np.stack((self.results.segmentation_mask,) * 3, axis=-1) > 0.1

    def change_bg(self, bg_image: str) -> Image.Image:
        bg_image_np = readb64(bg_image)
        resized = cv2.resize(bg_image_np, (self.image.shape[1], self.image.shape[0]), interpolation = cv2.INTER_AREA)
        output_image = cv2.cvtColor(np.where(self.condition, self.image, resized), cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(output_image).convert('RGB')
    
    def remove_bg(self, bg_color: Tuple[int, int, int]) -> Image.Image:
        bg_image = np.zeros(self.image.shape, dtype=np.uint8)
        bg_image[:] = bg_color
        output_image = cv2.cvtColor(np.where(self.condition, self.image, bg_image), cv2.COLOR_BGR2RGB)

        return Image.fromarray(output_image).convert('RGB')
    
    def default_bg(self) -> Image.Image:
        return Image.fromarray(self.image).convert('RGB')

    