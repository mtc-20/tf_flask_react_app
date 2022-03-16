from flask import Flask, render_template, request
import os
from reverseProxy import proxRequest
from classifier import classifyImage


MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'

print(MODE)
app = Flask(__name__)

# Ignore static folder in dev mode
if MODE == 'development':
    print("[dev]")
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

