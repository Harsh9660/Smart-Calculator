from calculator import SmartCalculator

def test_calculator():
    calc = SmartCalculator()
    
    assert calc.add(2, 3) == 5
    assert calc.divide(10, 2) == 5
    
    ci = calc.compound_interest(1000, 5, 5)
    print(f"CI Result: {ci}")
    assert 1280 < ci < 1290
    
    
    emi = calc.loan_emi(50000, 8.5, 3)
    print(f"EMI Result: {emi}")
    assert 1500 < emi < 1600
    
    pred = calc.predict_expense(13)
    print(f"Prediction for Month 13: {pred}")
    assert pred > 0

    print("All tests passed!")

if __name__ == "__main__":
    test_calculator()
