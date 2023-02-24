import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

IMAGE_FILES = ['./static/images/photo1.jpg']
BG_IMAGE = './static/images/bg.jpg'
BG_COLOR = (192, 192, 192) # gray
MASK_COLOR = (255, 255, 255) # white

def change_bg(image, bg_image):
 
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            bg_image = cv2.imread(BG_IMAGE)

            results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            resized = cv2.resize(bg_image, (image.shape[1], image.shape[0]), interpolation = cv2.INTER_AREA)

            output_image = np.where(condition, image, resized)
            
            cv2.imwrite('./output/' + str(idx) + 'change.png', output_image)

def remove_bg(image, bg_color):
        
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = bg_color

            output_image = cv2.cvtColor(np.where(condition, image, bg_image), cv2.COLOR_BGR2RGB)
            
            #cv2.imwrite('./output/' + str(idx) + 'remove.png', output_image)

    return output_image

if __name__ == '__main__':
    
    change_bg(IMAGE_FILES, BG_IMAGE)
    remove_bg(IMAGE_FILES, BG_COLOR)