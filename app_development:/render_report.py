from jinja2 import Environment, FileSystemLoader

# Load templates from the current directory
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('report.html')

# Fake data for now
data = {
    "total_revenue": "$12,000",
    "previous_total_revenue": "$10,000",
    "revenue_change_pct": "+20%",
    "active_customers": 120,
    "new_customers": 15,
    "churn_rate": "4.2%",
    "summary_text": (
        "Revenue increased primarily due to higher retention among existing customers. "
        "Customer churn remained stable compared to the previous period."
    )
}


# Render the template
rendered_html = template.render(data)

# Write output to a new file
with open("rendered_report.html", "w") as f:
    f.write(rendered_html)

print("Rendered report saved as rendered_report.html")
