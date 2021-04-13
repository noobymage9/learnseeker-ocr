from ocr import image_preprocess_factory
import numpy as np
from main import encode
from glob import glob
import cv2 as cv
from random import choice
from string import hexdigits
from base64 import b64decode

IMAGE_SIZE = 512
PIXEL_MAX = 255
IMAGE_PATH = "./assets/images"

def test_binarise():
  ''' Text Binarise '''
  image = np.random.randint(PIXEL_MAX, size=(IMAGE_SIZE, IMAGE_SIZE)).astype('uint8')
  assert (image >= 0).all() and (image <= PIXEL_MAX).all()
  binarized_image = image_preprocess_factory.binarise(image)
  assert not ((binarized_image > 0).all() and (binarized_image < PIXEL_MAX).all())

def test_encode():
  ''' Image Encode '''
  filenames = glob(''.join([IMAGE_PATH, '/*.png']))
  filenames.sort()
  image = cv.imread(choice(filenames))
  image_raw = encode(image)
  try:
   _ = b64decode(image_raw)
  except Exception:
    assert False