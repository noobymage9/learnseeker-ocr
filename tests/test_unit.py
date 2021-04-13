from ocr import image_preprocess_factory
import numpy as np
IMAGE_SIZE = 512
PIXEL_MAX = 255

def test_binarise():
  image = np.random.randint(PIXEL_MAX, size=(IMAGE_SIZE, IMAGE_SIZE)).astype('uint8')
  assert (image >= 0).all() and (image <= PIXEL_MAX).all()
  binarized_image = image_preprocess_factory.binarise(image)
  assert not ((binarized_image > 0).all() and (binarized_image < PIXEL_MAX).all())