import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import PartialDependenceDisplay
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

OUTPUT_DIR = Path("outputs")
PLOTS_DIR = OUTPUT_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path: str = "WA_Fn-UseC_-Telco-Customer-Churn.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    safe_tenure = data["tenure"].replace(0, 1)
    data["AvgMonthlySpend"] = data["TotalCharges"] / safe_tenure

    service_cols = ["PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
    data["ServiceCount"] = data[service_cols].apply(lambda r: sum(v == "Yes" for v in r), axis=1)
    contract_map = {"Month-to-month": 1, "One year": 12, "Two year": 24}
    data["ContractMonths"] = data["Contract"].map(contract_map).fillna(1)
    data["ContractValue"] = data["MonthlyCharges"] * data["ContractMonths"]
    return data


def build_best_classifier(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

    prep = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
    ])

    # chosen best model class for interpretability + strong tabular performance
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        class_weight="balanced",
        random_state=42,
    )

    pipe = Pipeline([("prep", prep), ("model", model)])
    pipe.fit(X_train, y_train)
    return pipe


def shap_global_and_local(pipe: Pipeline, X_test: pd.DataFrame, y_test: pd.Series):
    prep = pipe.named_steps["prep"]
    model = pipe.named_steps["model"]
    Xt = prep.transform(X_test)
    feature_names = prep.get_feature_names_out()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(Xt)

    # class 1 SHAP values for binary classification
    class1_shap = shap_values[1] if isinstance(shap_values, list) else shap_values

    plt.figure()
    shap.summary_plot(class1_shap, Xt, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "shap_summary_best_classifier.png", bbox_inches="tight")
    plt.close()

    proba = pipe.predict_proba(X_test)[:, 1]
    scored = X_test.copy()
    scored["actual_churn"] = y_test.values
    scored["churn_probability"] = proba
    churned_ix = scored[scored["actual_churn"] == 1].sort_values("churn_probability", ascending=False).index[0]
    retained_ix = scored[scored["actual_churn"] == 0].sort_values("churn_probability", ascending=True).index[0]

    local_rows = []
    for idx, label in [(churned_ix, "churned"), (retained_ix, "retained")]:
        pos = X_test.index.get_loc(idx)
        vals = class1_shap[pos]
        top_idx = np.argsort(np.abs(vals))[::-1][:10]
        local_df = pd.DataFrame({
            "feature": np.array(feature_names)[top_idx],
            "shap_value": vals[top_idx],
            "case_type": label,
            "row_index": int(idx),
        })
        local_rows.append(local_df)

    local_explanations = pd.concat(local_rows, ignore_index=True)
    local_explanations.to_csv(OUTPUT_DIR / "shap_local_explanations_two_cases.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "classification_scored_test_set.csv", index=False)

    return class1_shap, feature_names, scored


def pdp_top3(pipe: Pipeline, X_test: pd.DataFrame, class1_shap, feature_names):
    top3_idx = np.argsort(np.mean(np.abs(class1_shap), axis=0))[::-1][:3]
    top3_features = np.array(feature_names)[top3_idx].tolist()

    Xt = pipe.named_steps["prep"].transform(X_test)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    PartialDependenceDisplay.from_estimator(pipe.named_steps["model"], Xt, features=top3_idx.tolist(), ax=ax)
    for i, f in enumerate(top3_features):
        ax[i].set_title(f"PDP: {f}")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "pdp_top3_features.png", bbox_inches="tight")
    plt.close()
    return top3_features


def business_recommendations(scored: pd.DataFrame, raw_test: pd.DataFrame):
    merged = raw_test.copy()
    merged["actual_churn"] = scored["actual_churn"].values
    merged["churn_probability"] = scored["churn_probability"].values

    top_risk = merged.sort_values("churn_probability", ascending=False).head(100).copy()
    top_risk.to_csv(OUTPUT_DIR / "top_100_intervention_targets.csv", index=False)

    segment = (
        merged.groupby(["Contract", "InternetService"])["churn_probability"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
        .reset_index()
    )
    segment.to_csv(OUTPUT_DIR / "high_risk_segments.csv", index=False)

    expected_saved = top_risk["churn_probability"].sum()
    intervention_cost = 100 * 50
    expected_benefit = expected_saved * 500
    roi_model = (expected_benefit - intervention_cost) / intervention_cost

    random_baseline_prob = merged["actual_churn"].mean()
    expected_saved_random = 100 * random_baseline_prob
    benefit_random = expected_saved_random * 500
    roi_random = (benefit_random - intervention_cost) / intervention_cost

    roi_df = pd.DataFrame([
        {"strategy": "model_targeting", "expected_saved_customers": expected_saved, "benefit": expected_benefit, "cost": intervention_cost, "roi": roi_model},
        {"strategy": "random_targeting", "expected_saved_customers": expected_saved_random, "benefit": benefit_random, "cost": intervention_cost, "roi": roi_random},
    ])
    roi_df.to_csv(OUTPUT_DIR / "roi_model_vs_random.csv", index=False)


def main() -> None:
    df = feature_engineering(load_data())
    y = df["Churn"].map({"No": 0, "Yes": 1})
    X = df.drop(columns=["Churn", "customerID"])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    model = build_best_classifier(X_train, y_train)

    proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)
    print(f"Best classification model ROC-AUC: {auc:.4f}")

    class1_shap, feature_names, scored = shap_global_and_local(model, X_test, y_test)
    top3 = pdp_top3(model, X_test, class1_shap, feature_names)
    print("Top 3 PDP features:", top3)

    business_recommendations(scored, X_test)


if __name__ == "__main__":
    main()
