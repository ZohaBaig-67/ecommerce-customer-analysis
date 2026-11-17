# E-Commerce Customer Behavior Analysis

Exploratory data analysis and an interactive Streamlit dashboard using the supplied e-commerce customer dataset.

## Dataset
`ecommerce_customers.csv` contains 500 rows and 8 columns. It includes customer identifiers and engagement/spending measures: average session length, time on app, time on website, membership length, and yearly amount spent.

## Key findings
- No missing values were found in the supplied dataset.
- No exact duplicate rows were found.
- The strongest numeric relationship with yearly spending is **Length of Membership** (Pearson r = **0.809**).
- App-time correlation with yearly spending is **0.499**; website-time correlation is **-0.003**.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `ecommerce_customer_analysis.ipynb` — full step-by-step EDA notebook
- `app.py` — Streamlit dashboard
- `ecommerce_customers.csv` — dataset
- `requirements.txt` — Python dependencies
- `.gitignore` — ignores virtual environments and secrets

## Live app
Add the deployed Streamlit URL here after deployment.
