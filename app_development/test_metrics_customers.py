import pandas as pd
from metrics_customers import compute_customer_metrics

df = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 2, 3, 4],
        "charge_date": [
            "2025-11-15",  # previous
            "2025-11-20",  # previous
            "2025-11-25",  # previous
            "2025-12-20",  # current
            "2025-12-22",  # current
            "2025-12-23",  # current
        ],
    }
)

df["charge_date"] = pd.to_datetime(df["charge_date"], format="%Y-%m-%d", utc=True)
print(compute_customer_metrics(df))