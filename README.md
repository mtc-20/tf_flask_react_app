# TF Web app 

** An image classification web app using TF(inference), React(frontend) and Flask(backend) based on this [Medium article](https://medium.com/sopra-steria-norge/build-a-simple-image-classification-app-using-react-keras-and-flask-7b9075e3b6f5)). Decided to try this since they had a working web app running on Heroku, which is what my end goal was.**



However, couldn't get this to work even locally. Weirdly, it did only after adding a GET request check - if anyone can explain that to me, would be nice :sweat:



Still need to learn how react and flask communicate, I think there is something wrong with the urls/requests, but no clue how to debug...

Tips to deploy on Heroku
- Use `tensorflow-cpu` in the requirements - keeps slug size within limits[<sup>1</sup>][1]
- Make sure `Procfile` and `requirements.txt` are in root folder

[1]: https://stackoverflow.com/questions/61062303/deploy-python-app-to-heroku-slug-size-too-large