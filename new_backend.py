import argparse
import os
import sys

import cv2
import numpy as np
import paddle
from paddleseg.cvlibs import manager, Config
from paddleseg.utils import get_sys_env, logger
from paddleseg.core import predict
from paddleseg.transforms import Compose


paddle.set_device('cpu')

cfg = Config(path='./pretrained/ppmattingv2-stdc1-human_512.yml')

model = cfg.model
transform = Compose(cfg.transforms)

fg = predict(
    model,
    model_path='./pretrained_model/ppmattingv2-stdc1-human_512.pdparams',
    transforms=transform,
    image_list=['./assets/test3.jpg'],
    save_dir='./output',
)

print(fg)