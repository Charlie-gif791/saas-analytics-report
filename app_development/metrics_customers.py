import pandas as pd
from datetime import datetime, timedelta, timezone

def compute_customer_metrics(charges_df, analysis_date=None):
    """
    charges_df must include:
      - customer_id
      - charge_date (datetime)
    """
    charges_df = charges_df.copy()

    charges_df["charge_date"] = pd.to_datetime(
        charges_df["charge_date"],
        utc=True
    )
    
    assert pd.api.types.is_datetime64_any_dtype(charges_df["charge_date"])

    if analysis_date is None:
        analysis_date = datetime.now(timezone.utc)

    current_start = analysis_date - timedelta(days=30)
    previous_start = current_start - timedelta(days=30)

    current_period = charges_df[
        (charges_df["charge_date"] >= current_start) &
        (charges_df["charge_date"] < analysis_date)
    ]

    previous_period = charges_df[
        (charges_df["charge_date"] >= previous_start) &
        (charges_df["charge_date"] < current_start)
    ]

    current_customers = set(current_period["customer_id"])
    previous_customers = set(previous_period["customer_id"])

    active_customers = len(current_customers)

    new_customers = (
    len(current_customers - previous_customers)
    if len(previous_customers) > 0
    else None
    )

    churned_customers = len(previous_customers - current_customers)

    churn_rate = (
    round((churned_customers / len(previous_customers)) * 100, 2)
    if len(previous_customers) > 0
    else None
    )

    return {
        "active_customers": active_customers,
        "new_customers": new_customers,
        "customer_churn_rate": churn_rate
    }
