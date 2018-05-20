import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pickle

DATASET_PATH = os.environ.get('DATASET_PATH', 'dataset.csv')
DATASET_ENCODING = os.environ.get('DATASET_ENCODING', 'utf-8')
MODEL_FILE = os.environ.get('MODEL_FILE', 'model.pkl')


def make_features(df):
    vecs = []
    columns = df.columns[df.columns != 'date']
    for period in [1, 5, 10, 20, 30, 100, 360]:
        mean = df[-period:][columns].mean(axis=0).values
        min = df[-period:][columns].min(axis=0).values
        max = df[-period:][columns].max(axis=0).values
        std = df[-period:][columns].std(axis=0).values
        median = df[-period:][columns].median(axis=0).values
        feats = np.hstack([mean, min, max, std, median])
        vecs.append(feats)

    return np.hstack(vecs)


def make_range(df, stop_dt):
    return (df['date'] >= (stop_dt - timedelta(hours=1))) & (df['date'] < stop_dt)


def get_features_for_dt(df, dt):
    rng = df[make_range(df, dt)]
    feature_vector = make_features(rng)
    return feature_vector


def load_df():
    def parse_dt(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    df = pd.read_csv(DATASET_PATH, encoding=DATASET_ENCODING)
    df = df.fillna(0)
    df['date'] = df['date'].apply(parse_dt)

    return df


def load_model():
    mdl = None
    with open(MODEL_FILE, 'rb') as fin:
        mdl = pickle.load(fin)
    return mdl


def get_prediction_for_dt(df, model, dt):
    features = get_features_for_dt(df, dt)
    return model.predict([features])[0]

