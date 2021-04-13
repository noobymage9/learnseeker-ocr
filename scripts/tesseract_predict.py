from os.path import join
from os import mkdir
from glob import glob
import cv2 as cv
import pytesseract

DUMP_PATH = './assets/recognitions/tesseract'
IMAGE_PATH = "./assets/phrases"
mkdir(DUMP_PATH)

filenames = glob(''.join([IMAGE_PATH, '/*.png']))
filenames.sort()
for file_name in filenames:
    image = cv.imread(file_name, cv.IMREAD_GRAYSCALE)
    output = f'{DUMP_PATH}/{file_name.split("/")[-1][:-4]}.txt'
    with open(output, 'w') as file:
      print(f'Writing to {output}')
      file.write(pytesseract.image_to_string(image))