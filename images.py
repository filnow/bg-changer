import cv2
import numpy as np
from PIL import Image
from typing import Tuple
import paddle
from paddleseg.cvlibs import Config
from paddleseg.transforms import Compose

from ppmatting.core import predict
from utils import readb64


def change_bg(alpha: np.ndarray, 
              fg: np.ndarray, 
              bg_image: str) -> Image.Image:
    bg = readb64(bg_image)
    bg = cv2.resize(bg, (fg.shape[1], fg.shape[0]), interpolation = cv2.INTER_AREA)
    com = alpha * fg + (1 - alpha) * bg
    com = com.astype('uint8')
    output = cv2.cvtColor(com, cv2.COLOR_BGR2RGB)

    return Image.fromarray(output).convert('RGB')

def remove_bg(alpha: np.ndarray, 
              fg: np.ndarray, 
              bg_color: Tuple[int, int, int]) -> Image.Image:
    bg_image = np.zeros(fg.shape, dtype=np.uint8)
    bg_image[:] = bg_color
    com = alpha * fg + (1 - alpha) * bg_image
    com = com.astype('uint8')
    output = cv2.cvtColor(com, cv2.COLOR_BGR2RGB)

    return Image.fromarray(output).convert('RGB')

def default_bg(img: str) -> Image.Image:
    output = cv2.cvtColor(readb64(img), cv2.COLOR_BGR2RGB)
    return Image.fromarray(output).convert('RGB')

def process(img: str) -> Tuple[np.ndarray, np.ndarray]:
    paddle.set_device('cpu')
    cfg = Config('./config/ppmattingv2-stdc1-human_512.yml')
    in_img = readb64(img)
    model = cfg.model
    transforms = Compose(cfg.val_transforms)

    alpha, fg = predict(
        model,
        model_path='./config/ppmattingv2-stdc1-human_512.pdparams',
        transforms=transforms,
        image_list=[in_img],
        )
    
    alpha = alpha / 255.0
    alpha = alpha[:, :, np.newaxis]

    return (alpha, fg)