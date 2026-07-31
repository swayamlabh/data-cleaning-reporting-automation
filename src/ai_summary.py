import json
from .config import settings


def heuristic_summary(profile: dict, changes: dict) -> str:
    """Useful local fallback when no AI provider is configured."""
    shape = profile["shape"]; score = profile["quality_score"]
    return (f"The dataset contains {shape['rows']:,} rows and {shape['columns']} fields after processing. "
            f"Data quality is scored at {score}/100. The pipeline removed {changes.get('duplicates_removed', 0)} duplicate records. "
            "Prioritize reviewing high-impact correlations and validate operational assumptions before deployment.")


def generate_insights(profile: dict, changes: dict) -> str:
    """Call the Responses API when configured; otherwise return a deterministic executive summary."""
    if not settings.openai_api_key:
        return heuristic_summary(profile, changes)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = "Write a concise executive data-quality and business-insight summary. Use professional language. Data: " + json.dumps({"profile": profile, "changes": changes}, default=str)
        response = client.responses.create(model=settings.openai_model, input=prompt)
        return response.output_text
    except Exception:
        return heuristic_summary(profile, changes)
