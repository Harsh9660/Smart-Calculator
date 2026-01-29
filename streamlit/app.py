import streamlit as st
from calculator import SmartCalculator

def main():
    st.title("Smart Calculator")
    st.write("This is a simple calculator that can perform basic arithmetic operations.")

    try:
        # This instantiates the calculator and trains the ML model
        calc = SmartCalculator()
    except FileNotFoundError:
        st.error("Error: `data.csv` not found. Please create this file in the project root directory with 'month' and 'expense' columns.")
        st.stop()

    num1 = st.number_input("Enter the first number:", value=0.0, format="%.4f")
    num2 = st.number_input("Enter the second number:", value=0.0, format="%.4f")

    operation = st.selectbox(
        "Select an operation:",
        ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Power"]
    )

    if st.button("Calculate"):
        result = None
        if operation == "Addition":
            result = calc.add(num1, num2)
        elif operation == "Subtraction":
            result = calc.subtract(num1, num2)
        elif operation == "Multiplication":
            result = calc.multiply(num1, num2)
        elif operation == "Division":
            if num2 == 0:
                st.error("Error: Division by zero is not allowed.")
            else:
                result = calc.divide(num1, num2)
        elif operation == "Modulo":
            if num2 == 0:
                st.error("Error: Modulo by zero is not allowed.")
            else:
                result = calc.modulo(num1, num2)
        elif operation == "Power":
            result = calc.power(num1, num2)

        if result is not None:
            st.success(f"Result: {result}")

if __name__ == "__main__":
    main()