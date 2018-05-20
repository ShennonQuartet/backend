import os
import asyncio
import websockets
import json
import logging
from model import load_df, load_model, get_prediction_for_dt
from verification_model import get_verification


PERIOD = int(os.environ.get('PERIOD', 10))
COLUMNS = os.environ.get('COLUMNS', 'date,RF.21304.Ток...213MII904A').split(',')


DATASET_PATH = os.environ.get('DATASET_PATH', 'dataset.csv')
DATASET_ENCODING = os.environ.get('DATASET_ENCODING', 'utf-8')
PREDICTION_MODEL_NAME = os.environ.get('PREDICTION_MODEL_NAME', 'Predictions')
VERIFICATION_MODEL_NAME = os.environ.get('VERIFICATION_MODEL_NAME', 'model1')

IMAGES_PATH = os.environ.get('IMAGES_PATH', 'images')
API_URL = os.environ.get("API_URL", 'localhost:8000/static/')

SKIP_ROWS = int(os.environ.get("SKIP_ROWS", 2000))


def preprocess_streamdf(df):
    df = df.fillna(0)
    df = df[COLUMNS]
    logging.info(df.head())
    return df


fulldf = load_df(DATASET_PATH, DATASET_ENCODING)
logging.info(fulldf.head())
streamdf = preprocess_streamdf(fulldf)
logging.info(streamdf.head())

prediction_model = load_model(PREDICTION_MODEL_NAME)
verif_model = load_model(VERIFICATION_MODEL_NAME)


def row_to_dict(row, columns):
    data = {}
    for i, colname in enumerate(columns):
        try:
            json.dumps(row[i])
            data[colname] = row[i]
        except TypeError:
            data[colname] = str(row[i])
    return data


SUBSCRIBERS = set()


async def sub(websocket, path):
    SUBSCRIBERS.add(websocket)
    print(f'Subscribed {websocket.remote_address}')
    try:
        async for msg in websocket:
            pass
    except websockets.ConnectionClosed:
        SUBSCRIBERS.remove(websocket)
        print(f'Unsubscribed {websocket.remote_address}')


async def pub():
    while True:
        for i, row in streamdf.iterrows():
            if i < SKIP_ROWS:
                continue
            print('pub', i)
            for websocket in SUBSCRIBERS:
                logging.info(f'{str(websocket.remote_address)} notified')
                try:
                    row['prediction'] = round(get_prediction_for_dt(fulldf, prediction_model, row['date']), 6)
                    row['verification'] = get_verification(verif_model, IMAGES_PATH, API_URL)
                    print(f'Prediction: {row["prediction"]}, Verification: {row["verification"]}')
                    cols = list(streamdf.columns) + ['prediction', 'verification']
                    row_json = json.dumps(row_to_dict(row, cols))
                    logging.debug(
                        f'to {str(websocket.remote_address)} send: {row_json}')
                    await websocket.send(row_json)
                except websockets.exceptions.ConnectionClosed:
                    websocket.remove(websocket)
                    print(f'Unsubscribed {websocket.remote_addr}')
            await asyncio.sleep(PERIOD)


loop = asyncio.get_event_loop()
start_server = websockets.serve(sub, '0.0.0.0', 5678)
print('starting server')
loop.run_until_complete(start_server)
print('starting publishing')
asyncio.async(pub())
loop.run_forever()
