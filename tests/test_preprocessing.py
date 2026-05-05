import pandas as pd
from src.preprocessing import clean_and_engineer


def test_clean_and_engineer_adds_columns():
    df = pd.DataFrame({
        "TotalCharges": [100.0, None],
        "tenure": [10, 0],
        "PhoneService": ["Yes", "No"],
        "MultipleLines": ["No", "Yes"],
        "OnlineSecurity": ["Yes", "No"],
        "OnlineBackup": ["No", "No"],
        "DeviceProtection": ["No", "No"],
        "TechSupport": ["Yes", "No"],
        "StreamingTV": ["No", "Yes"],
        "StreamingMovies": ["No", "No"],
        "Contract": ["Month-to-month", "One year"],
        "MonthlyCharges": [20.0, 30.0],
    })
    out = clean_and_engineer(df)
    for c in ["AvgMonthlySpend", "ServiceCount", "ContractMonths", "ContractValue"]:
        assert c in out.columns
