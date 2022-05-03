# TF Web app 

**An object detection web app using TF(inference), React(frontend) and Flask(backend) that runs inference on camera feed. Based on this [Medium article](https://medium.com/sopra-steria-norge/build-a-simple-image-classification-app-using-react-keras-and-flask-7b9075e3b6f5)).** 

This app has been tested only for local deployment so far. It works but takes around 3s per detection on my system.



**v0.1 notes:**

-    Originally, decided to try the tutorial since they had a working web app running on Heroku, which is what my end goal was. However, couldn't get it to work locally just from the post. Weirdly, it **did work** only after adding a `GET` request check - if anyone can explain that to me, would be nice :sweat:


    Still need to learn how react and flask communicate, I think there was something wrong 
    with the urls/requests, but no clue how to debug...

## Getting started
Would be a good idea to create a virtual environment. I used `conda` for this containing Python 3.9 and Tensorflow 2.6.

The backend is handled by Python and the requirements are in `backend` folder
```bash
cd backend
pip install -r requirments.txt
```

Node handles frontend stuff and the requirements are in `frontend` folder
```bash
cd frontend
npm install
```
To run locally
```bash
cd frontend
npm run start:server-dev
```
## Model
The model used is a [Mobilenetv2 SSD](https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2) trained on the COCO2017 dataset.

