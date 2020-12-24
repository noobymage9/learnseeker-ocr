from flask import Flask, render_template, request, jsonify
from base64 import b64decode, b64encode
from os import environ
from image_preprocess_factory import preprocess
import numpy as np
import cv2 as cv
app = Flask("main")

# # Method 1
# @app.route('/left_most_scan')
# def left_most_scan():
# 	return render_template('left_most_scan')

# Method 4
@app.route('/manual_bound')
def user_select():
	return render_template('manual_bound.html', url=environ.get("SERVER_URL"))

# Image Preprocessing
@app.route('/image_preprocess', methods=['POST'])
def image_preprocess():
	data = {}
	for idx, image_data_pack in enumerate(request.json['images']):
		image_data = image_data_pack.split(',')[1]
		image_bytes = b64decode(image_data)
		image = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
		preprocessed_image = preprocess(image)
		_, buffer = cv.imencode(".png", preprocessed_image)

		data[idx] = b64encode(buffer).decode('utf-8')


	return jsonify(data)