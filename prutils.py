import asyncio
import json
import prconfig
import random
import time
from openai import OpenAI
from typing import Any, Dict

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
    
def llm_json(
    client: OpenAI,
    system: str,
    user: str,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Calls the model and expects a JSON object back.
    If the model returns non-JSON, this raises with helpful debug output.
    """
    resp = client.chat.completions.create(
        model=prconfig.model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )

    content = (resp.choices[0].message.content or "").strip()
    parsed = _try_parse_json(content)
    if parsed is None:
        raise ValueError(
            "Model did not return valid JSON.\n\n--- Raw output ---\n"
            f"{content}\n"
            "------------------\n"
        )
    return parsed

async def checktime():
    while True:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
        await asyncio.sleep(random.randint(10 * 60, 14 * 60))  # every 25 minutes
