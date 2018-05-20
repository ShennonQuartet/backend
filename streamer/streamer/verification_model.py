import os
import random


def get_image(img_path):
    img_names = os.listdir(img_path)
    img_name = random.choice(img_names)
    return os.path.join(img_path, img_name)


def get_verification(clf, img_path, api_url):
    verification = {}
    verification['image']= get_image(img_path)
    verification['image_url']= api_url + verification['image']
    #with open(verification['image'], 'rb') as f:
    #    verification['verdict'] = clf.predict(f.read())
    return verification