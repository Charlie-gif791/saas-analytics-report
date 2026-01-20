import pandas as pd
from datetime import timedelta

def validate_charge_date_coverage(charges_df, analysis_date):
    """
    Ensures the dataset covers at least the last 30 days.
    """
    charges_df = charges_df.copy()

    charges_df["charge_date"] = pd.to_datetime(
        charges_df["charge_date"],
        utc=True
    )

    required_columns = {"customer_id", "charge_date", "amount"}
    missing = required_columns - set(charges_df.columns)

    if charges_df.empty:
        raise ValueError("Uploaded dataset contains no rows.")

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if (charges_df["amount"] < 0).any():
        raise ValueError("Charge amounts must be non-negative.")

    min_required_date = analysis_date - timedelta(days=30)
    max_charge_date = charges_df["charge_date"].max()

    if max_charge_date < min_required_date:
        raise ValueError(
            "Charge data does not cover the required last 30-day analysis window."
        )
