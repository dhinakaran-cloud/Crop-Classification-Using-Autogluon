

import pickle
from autogluon.tabular import TabularPredictor


model_file = 'autogluon_model.pkl'
with open(model_file, 'rb') as f:
    predictor = pickle.load(f)

def predict(input_data):
    predictions = predictor.predict(input_data)
    return predictions
