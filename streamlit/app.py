import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
# Add the project root to the Python path to allow importing 'calculator'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculator import SmartCalculator


@st.cache_resource
def load_calculator():
    """Loads the SmartCalculator and trains the model. Cached to prevent reloading on each run."""
    try:
        calc = SmartCalculator()
        return calc
    except FileNotFoundError:
        return None

@st.cache_data
def load_data():
    """Loads the historical expense data from data.csv. Cached for performance."""
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.csv'))
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        return None

def main():
    st.set_page_config(page_title="Smart Calculator", page_icon="💡", layout="wide")

    st.title("💡 Smart Financial Calculator")
    st.write("An intelligent tool for your arithmetic needs and financial expense forecasting.")

    calc = load_calculator()
    expense_data = load_data()

    if calc is None or expense_data is None:
        st.error("Error: `data.csv` not found. Please ensure it exists in the project root directory.")
        st.stop()

    # --- Sidebar for Inputs ---
    st.sidebar.header("Controls")

    # Calculator Section in Sidebar
    with st.sidebar.expander("🧮 Basic Calculator", expanded=False):
        num1 = st.number_input("First number:", value=0.0, format="%.4f", key="num1")
        num2 = st.number_input("Second number:", value=1.0, format="%.4f", key="num2")
        operation = st.selectbox(
            "Operation:",
            ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Power"],
            key="op"
        )
        if st.button("Calculate", key="calc_btn"):
            result = None
            try:
                if operation == "Addition": result = calc.add(num1, num2)
                elif operation == "Subtraction": result = calc.subtract(num1, num2)
                elif operation == "Multiplication": result = calc.multiply(num1, num2)
                elif operation == "Division": result = calc.divide(num1, num2)
                elif operation == "Modulo": result = calc.modulo(num1, num2)
                elif operation == "Power": result = calc.power(num1, num2)
                
                if result is not None:
                    st.session_state.calc_result = f"The result of {operation} is **{result:.4f}**"
            except ValueError as e:
                st.session_state.calc_result = f"Error: {e}"

    # Prediction Section in Sidebar
    st.sidebar.header("📈 Expense Prediction")
    future_month = st.sidebar.slider(
        "Select a future month to predict:", 
        min_value=1, 
        max_value=36, 
        value=max(13, int(expense_data['month'].max()) + 1), 
        step=1
    )

    # --- Main Panel for Outputs ---
    if 'calc_result' in st.session_state:
        st.info(st.session_state.calc_result)
        del st.session_state.calc_result

    st.header("Expense Analysis and Forecasting")
    
    prediction = calc.predict_expense(future_month)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Expense Trend & Prediction")
        max_month = max(future_month, int(expense_data['month'].max()))
        x_range = list(range(1, max_month + 2))
        y_pred_line = [calc.predict_expense(m) for m in x_range]

        fig, ax = plt.subplots()
        ax.plot(expense_data['month'], expense_data['expense'], marker='o', linestyle='-', color='b', label='Historical Expenses')
        ax.plot(x_range, y_pred_line, linestyle='--', color='r', label='Expense Trend')
        ax.plot(future_month, prediction, marker='*', markersize=15, color='gold', label=f'Prediction for Month {future_month}')
        ax.set_title("Historical vs. Predicted Expenses")
        ax.set_xlabel("Month")
        ax.set_ylabel("Expense ($)")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.subheader("Prediction Result")
        st.metric(label=f"Predicted Expense for Month {future_month}", value=f"${prediction:,.2f}")
        st.info(f"Based on the historical data, the model predicts the expense for month {future_month} will be approximately **${prediction:,.2f}**.")

if __name__ == "__main__":
    main()
