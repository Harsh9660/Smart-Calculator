import streamlit as st
from calculator import add, sub, mul, div, mod, pow

def main():
    st.title("Smart Calculator")
    st.write("This is a simple calculator that can perform basic arithmetic operations.")

    num1 = st.number_input("Enter the first number:", value=0.0, format="%.4f")
    num2 = st.number_input("Enter the second number:", value=0.0, format="%.4f")

    operation = st.selectbox(
        "Select an operation:",
        ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Power"]
    )

    if st.button("Calculate"):
        result = None
        if operation == "Addition":
            result = add(num1, num2)
        elif operation == "Subtraction":
            result = sub(num1, num2)
        elif operation == "Multiplication":
            result = mul(num1, num2)
        elif operation == "Division":
            if num2 == 0:
                st.error("Error: Division by zero is not allowed.")
            else:
                result = div(num1, num2)
        elif operation == "Modulo":
            if num2 == 0:
                st.error("Error: Modulo by zero is not allowed.")
            else:
                result = mod(num1, num2)
        elif operation == "Power":
            result = pow(num1, num2)

        if result is not None:
            st.success(f"Result: {result}")

if __name__ == "__main__":
    main()