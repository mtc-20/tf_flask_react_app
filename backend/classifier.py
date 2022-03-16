from cProfile import label
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from numpy import argmax
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageFile

model = load_model("../backend/fashion_cnn_e10")
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# print(model.output)
def getPredictions(image_file, model):
    img_input = Image.open(image_file)
    img_input = img_input.convert('L')
    img_input = img_input.resize((28,28), Image.NEAREST)

    numpy_img = image.img_to_array(img_input)
    numpy_img = numpy_img/255
    numpy_img= numpy_img.reshape(1,28,28,1)
    preds = model.predict(numpy_img)

    return preds

def classifyImage(image_file):
    preds = getPredictions(image_file, model)
    label = argmax(preds, axis=-1)[0]
    return class_names[label]

