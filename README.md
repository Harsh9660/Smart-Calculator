# Smart Calculator with Machine Learning

## Project Overview
A web-based "Smart Calculator" built with Python and Streamlit. This application performs standard arithmetic operations and provides financial forecasting by using a Linear Regression model to predict future expenses. It also visualizes historical data against the predicted trend.

## Features
- **Basic Arithmetic:** Addition, Subtraction, Multiplication, Division, Modulo, and Power.
- **Expense Prediction:** Uses a trained Machine Learning model to forecast expenses for future months.
- **Interactive Visualization:** Displays a plot of historical expenses, the learned regression line, and the specific future prediction.
- **User-Friendly Interface:** A clean, interactive UI built with Streamlit, featuring sidebar controls and organized layouts.

## Technologies
- Python
- Streamlit
- Pandas
- Scikit-learn (Linear Regression)
- Matplotlib

## How to Run
1.  **Install dependencies:**
    ```bash
    pip install streamlit pandas scikit-learn matplotlib
    ```
2.  **Run the application:**
    From the project's root directory, execute the following command in your terminal:
    ```bash
    streamlit run streamlit/app.py
    ```

## Data
Historical expense data is stored in `data.csv` and is used to train the Linear Regression model. The model learns the trend from this data to make future predictions.
