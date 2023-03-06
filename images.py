import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

def change_bg(image, bg_image):
 
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:

        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        resized = cv2.resize(bg_image, (image.shape[1], image.shape[0]), interpolation = cv2.INTER_AREA)

        output_image = cv2.cvtColor(np.where(condition, image, resized), cv2.COLOR_BGR2RGB)
            
    return output_image

def remove_bg(image, bg_color):
        
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
       
        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = bg_color

        output_image = cv2.cvtColor(np.where(condition, image, bg_image), cv2.COLOR_BGR2RGB)

    return output_image

    