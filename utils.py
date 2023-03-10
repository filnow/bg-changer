import cv2
import base64
import numpy as np
import io
from PIL import Image

def readb64(uri: str) -> np.ndarray:
   encoded_data = uri.split(',')[1]
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def str_to_io(img: Image.Image) -> io.BytesIO:
   img_io = io.BytesIO()
   img.save(img_io, 'PNG')
   img_io.seek(0)
   return img_io

def b64_image(image_filename: str) -> str:
   with open(image_filename, 'rb') as f:
      image = f.read()
   return 'data:image/jpg;base64,' + base64.b64encode(image).decode('utf-8')