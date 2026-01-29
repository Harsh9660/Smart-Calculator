import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculator import SmartCalculator

@st.cache_resource
def load_calculator():
    """Loads the SmartCalculator and trains the model."""
    try:
        calc = SmartCalculator(),

        if not hasattr(calc, 'compound_interest') or not hasattr(calc, 'loan_emi'):
            st.cache_resource.clear()
            calc = SmartCalculator()
        return calc
    except Exception as e:
        print(f"Error loading calculator: {e}")
        return None

def load_expense_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.csv'))
    try:
        return pd.read_csv(data_path), data_path
    except FileNotFoundError:
        st.error("Error: `data.csv` not found.")
        st.stop()

def main():
    st.set_page_config(page_title="Smart Calc AI", page_icon="💰", layout="wide")

    # Re-applying Premium CSS
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stButton>button {
            width: 100%; border-radius: 8px; height: 3em;
            background-color: #007bff; color: white; font-weight: bold;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            color: #000000 !important;
        }
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Smart Calc AI & Expense Forecast")
    st.markdown("---")

    calc = load_calculator()
    if calc is None or not hasattr(calc, 'compound_interest'):
        st.error("Fatal Error: Could not initialize the Smart Calculator with full features. Please refresh the page.")
        st.cache_resource.clear()
        st.stop()

    expense_data, data_path = load_expense_data()

    tab1, tab2, tab3 = st.tabs(["Calculator Suite", "Expense Forecast", "Data Management"])

    with tab1:
        st.header("Financial Calculator Suite")
        calc_type = st.selectbox("Choose a tool:", ["Basic Arithmetic", "Compound Interest", "Loan EMI"])
        
        col_in, col_out = st.columns([1, 1])
        
        with col_in:
            result = None
            if calc_type == "Basic Arithmetic":
                n1 = st.number_input("Number 1", value=0.0)
                n2 = st.number_input("Number 2", value=0.0)
                op = st.selectbox("Operation", ["+", "-", "*", "/", "%", "^"])
                if st.button("Calculate Result", key="basic_calc"):
                    try:
                        if op == "+": result = calc.add(n1, n2)
                        elif op == "-": result = calc.subtract(n1, n2)
                        elif op == "*": result = calc.multiply(n1, n2)
                        elif op == "/": result = calc.divide(n1, n2)
                        elif op == "%": result = calc.modulo(n1, n2)
                        else: result = calc.power(n1, n2)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            elif calc_type == "Compound Interest":
                p = st.number_input("Principal (P)", value=1000.0)
                r = st.number_input("Annual Interest Rate (%)", value=5.0)
                t = st.number_input("Time Period (Years)", value=5.0)
                if st.button("Calculate Final Amount", key="ci_calc"):
                    result = calc.compound_interest(p, r, t)

            elif calc_type == "Loan EMI":
                p = st.number_input("Loan Amount", value=50000.0)
                r = st.number_input("Annual Interest Rate (%)", value=8.5)
                t = st.number_input("Loan Tenure (Years)", value=3.0)
                if st.button("Calculate Monthly EMI", key="emi_calc"):
                    result = calc.loan_emi(p, r, t)

        with col_out:
            if result is not None:
                st.subheader("Calculation Result")
                st.metric("Total/Result", f"{result:,.2f}")

    with tab2:
        st.header("Expense Forecasting")
        future_m = st.slider("Select Month for Prediction:", 
                           min_value=1, max_value=48, 
                           value=int(expense_data['month'].max()) + 1)
        
        prediction = calc.predict_expense(future_m)
        
        max_m = max(future_m, int(expense_data['month'].max()))
        x_trend = list(range(1, max_m + 2))
        y_trend = [calc.predict_expense(m) for m in x_trend]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=expense_data['month'], y=expense_data['expense'], 
                                mode='lines+markers', name='Historical', line=dict(color='#007bff', width=3)))
        fig.add_trace(go.Scatter(x=x_trend, y=y_trend, 
                                mode='lines', name='Forecast Trend', line=dict(color='#ff7f0e', dash='dash')))
        fig.add_trace(go.Scatter(x=[future_m], y=[prediction], 
                                mode='markers', name='Prediction Point', marker=dict(color='red', size=15, symbol='star')))
        
        fig.update_layout(title="Expense Trend Analysis", xaxis_title="Month", yaxis_title="Expense Amount",
                          template="plotly_white", hovermode="x unified")
        
        st.plotly_chart(fig, width='stretch')
        st.success(f"Estimated expense for month **{future_m}**: **₹{prediction:,.2f}**")

    with tab3:
        st.header("Data Management")
        col_v, col_a = st.columns([1, 1])
        
        with col_v:
            st.subheader("Historical Records")
            st.dataframe(expense_data, width='stretch')
        
        with col_a:
            st.subheader("Add or Update Record")
            new_m = st.number_input("Month Index", value=int(expense_data['month'].max()) + 1, step=1)
            new_e = st.number_input("Expense Value", value=1000.0, step=100.0)
            
            if st.button("Save Record"):
                if new_m in expense_data['month'].values:
                    expense_data.loc[expense_data['month'] == new_m, 'expense'] = new_e
                else:
                    new_row = pd.DataFrame({'month': [new_m], 'expense': [new_e]})
                    expense_data = pd.concat([expense_data, new_row], ignore_index=True)
                
                expense_data = expense_data.sort_values('month')
                expense_data.to_csv(data_path, index=False)
                calc.expense_predictor.train_model()
                st.cache_resource.clear() 
                st.rerun()

if __name__ == "__main__":
    main()
