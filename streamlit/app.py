import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from ..calculator import add, sub, mul, div, mod, pow

def main():
    st.title("Smart Calculator")
    st.write("This is a smart calculator that can perform addition, subtraction, multiplication, division, and modulo operations.")
    st.write("Enter the first number:")
    num1 = st.number_input("Number 1", value=0)
    st.write("Enter the second number:")
    num2 = st.number_input("Number 2", value=0)
    st.write("Select the operation:")
    operation = st.selectbox("Operation", ["Addition", "Subtraction", "Multiplication", "Division", "Modulo"])
    if st.button("Calculate"):
        if operation == "Addition":
            st.write("The result is:", num1 + num2)
        elif operation == "Subtraction":
            st.write("The result is:", num1 - num2)
        elif operation == "Multiplication":
            st.write("The result is:", num1 * num2)
        elif operation == "Division":
            st.write("The result is:", num1 / num2)
        elif operation == "Modulo":
            st.write("The result is:", num1 % num2)

    else:
        st.write("Please select an operation.")