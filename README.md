# TeleConnect ML Assignment
End-to-end supervised learning project for telecom churn prediction and monthly revenue forecasting, including interpretability and business recommendations.
This repository is organized to match the assignment submission structure and supports EDA, preprocessing, classification, regression, and SHAP/PDP interpretation workflows.

## Dataset
- Source: Telco Customer Churn (Kaggle)  
  https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Contains ~7,043 customer records with demographic, service, contract, billing, churn labels, and charge fields.

## Installation & Setup
```bash
git clone https://github.com/your-username/teleconnect-ml-assignment.git
cd teleconnect-ml-assignment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Repository Structure
- `data/` raw + processed data folders and dataset notes
- `notebooks/` assignment-stage notebooks (EDA to interpretation)
- `src/` reusable pipeline modules
- `models/` saved trained artifacts
- `reports/` markdown results and figures
- `tests/` unit tests for preprocessing and evaluation helpers

## Quick Run
Place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/raw/` (or repo root for legacy scripts), then run your chosen notebook/script workflow.

## Current outputs from interpretation workflow
- SHAP summary and local explanations
- PDP plots for top features
- High-risk segments and top-100 intervention targets
- ROI comparison: model targeting vs random targeting
