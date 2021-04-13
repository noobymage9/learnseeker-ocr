from flask import Flask, render_template, request, jsonify, redirect, url_for
from os import environ, makedirs
from ocr import image_preprocess_factory
from utilities import spell_check, encode, decode
import numpy as np
import cv2 as cv
import pytesseract
from PIL import Image
from uuid import uuid4
app = Flask(__name__)

CAPTURE_PHRASE = environ.get('CAPTURE_PHRASE') == 'True'

@app.route('/home')
def home():
	return render_template('home.html', url=request.url_root)

# Method 1
@app.route('/auto_bound')
def auto_bound():
	return render_template('auto_bound.html', url=request.url_root)

# Method 4
@app.route('/manual_bound')
def user_select():
	return render_template('manual_bound.html', url=request.url_root)

# Image Preprocessing
@app.route('/image_preprocess', methods=['POST'])
def image_preprocess():
	data = {
		'texts': [],
		'images': [],
		'cropped_areas': {
			'areas': [],
			'size': []
		},
	}
	for idx, image_data_pack in enumerate(request.json['images']):
		image_data = image_data_pack.split(',')[1]
		image = decode(image_data)
		preprocessed_image = image_preprocess_factory.preprocess(image)
		data['images'].append(encode(image = preprocessed_image))
		# if auto bound
		if 'zone_type' in request.json:
			cropped_areas = image_preprocess_factory.zone(preprocessed_image, request.json['zone_type'])
			for idx, cropped_area in enumerate(cropped_areas):
				data["texts"].append(pytesseract.image_to_string(cropped_area))

			# spell_check(data['texts'])
			data['cropped_areas']['areas'].append(encode(images = cropped_areas))
			data['cropped_areas']['size'].append(list(map(lambda area: [(area.shape[1] / image.shape[1]) * 600, (area.shape[0] / image.shape[0]) * 800], cropped_areas)))
 
	return jsonify(data)

@app.route('/text_recognise', methods=['POST'])
def text_recognise():
	data = {
		'texts': [],
	}
	for idx, image_data_pack in enumerate(request.json['images']):
		image_data = image_data_pack.split(',')[1]
		image = decode(image_data)
		data["texts"].append(pytesseract.image_to_string(image))

		if CAPTURE_PHRASE:
			makedirs('./assets/phrases', exist_ok=True)
			word_image = image
			word_image = Image.fromarray(word_image)
			word_image.save(''.join(['./assets/phrases', '/', f'{uuid4().hex}.png']), 'PNG')

	# spell_check(data['texts'])
	return jsonify(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def other(path):
    return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(host='0.0.0.0')