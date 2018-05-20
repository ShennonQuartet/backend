import os
import random
import numpy as np
from itertools import cycle
from keras.preprocessing import image

IMAGES_PATH = os.environ.get('IMAGES_PATH', 'images')

IMAGES_CYCLE = cycle(os.listdir(IMAGES_PATH))

def get_image(img_path):
    img_name = next(IMAGES_CYCLE)
    return os.path.join(img_path, img_name)


def get_verification(clf, img_dir, api_url):
    verification = {}
    img = get_image(img_dir)
    verification['image_url'] = api_url + img

    img = image.load_img(img, target_size=(150, 150))
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    verification['verdict'] = int(clf.predict_classes([x])[0][0])
    return verification