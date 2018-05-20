import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from keras.models import model_from_json


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
    pred_base = df[df.date < pd.Timestamp(dt)].tail(1000) # choose last 1000 observations
    pred_base = pred_base.iloc[:,1:] # delete date column
    pred_base = (pred_base - pred_base.mean()) / (pred_base.max() - pred_base.min()) # normalize data
    X = pred_base.values # return numpy array of values
    return X.reshape(1, 1000, 43)


def load_df(fpath, encoding):
    def parse_dt(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    df = pd.read_csv(fpath, encoding=encoding)
    df = df.fillna(0)
    df['date'] = df['date'].apply(parse_dt)

    return df


def load_model(model_file):
    # load json and create model
    with open(model_file + '.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_file + '.h5')
    return loaded_model


def norm(x, min_, max_):
    return (x - min_) / (max_ - min_)


def get_prediction_for_dt(df, model, dt):
    features = get_features_for_dt(df, dt)
    prediction = model.predict([features]).reshape(99)
    prediction = prediction[~np.isnan(prediction)][-1]
    return norm(prediction, 0, 0.05)
