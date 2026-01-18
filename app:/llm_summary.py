import openai, os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_summary(metrics_payload: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheap and sufficient
        messages=[
            {
                "role": "system",
                "content": (
                    """
                    You are a neutral analytics assistant generating an executive summary for a SaaS business report.

                    Rules:
                    - Base the summary strictly on the provided metrics.
                    - Do not speculate, forecast, or give advice.
                    - Do not introduce new metrics or assumptions.
                    - When referring to annualized run rate, describe it explicitly as “based on the last 30 days” and avoid predictive language (e.g., “projected”, “expected”).
                    - If any metric is marked “N/A” or missing, explicitly state that insufficient data was available for that metric.
                    - Use a professional, concise, consulting-style tone.
                    - Limit the summary to 3-4 sentences.
                    - Each sentence should focus on a distinct category: revenue, customer activity, churn, and data limitations (if applicable).
                    """
                )
            },
            {
                "role": "user",
                "content": metrics_payload
            }
        ],
        temperature=0.1,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
