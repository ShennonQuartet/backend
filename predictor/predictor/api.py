from apistar import App, Route, http, types, validators
from model import load_df, load_model, get_prediction_for_dt

df = load_df()
model = load_model()

def echo_query_params(query_params: http.QueryParams) -> dict:
    return dict(query_params)


class PredictionRequest(types.Type):
    datetime = validators.DateTime()


def get_prediction(datetime):
    request = PredictionRequest({'datetime': datetime})
    datetime = request.datetime
    return get_prediction_for_dt(df, model, datetime)


def get_confirmation(datetime):
    pass


routes = [
    Route('/', method='GET', handler=echo_query_params),
    Route('/predict', method='GET', handler=get_prediction),
    Route('/confirm', method='GET', handler=get_confirmation),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('0.0.0.0', 5000, debug=True)