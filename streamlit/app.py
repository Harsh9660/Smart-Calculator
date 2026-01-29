import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculator import SmartCalculator

@st.cache_resource
def load_calculator():
    """Loads the SmartCalculator and trains the model. Cached to prevent reloading."""
    try:
        return SmartCalculator()
    except Exception:
        return None

def main():
    st.set_page_config(page_title="Smart Calc AI", page_icon="📈", layout="wide")

    # Custom CSS for Premium Look
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #007bff;
            color: white;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        div[data-testid="stExpander"] {
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Smart Calc AI & Expense Forecast")
    st.markdown("---")

    calc = load_calculator()
    
    # Path for data
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data.csv'))
    
    try:
        expense_data = pd.read_csv(data_path)
    except FileNotFoundError:
        st.error("Error: `data.csv` not found.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["🧮 Calculator Suite", "📈 Expense Forecast", "📊 Data Management"])

    with tab1:
        st.header("Financial Calculator Suite")
        calc_type = st.selectbox("Choose a tool:", ["Basic Arithmetic", "Compound Interest", "Loan EMI"])
        
        col_in, col_out = st.columns([1, 1])
        
        with col_in:
            if calc_type == "Basic Arithmetic":
                n1 = st.number_input("Number 1", value=0.0, step=1.0)
                n2 = st.number_input("Number 2", value=0.0, step=1.0)
                op = st.selectbox("Operation", ["+", "-", "*", "/", "%", "^"])
                if st.button("Calculate Result"):
                    try:
                        if op == "+": res = calc.add(n1, n2)
                        elif op == "-": res = calc.subtract(n1, n2)
                        elif op == "*": res = calc.multiply(n1, n2)
                        elif op == "/": res = calc.divide(n1, n2)
                        elif op == "%": res = calc.modulo(n1, n2)
                        else: res = calc.power(n1, n2)
                        st.session_state.res = res
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            elif calc_type == "Compound Interest":
                p = st.number_input("Principal (P)", value=1000.0, step=100.0)
                r = st.number_input("Annual Interest Rate (%)", value=5.0, step=0.1)
                t = st.number_input("Time Period (Years)", value=5.0, step=1.0)
                if st.button("Calculate Final Amount"):
                    st.session_state.res = calc.compound_interest(p, r, t)

            elif calc_type == "Loan EMI":
                p = st.number_input("Loan Amount", value=50000.0, step=1000.0)
                r = st.number_input("Annual Interest Rate (%)", value=8.5, step=0.1)
                t = st.number_input("Loan Tenure (Years)", value=3.0, step=0.5)
                if st.button("Calculate Monthly EMI"):
                    st.session_state.res = calc.loan_emi(p, r, t)

        with col_out:
            if 'res' in st.session_state:
                st.subheader("Calculation Result")
                st.metric("Total/Result", f"{st.session_state.res:,.2f}")
                del st.session_state.res

    with tab2:
        st.header("Expense Forecasting")
        
        future_m = st.slider("Select Month for Prediction:", 
                           min_value=1, 
                           max_value=48, 
                           value=int(expense_data['month'].max()) + 1)
        
        prediction = calc.predict_expense(future_m)
        
        # Plotly Visualization
        max_m = max(future_m, int(expense_data['month'].max()))
        x_trend = list(range(1, max_m + 2))
        y_trend = [calc.predict_expense(m) for m in x_trend]
        
        fig = go.Figure()
        
        # Historical Data
        fig.add_trace(go.Scatter(x=expense_data['month'], y=expense_data['expense'], 
                                mode='lines+markers', name='Historical',
                                line=dict(color='#007bff', width=3)))
        
        # Trend Line
        fig.add_trace(go.Scatter(x=x_trend, y=y_trend, 
                                mode='lines', name='Forecast Trend',
                                line=dict(color='#ff7f0e', dash='dash')))
        
        # Prediction Point
        fig.add_trace(go.Scatter(x=[future_m], y=[prediction], 
                                mode='markers', name='Prediction Point',
                                marker=dict(color='red', size=15, symbol='star')))
        
        fig.update_layout(title="Expense Trend Analysis",
                          xaxis_title="Month",
                          yaxis_title="Expense Amount",
                          template="plotly_white",
                          hovermode="x unified")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"Estimated expense for month **{future_m}** is **${prediction:,.2f}**.")

    with tab3:
        st.header("Data Management")
        
        col_v, col_a = st.columns([1, 1])
        
        with col_v:
            st.subheader("Historical Records")
            st.dataframe(expense_data, use_container_width=True)
        
        with col_a:
            st.subheader("Add or Update Record")
            new_m = st.number_input("Month Index", value=int(expense_data['month'].max()) + 1, step=1)
            new_e = st.number_input("Expense Value", value=1000.0, step=100.0)
            
            if st.button("Save Record"):
                if new_m in expense_data['month'].values:
                    expense_data.loc[expense_data['month'] == new_m, 'expense'] = new_e
                    st.info(f"Updated record for month {new_m}")
                else:
                    new_row = pd.DataFrame({'month': [new_m], 'expense': [new_e]})
                    expense_data = pd.concat([expense_data, new_row], ignore_index=True)
                    st.success(f"Added new record for month {new_m}")
                
                expense_data = expense_data.sort_values('month')
                expense_data.to_csv(data_path, index=False)
                
                # Retrain model
                calc.expense_predictor.train_model()
                st.rerun()

if __name__ == "__main__":
    main()
