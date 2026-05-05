import pandas as pd


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["TotalCharges"] = data["TotalCharges"].fillna(data["TotalCharges"].median())
    safe_tenure = data["tenure"].replace(0, 1)
    data["AvgMonthlySpend"] = data["TotalCharges"] / safe_tenure
    service_cols = ["PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
    data["ServiceCount"] = data[service_cols].apply(lambda r: sum(v == "Yes" for v in r), axis=1)
    contract_map = {"Month-to-month": 1, "One year": 12, "Two year": 24}
    data["ContractMonths"] = data["Contract"].map(contract_map).fillna(1)
    data["ContractValue"] = data["MonthlyCharges"] * data["ContractMonths"]
    return data
