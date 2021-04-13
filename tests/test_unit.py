from ocr import image_preprocess_factory
import numpy as np
from main import encode
IMAGE_SIZE = 512
PIXEL_MAX = 255
IMAGE_PATH = "./dataset/image"

def test_binarise():
  image = np.random.randint(PIXEL_MAX, size=(IMAGE_SIZE, IMAGE_SIZE)).astype('uint8')
  assert (image >= 0).all() and (image <= PIXEL_MAX).all()
  binarized_image = image_preprocess_factory.binarise(image)
  assert not ((binarized_image > 0).all() and (binarized_image < PIXEL_MAX).all())

def test_encode():
  filenames = glob(''.join([IMAGE_PATH, '/*/*.png']))
  filenames.sort()
  image = cv.imread(choice(filenames))
  image_raw = encode(image)
  assert all(chars in string.hexdigits for chars in image_raw)
