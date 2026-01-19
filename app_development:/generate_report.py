import pandas as pd, json
from datetime import datetime, timezone
from pathlib import Path

from .validation import validate_charge_date_coverage
from .metrics_customers import compute_customer_metrics
from .metrics_revenue import compute_revenue_metrics
from .load_stripe_csv import load_stripe_charges
from .llm_summary import generate_summary
from jinja2 import Environment, FileSystemLoader, StrictUndefined

BASE_DIR = Path(__file__).resolve().parent
NA = "N/A"

# Make an error message if jinja cannot access variables
env = Environment(
    loader=FileSystemLoader(BASE_DIR),
    undefined=StrictUndefined
)

# -----------------------
# Load Stripe CSV
# -----------------------
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

csv_path = DATA_DIR / "example_stripe_export.csv"
charges_df = load_stripe_charges(csv_path)

# -----------------------
# Analysis date
# -----------------------
analysis_date = charges_df["charge_date"].max()

# Validate input or report warning/failure
failure_reason = None
warning_reason = None

try:
    # -----------------------
    # Validation
    # -----------------------
    validate_charge_date_coverage(charges_df, analysis_date)
    print("Validating CSV input...")

    # -----------------------
    # Compute metrics
    # -----------------------

    customer_metrics = compute_customer_metrics(charges_df, analysis_date)
    revenue_metrics = compute_revenue_metrics(charges_df, analysis_date)
    print("Computing revenue and customer metrics...")

except Exception as e:
    failure_reason = str(e)

    customer_metrics = {
        "active_customers": NA,
        "new_customers": NA,
        "customer_churn_rate": None,
    }

    revenue_metrics = {
        "total_revenue": NA,
        "previous_total_revenue": NA,
        "revenue_change_percent": None,
        "annualized_run_rate": NA,
    }

# -----------------------
# Create summary
# -----------------------
if failure_reason:
    summary_text = (
        "The uploaded data could not be processed due to missing or "
        "invalid required fields."
    )
else:
    metrics_payload = json.dumps(
        {
        "revenue_metrics": revenue_metrics,
        "customer_metrics": customer_metrics,
        }
    )
    summary_text = generate_summary(metrics_payload)
    print("Generating LLM summary...")

# -----------------------
# Prepare report data
# -----------------------
report_data = {
    "total_revenue": f"${revenue_metrics['total_revenue']}",
    "previous_total_revenue": f"${revenue_metrics['previous_total_revenue']}",
    "revenue_change_percent": (
        f"{revenue_metrics['revenue_change_percent']}%"
        if revenue_metrics["revenue_change_percent"] is not None
        else "N/A"
    ),
    "annualized_run_rate": (
    f"${revenue_metrics['annualized_run_rate']}"
    if revenue_metrics["annualized_run_rate"] is not None
    else "N/A"
    ),
    "active_customers": customer_metrics["active_customers"],
    "new_customers": customer_metrics["new_customers"],
    "customer_churn_rate": (
        f"{customer_metrics['customer_churn_rate']}%"
        if customer_metrics["customer_churn_rate"] is not None
        else "N/A"
    ),
    "summary_text": summary_text,
}

# -----------------------
# Render report
# -----------------------
env = Environment(loader=FileSystemLoader(BASE_DIR))
template = env.get_template("report.html")

rendered_html = template.render(report_data)

output_path = BASE_DIR / "final_report.html"

with open(output_path, "w") as f:
    f.write(rendered_html)

print("Report generated: final_report.html")