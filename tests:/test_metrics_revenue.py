import pandas as pd
from metrics_revenue import compute_revenue_metrics

# TEST
df = pd.DataFrame(
    {
        "amount": [1000, 1200],
        "charge_date": ["2025-12-1", "2026-1-11"],
    }
)

df["charge_date"] = pd.to_datetime(df["charge_date"], format="%Y-%m-%d", utc=True)
print(compute_revenue_metrics(df))