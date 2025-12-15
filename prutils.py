import json

def _try_parse_json(text: str):
    """
    Attempts to parse JSON from model output.
    Strips all Markdown backticks before parsing.
    """
    if not text:
        return None

    # Remove all backticks (``` and `)
    cleaned = text.replace("```", "").replace("`", "").replace("json","").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        return None