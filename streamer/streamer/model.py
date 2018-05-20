import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pickle


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


def load_df(fpath, encoding):
    def parse_dt(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    df = pd.read_csv(fpath, encoding=encoding)
    df = df.fillna(0)
    df['date'] = df['date'].apply(parse_dt)

    return df


def load_model(fpath):
    mdl = None
    with open(fpath, 'rb') as fin:
        mdl = pickle.load(fin)
    return mdl


def get_prediction_for_dt(df, model, dt):
    features = get_features_for_dt(df, dt)
    return model.predict([features])[0]

