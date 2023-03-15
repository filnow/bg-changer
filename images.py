import cv2
import numpy as np
from PIL import Image
from typing import Tuple
import paddle
from paddleseg.cvlibs import Config
from paddleseg.transforms import Compose

from ppmatting.core import predict
from utils import readb64


class ImageProcessor:
    def __init__(self, image: str) -> None:
        paddle.set_device('cpu')
        self.cfg = Config('./config/ppmattingv2-stdc1-human_512.yml')
        self.image = readb64(image)
        self.model = self.cfg.model
        self.transforms = Compose(self.cfg.val_transforms)

        self.alpha, self.fg = predict(
            self.model,
            model_path='./config/ppmattingv2-stdc1-human_512.pdparams',
            transforms=self.transforms,
            image_list=[self.image],
            )
        
        self.alpha = self.alpha / 255.0
        self.alpha = self.alpha[:, :, np.newaxis]

    def change_bg(self, bg_image: str) -> Image.Image:
        bg = readb64(bg_image)
        bg = cv2.resize(bg, (self.image.shape[1], self.image.shape[0]), interpolation = cv2.INTER_AREA)
        com = self.alpha * self.fg + (1 - self.alpha) * bg
        com = com.astype('uint8')
        output = cv2.cvtColor(com, cv2.COLOR_BGR2RGB)

        return Image.fromarray(output).convert('RGB')

    
    def remove_bg(self, bg_color: Tuple[int, int, int]) -> Image.Image:
        bg_image = np.zeros(self.image.shape, dtype=np.uint8)
        bg_image[:] = bg_color
        com = self.alpha * self.fg + (1 - self.alpha) * bg_image
        com = com.astype('uint8')
        output = cv2.cvtColor(com, cv2.COLOR_BGR2RGB)

        return Image.fromarray(output).convert('RGB')
    
    def default_bg(self) -> Image.Image:
        return Image.fromarray(self.image).convert('RGB')