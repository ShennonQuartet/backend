import os
import asyncio
import websockets
import json
import logging
import pandas as pd

PERIOD = os.environ.get('PERIOD', 10)
FILE_PATH = os.environ.get('FILE_PATH', 'data.csv')
COLUMNS = os.environ.get('COLUMNS', 'date,RF.21304.Ток...213MII904A').split(',')
ENCODING = os.environ.get('ENCODING', 'utf-8')


def preprocess_df(df):
    df = df.fillna(0)
    df = df[COLUMNS]
    logging.info(df.head())
    return df


df = None
if '.csv' in FILE_PATH:
    df = pd.read_csv(FILE_PATH, encoding=ENCODING)
elif 'h5' in FILE_PATH:
    df = pd.read_hdf(FILE_PATH)
logging.info(df.head())
df = preprocess_df(df)


def row_to_dict(row, columns):
    data = dict([
        (colname, row[i])
        for i, colname in enumerate(columns)
    ])
    return data


async def stream_data(websocket, path):
    while True:
        for i, row in df.iterrows():
            row_json = json.dumps(row_to_dict(row, df.columns))
            logging.debug(f'to {str(websocket.remote_address)} send: {row_json}')
            await websocket.send(row_json)
            await asyncio.sleep(PERIOD)


start_server = websockets.serve(stream_data, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
