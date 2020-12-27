from flask import Flask, render_template, request, jsonify
from base64 import b64decode, b64encode
from os import environ
from image_preprocess_factory import preprocess, zone
import numpy as np
import cv2 as cv
app = Flask(__name__)


# Method 1
@app.route('/auto_bound')
def auto_bound():
	return render_template('auto_bound.html', url=environ.get("SERVER_URL"))

# Method 4
@app.route('/manual_bound')
def user_select():
	return render_template('manual_bound.html', url=environ.get("SERVER_URL"))

# Image Preprocessing
@app.route('/image_preprocess', methods=['POST'])
def image_preprocess():
	data = {
		'images': [],
		'cropped_areas': {
			'areas': [],
			'size': []
		},
	}
	for idx, image_data_pack in enumerate(request.json['images']):
		image_data = image_data_pack.split(',')[1]
		image_bytes = b64decode(image_data)
		image = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
		preprocessed_image = preprocess(image)
		data['images'].append(encode(image = preprocessed_image))
		if 'zone_type' in request.json:
			croppedAreas = zone(preprocessed_image, request.json['zone_type'])
			data['cropped_areas']['areas'].append(encode(images = croppedAreas))
			data['cropped_areas']['size'].append(list(map(lambda area: [(area.shape[1] / image.shape[1]) * 600, (area.shape[0] / image.shape[0]) * 800], croppedAreas)))
	return jsonify(data)

def encode(image = [], images = []):
	if len(image) != 0:
		_, buffer = cv.imencode(".png", image)
		return b64encode(buffer).decode('utf-8')
	elif len(images) != 0:
		temp = []
		for image in images:
			if len(image) > 5:
				_, buffer = cv.imencode(".png", image)
				temp.append(b64encode(buffer).decode('utf-8'))
		return temp
	else:
		return None

if __name__ == "__main__":
  app.run(host='0.0.0.0')