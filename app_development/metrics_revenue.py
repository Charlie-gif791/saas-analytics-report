import pandas as pd
from datetime import datetime, timedelta, timezone

def compute_revenue_metrics(charges_df, analysis_date=None):
    """
    charges_df must include:
      - amount (numeric, dollars)
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

    current_revenue = current_period["amount"].sum()
    previous_revenue = previous_period["amount"].sum()
    
    annualized_run_rate = (
        round(current_revenue * 12, 2)
        if current_revenue > 0
        else None
        )

    revenue_change_percent = (
        round((current_revenue - previous_revenue) / previous_revenue * 100, 2)
        if previous_revenue > 0
        else None
    )

    return {
        "total_revenue": round(current_revenue, 2),
        "previous_total_revenue": round(previous_revenue, 2),
        "revenue_change_percent": revenue_change_percent,
        "annualized_run_rate": annualized_run_rate,
    }
