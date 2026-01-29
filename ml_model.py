import pandas as pd
from sklearn.linear_model import LinearRegression

class ExpensePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train_model(self):
        data = pd.read_csv("data.csv")
        X = data[['month']]       
        y = data['expense']       

        self.model.fit(X, y)

    def predict(self, month):
        prediction = self.model.predict([[month]])
        return prediction[0]
