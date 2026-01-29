from ml_model import ExpensePredictor

class SmartCalculator:
    def __init__(self):
        self.expense_predictor = ExpensePredictor()
        self.expense_predictor.train_model()

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def modulo(self, a, b):
        if b == 0:
            raise ValueError("Cannot perform modulo by zero")
        return a % b

    def power(self, a, b):
        return a ** b

    def calculate_expense(self, monthly, months):
        return monthly * months

    def compound_interest(self, principal, rate, time, n=12):
        """
        Calculates compound interest.
        A = P(1 + r/n)^(nt)
        """
        amount = principal * (1 + (rate / 100) / n) ** (n * time)
        return amount

    def loan_emi(self, principal, rate, time_years):
        r = (rate / 100) / 12
        n = time_years * 12
        if r == 0:
            return principal / n
        emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return emi

    def predict_expense(self, future_month):
        return self.expense_predictor.predict(future_month)

def main():
    calc = SmartCalculator()

    while True:
        print("\n--- Smart Calculator Menu ---")
        print("1. Basic Calculator")
        print("2. Calculate Total Expense")
        print("3. Predict Future Expense (ML)")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print("Select operation:")
                print("a. Add")
                print("b. Subtract")
                print("c. Multiply")
                print("d. Divide")
                op = input("Operation: ")

                if op == "a":
                    print("Result:", calc.add(a, b))
                elif op == "b":
                    print("Result:", calc.subtract(a, b))
                elif op == "c":
                    print("Result:", calc.multiply(a, b))
                elif op == "d":
                    try:
                        print("Result:", calc.divide(a, b))
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid operation.")
            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "2":
            try:
                monthly = float(input("Enter monthly expense: "))
                months = int(input("Enter number of months: "))
                total = calc.calculate_expense(monthly, months)
                print(f"Total expense for {months} months is: {total}")
            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            try:
                future_month = int(input("Enter future month number for prediction: "))
                prediction = calc.predict_expense(future_month)
                print(f"Predicted expense for month {future_month}: {prediction:.2f}")
            except ValueError:
                print("Enter a valid integer.")
        
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
