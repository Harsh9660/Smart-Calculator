import pandas as pd
from sklearn.linear_model import LinearRegression
import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_CURRENT_DIR, "data.csv")

class ExpensePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def train_model(self):
        """Trains the model using historical data from data.csv."""
        try:
            if not os.path.exists(_DATA_PATH):
                df = pd.DataFrame({'month': [1], 'expense': [1000]})
                df.to_csv(_DATA_PATH, index=False)
            
            data = pd.read_csv(_DATA_PATH)
            
            if data.empty or len(data) < 2:
                self.is_trained = False
                return

            X = data[['month']]       
            y = data['expense']       

            self.model.fit(X, y)
            self.is_trained = True
        except Exception as e:
            print(f"Error training model: {e}")
            self.is_trained = False

    def predict(self, month):
        """Predicts expense for a given month index."""
        if not self.is_trained:
            self.train_model()
            
        if not self.is_trained:
            return 0.0
            
        X_predict = pd.DataFrame([[month]], columns=['month'])
        prediction = self.model.predict(X_predict)
        return max(0, float(prediction[0]))
