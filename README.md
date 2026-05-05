# TeleConnect ML Assignment Solution

## Task 5 Implemented: Model Interpretation & Business Recommendations

This script now focuses on interpreting the best churn classification model and generating business-facing recommendations.

## What is included
- Trains a best-practice churn classifier (Random Forest) on engineered Telco features.
- Uses **SHAP** for:
  - Global feature importance (summary plot)
  - Local explanations for 2 customers (1 churned, 1 retained)
- Builds **Partial Dependence Plots (PDP)** for top 3 SHAP-ranked features.
- Produces business evidence files to answer:
  1. Top churn drivers
  2. Highest-risk segments
  3. Intervention targeting list (top 100)
  4. ROI of model-based targeting vs random targeting

## Run
1. Ensure `WA_Fn-UseC_-Telco-Customer-Churn.csv` is in repo root.
2. Install dependencies if needed (`shap`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`).
3. Execute:
```bash
python teleconnect_churn_ml_pipeline.py
```

## Key outputs
- `outputs/classification_scored_test_set.csv`
- `outputs/shap_local_explanations_two_cases.csv`
- `outputs/high_risk_segments.csv`
- `outputs/top_100_intervention_targets.csv`
- `outputs/roi_model_vs_random.csv`
- `outputs/plots/shap_summary_best_classifier.png`
- `outputs/plots/pdp_top3_features.png`
