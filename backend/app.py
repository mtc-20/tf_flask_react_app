from flask import Flask, render_template, request, send_file
import os
# from backend.detector import overlayImage
from reverseProxy import proxRequest
from classifier import classifyImage
from detector_lite import overlayImage

MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'


app = Flask(__name__)

# Ignore static folder in dev mode
if MODE == 'development':
	app = Flask(__name__, static_folder=None)

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
	if MODE == 'development':
		return proxRequest(DEV_SERVER_URL, path)
	else:
		return render_template('index.html')
		# return "Hello from Flask"

@app.route('/classify', methods=['GET','POST'])
def classify():
	if request.method == 'GET':
		return "Hello classifier"
	else:
		if(request.files['image']):
			file_got = request.files['image']

			result = classifyImage(file_got)
			print("Model classsification: " + result)
			return result

@app.route('/detect', methods=['GET','POST'])
def detect():
	if request.method == 'GET':
		return "Hello detector"
	else:
		if(request.files['image']):
			file_got = request.files['image']

			overlay = overlayImage(file_got)
			return send_file(overlay, mimetype='image/png')

