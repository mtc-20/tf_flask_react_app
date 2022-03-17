# TF Web app 

**An image classification web app using TF(inference), React(frontend) and Flask(backend) based on this [([Medium article]](https://medium.com/sopra-steria-norge/build-a-simple-image-classification-app-using-react-keras-and-flask-7b9075e3b6f5)). Decided to try this since they had a working web app running on Heroku, which is what my end goal was.**



However, couldn't get this to work locally just from the post. Weirdly, it **did work** only after adding a `GET` request check - if anyone can explain that to me, would be nice :sweat:



Still need to learn how react and flask communicate, I think there was something wrong with the urls/requests, but no clue how to debug...

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
The model used is an image classification model trained on the FashionMNIST dataset using a simple CNN. The model training notebook can be found [here](https://github.com/mtc-20/Machine_learning_projects/blob/MTC/Fashion_classification/Fashion_classification.ipynb).


Next will try to switch to a more meaningful model.
