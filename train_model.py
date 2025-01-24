import pandas as pd
from autogluon.tabular import TabularPredictor
import pickle

file_path = "C:/Users/hp/Downloads/Crop_recommendation.csv"
df = pd.read_csv(file_path)


if 'label_num' in df.columns:
    df = df.drop(columns=['label_num'])


label_column = 'label'
X = df.drop(columns=[label_column])
y = df[label_column]


predictor = TabularPredictor(label=label_column).fit(train_data=df)


model_file = 'autogluon_model.pkl'
with open(model_file, 'wb') as f:
    pickle.dump(predictor, f)

print(f"AutoGluon model saved successfully to {model_file}")
