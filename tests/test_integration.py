import pytest
from unittest import TestCase
import sys, os
import json
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from main import app, encode
from glob import glob
from random import choice
import cv2 as cv

IMAGE_PATH = "./asset/images"
PHRASE_PATH = "./assets/phrases"

class IntegrationTest(TestCase):

  # Assert GET /manual_bound exist
  def test_manual_bound(self):
    ''' GET Manual Bound Page '''
    tester = app.test_client(self)
    response = tester.get('/manual_bound', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  # Assert GET /auto_bound exist
  def test_auto_bound(self):
    ''' GET Auto Bound Page '''
    tester = app.test_client(self)
    response = tester.get('/auto_bound', content_type='html/text')
    self.assertEqual(response.status_code, 200)


  def test_manual_bound_image_preprocess(self):
    ''' POST Manual Bound Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image)}']
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) == 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) == 0
    
    assert 'images' in result
    assert len(result.get('images')) == 1

  def test_manual_bound_multiple_image_preprocess(self):
    ''' POST Manual Bound Multiple Images Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image_1 = cv.imread(choice(filenames))
    image_2 = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image_1)}', f'data:image/png;base64,{encode(image_2)}']
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) == 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) == 0
    
    assert 'images' in result
    assert len(result.get('images')) == 2
    
  def test_auto_bound_left_detect_image_preprocess(self):
    ''' POST Auto Bound Left Detect Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image)}'],
      'zone_type': 'LEFT_DETECT'
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) > 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) > 0
    
    assert 'images' in result
    assert len(result.get('images')) == 1

  def test_auto_bound_multiple_left_detect_image_preprocess(self):
    ''' POST Auto Bound Multiple Images Left Detect Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image_1 = cv.imread(choice(filenames))
    image_2 = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image_1)}', f'data:image/png;base64,{encode(image_2)}'],
      'zone_type': 'LEFT_DETECT'
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) > 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) > 0
    
    assert 'images' in result
    assert len(result.get('images')) == 2

  def test_auto_bound_grow_image_preprocess(self):
    ''' POST Auto Bound Grow Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image)}'],
      'zone_type': 'GROW'
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) > 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) > 0
    
    assert 'images' in result
    assert len(result.get('images')) == 1
    
    assert 'texts' in result
    assert len(result.get('texts')) > 0

  def test_auto_bound_multiple_grow_image_preprocess(self):
    ''' POST Auto Bound Multiple Images Grow Image Preprocess '''
    tester = app.test_client(self)
    filenames = glob(''.join([IMAGE_PATH, '/*.png']))
    filenames.sort()
    image_1 = cv.imread(choice(filenames))
    image_2 = cv.imread(choice(filenames))

    response = tester.post('/image_preprocess', json={
      'images': [f'data:image/png;base64,{encode(image_1)}', f'data:image/png;base64,{encode(image_2)}'],
      'zone_type': 'GROW'
    })
    result = response.get_json()

    assert 'cropped_areas' in result
    assert 'areas' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('areas')) > 0
    assert 'size' in result.get('cropped_areas')
    assert len(result.get('cropped_areas').get('size')) > 0
    
    assert 'images' in result
    assert len(result.get('images')) == 2
    
    assert 'texts' in result
    assert len(result.get('texts')) > 0

  def test_text_recognise(self):
    ''' POST Text Recognise '''
    tester = app.test_client(self)
    filenames = glob(''.join([PHRASE_PATH, '/*.png']))
    filenames.sort()
    image = cv.imread(choice(filenames))

    response = tester.post('/text_recognise', json={
      'images': [f'data:image/png;base64,{encode(image)}'],
    })
    result = response.get_json()

    assert 'texts' in result
    assert len(result.get('texts')) == 1

  def test_text_recognise_multiple(self):
    ''' Post Text Recognise Multiple Images '''
    tester = app.test_client(self)
    filenames = glob(''.join([PHRASE_PATH, '/*.png']))
    filenames.sort()
    image_1 = cv.imread(choice(filenames))
    image_2 = cv.imread(choice(filenames))

    response = tester.post('/text_recognise', json={
      'images': [f'data:image/png;base64,{encode(image_1)}', f'data:image/png;base64,{encode(image_2)}'],
    })
    result = response.get_json()
    
    assert 'texts' in result
    assert len(result.get('texts')) == 2