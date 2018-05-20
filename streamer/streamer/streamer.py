import os
import asyncio
import websockets
import json
import logging
import pandas as pd
from model import load_df, load_model, get_prediction_for_dt


PERIOD = os.environ.get('PERIOD', 10)
COLUMNS = os.environ.get('COLUMNS', 'date,RF.21304.Ток...213MII904A').split(',')
ENCODING = os.environ.get('ENCODING', 'utf-8')


def preprocess_df(df):
    df = df.fillna(0)
    df = df[COLUMNS]
    logging.info(df.head())
    return df

fulldf = load_df()
logging.info(fulldf.head())
streamdf = preprocess_df(fulldf)
logging.info(streamdf.head())

model = load_model()


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
            print('pub', i)
            for websocket in SUBSCRIBERS:
                logging.info(f'{str(websocket.remote_address)} notified')
                try:
                    row['prediction'] = round(get_prediction_for_dt(fulldf, model, row['date']), 6)
                    print(row_to_dict(row, streamdf.columns))
                    cols = list(streamdf.columns) + ['prediction']
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
