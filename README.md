# TF Web app 

**An image classification web app using [`TF2.x`](https://www.tensorflow.org/)(inference), `React`(frontend) and `Flask`(backend) based on this [Medium article](https://medium.com/sopra-steria-norge/build-a-simple-image-classification-app-using-react-keras-and-flask-7b9075e3b6f5)). Decided to try this since they had a working web app running on Heroku, which is what my end goal was.**



However, couldn't get this to work locally just from the post intructions. Weirdly, it did only after adding a GET request check - if anyone can explain that to me, would be nice :sweat:



Still need to learn how react and flask communicate, I think there is something wrong with the urls/requests, but no clue how to debug...

## Tips to deploy on Heroku
- Use `tensorflow-cpu` in the requirements - keeps slug size within limits[<sup>1</sup>][1]
  - tf2.6 has some weird bug with keras dependency, so make sure to add `keras` version to `requirements` if using
- Make sure `Procfile` and `requirements.txt` are in root folder
- Make sure you have all buildpacks specified(accesible from Settings) - in this case `heroku/python` and `heroku/nodejs`
- Remember to set the host to `0.0.0.0` and the port to `PORT` since these are both generated by heroku

[1]: https://stackoverflow.com/questions/61062303/deploy-python-app-to-heroku-slug-size-too-large