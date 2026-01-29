import pandas as pd
from sklearn.linear_model import LinearRegression
import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_CURRENT_DIR, "data.csv")

class ExpensePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train_model(self):
        try:
            data = pd.read_csv(_DATA_PATH)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Error: The data file 'data.csv' was not found. It should be in the project root: {_CURRENT_DIR}"
            )
        X = data[['month']]       
        y = data['expense']       

        self.model.fit(X, y)

    def predict(self, month):
        prediction = self.model.predict([[month]])
        return prediction[0]
