from __future__ import annotations

import json
from openai import OpenAI
from typing import Any, Dict

import prconfig
import prutils

# Step 1: fingerprint extraction
def extract_pragmatic_fingerprint(
    client: OpenAI,
    text: str,
    language_context: str = "unknown",
) -> Dict[str, Any]:
    system = "You are a linguistics expert specializing in pragmatics, politeness theory, and translation pragmatics."
    user = f"""
{prconfig.politeness_schema}

Analyze the following text.

Context:
- Language context (if known): {language_context}
- This text MAY be a translation into English; infer upstream pragmatic features where appropriate.

Text:
\"\"\"{text}\"\"\"

Return ONLY a JSON object with this exact shape:

{{
  "features": {{
    "addressee_elevation": {{"value": "...", "evidence": ["..."]}},
    "speaker_self_lowering": {{"value": "...", "evidence": ["..."]}},
    "directness_strategy": {{"value": "...", "evidence": ["..."]}},
    "face_management": {{"value": "...", "evidence": ["..."]}},
    "politeness_redundancy": {{"value": "...", "evidence": ["..."]}},
    "obligation_softening": {{"value": "...", "evidence": ["..."]}},
    "grammaticalized_politeness_origin": {{"value": "...", "evidence": ["..."]}}
  }},
  "notes": {{
    "compensatory_english_strategies": ["..."],
    "uncertainties": ["..."]
  }}
}}

Rules:
- Use ONLY allowed values from the schema.
- Evidence must be short quotes or precise descriptions referencing the text.
- Do NOT guess the language.
"""
    return prutils.llm_json(client, system=system, user=user, temperature=0.2)