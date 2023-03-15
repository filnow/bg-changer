import os
import cv2
import numpy as np
import paddle
from paddleseg.cvlibs import Config
from paddleseg.transforms import Compose

from ppmatting.core import predict

def main():
    paddle.set_device('cpu')

    cfg = Config('ppmattingv2-stdc1-human_512.yml')
    image_path = '/home/filnow/fun/bg-changer/assets/test.jpg'
    save_dir = './output/result/'

    model = cfg.model
    transforms = Compose(cfg.val_transforms)

    alpha, fg = predict(
        model,
        model_path='ppmattingv2-stdc1-human_512.pdparams',
        transforms=transforms,
        image_list=[image_path],
        save_dir=save_dir,
        )

    img_ori = cv2.imread(image_path)
    bg = get_bg('/home/filnow/fun/bg-changer/assets/city.jpg', img_ori.shape)
    alpha = alpha / 255.0
    alpha = alpha[:, :, np.newaxis]
    com = alpha * fg + (1 - alpha) * bg
    com = com.astype('uint8')
    com_save_path = os.path.join(save_dir,
                                 os.path.basename(image_path))
    cv2.imwrite(com_save_path, com)


def get_bg(background, img_shape):
    bg = np.zeros(img_shape)
    if background == 'r':
        bg[:, :, 2] = 255
    elif background is None or background == 'g':
        bg[:, :, 1] = 255
    elif background == 'b':
        bg[:, :, 0] = 255
    elif background == 'w':
        bg[:, :, :] = 255

    else:
        bg = cv2.imread(background)
        bg = cv2.resize(bg, (img_shape[1], img_shape[0]))
    return bg


if __name__ == "__main__":
    main()
