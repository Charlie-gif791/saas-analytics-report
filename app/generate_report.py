import pandas as pd
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from .validation import validate_charge_date_coverage
from .metrics_customers import compute_customer_metrics
from .metrics_revenue import compute_revenue_metrics
from .load_stripe_csv import load_stripe_charges
from .llm_summary import generate_summary
from jinja2 import Environment, FileSystemLoader, StrictUndefined

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
NA = "N/A"

def generate_report(charges_df: pd.DataFrame) -> str:
    """
    Runs validation, computes metrics, generates LLM summary,
    and returns rendered HTML report.
    """
    logger.info("Starting report generation")
    failure_reason = None

    # -----------------------
    # Validation
    # -----------------------
    try:
        logger.info("Validating input data")
        validate_charge_date_coverage(charges_df)
    
    except Exception as e:
        failure_reason = str(e)

    # -----------------------
    # Metrics
    # -----------------------
    if not failure_reason:
        logger.info("Computing customer metrics")
        customer_metrics = compute_customer_metrics(charges_df)

        logger.info("Computing revenue metrics")
        revenue_metrics = compute_revenue_metrics(charges_df)
    else:
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
    # Create report data
    # -----------------------
    report_data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "customer_metrics": customer_metrics,
        "revenue_metrics": revenue_metrics,
        "summary_text": None
    }

    # -----------------------
    # Create summary
    # -----------------------
    if failure_reason:
        summary_text = (
            "Insufficient historical data to compute one or more metrics "
            "for the 30-day analysis window."
        )
    else:
        summary_text = generate_summary(report_data)

    report_data["summary_text"] = summary_text

    # -----------------------
    # Render report
    # -----------------------
    env = Environment(
        loader=FileSystemLoader(BASE_DIR),
        undefined=StrictUndefined,
    )
    template = env.get_template("report.html")

    logger.info("Rendering HTML report")
    rendered_html = template.render(report_data)

    return rendered_html

# -----------------------
# Script feature
# -----------------------
if __name__ == "__main__":
    csv_path = Path("data/example_stripe_export.csv")
    charges_df = load_stripe_charges(csv_path)
    html = generate_report(charges_df)

    output_path = BASE_DIR / "final_report.html"
    with open(output_path, "w") as f:
        f.write(html)

    print("Report generated: final_report.html")
