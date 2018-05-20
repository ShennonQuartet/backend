import os
import random
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image


def load_verification_model(model_file):
    # load json and create model
    with open(model_file + '.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_file + '.h5')
    return loaded_model


def get_image(img_path):
    img_names = os.listdir(img_path)
    img_name = random.choice(img_names)
    return os.path.join(img_path, img_name)


def get_verification(clf, img_path, api_url):
    verification = {}
    verification['image']= get_image(img_path)
    verification['image_url']= api_url + verification['image']

    img = image.load_img(verification['image'], target_size=(150, 150))
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    verification['verdict'] = int(clf.predict_classes([x])[0][0])

    return verification