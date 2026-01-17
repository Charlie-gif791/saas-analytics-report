import pandas as pd

def load_stripe_charges(csv_path: str) -> pd.DataFrame:
    """
    Load and normalize a Stripe charges CSV export.

    Expected Stripe columns (minimum):
    - customer_id
    - created
    - amount (in cents)

    Returns a DataFrame with:
    - customer_id
    - charge_date (UTC datetime)
    - amount (float, dollars)
    """

    df = pd.read_csv(csv_path)

    # ---- Required columns ----
    required_columns = {"customer_id", "charge_date", "amount"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required Stripe columns: {missing}")

    # ---- Normalize schema ----
    normalized_df = pd.DataFrame()

    normalized_df["customer_id"] = df["customer_id"]

    # Stripe 'created' is typically a Unix timestamp (seconds)
    normalized_df["charge_date"] = pd.to_datetime(
        df["charge_date"],
        format="%Y-%m-%d",
        utc=True,
    )

    # Convert cents to dollars
    normalized_df["amount"] = df["amount"] / 100.0

    return normalized_df
