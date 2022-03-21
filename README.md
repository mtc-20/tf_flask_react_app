# TF Web app 

**An image classification web app using [`TF2.x`](https://www.tensorflow.org/)(inference), `React`(frontend) and `Flask`(backend) based on this [Medium article](https://medium.com/sopra-steria-norge/build-a-simple-image-classification-app-using-react-keras-and-flask-7b9075e3b6f5)). Decided to try this since they had a working web app running on Heroku, which is what my end goal was.**

**v0.2 notes**:

- Seem to run into memory error with Heroku
    
    >[web.1]: Process running mem=1189M(232.4%)
    >
    >[web.1]: Error R15 (Memory quota vastly exceeded)

- Have got it down to 152% with a smaller model and some `gc`

    > [web.1]: Process running mem=783M(152.2%)
    > 
    >[web.1]: Error R14 (Memory quota exceeded)
- Got it down to 102% and less with `tflite`, however now run into `interpreter` internal buffer issues



**v0.1 notes**:


    It was even harder to get it working on Heroku, atleast its deployed now 🙂!

## Tips for deploying on Heroku
- Use `tensorflow-cpu` in the requirements - keeps slug size within limits[<sup>1</sup>][1]
  - tf2.6 has some weird bug with keras dependency, so make sure to add `keras` version to `requirements` if using
- Make sure `Procfile` and `requirements.txt` are in root folder
- Make sure you have all buildpacks specified(accesible from Settings) - in this case `heroku/python` and `heroku/nodejs`
- Remember to set the host to `0.0.0.0` and the port to `PORT` since these are both generated by heroku
- Memory usage needs to be limited to 512MB

[1]: https://stackoverflow.com/questions/61062303/deploy-python-app-to-heroku-slug-size-too-large
