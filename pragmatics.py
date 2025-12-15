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

# Step 2: translation resistance
def analyze_translation_resistance(
    client: OpenAI,
    source_text: str,
    english_translation: str,
    source_language_context: str = "unknown",
) -> Dict[str, Any]:
    system = "You are a translation pragmatics analyst. You track what politeness meaning is preserved vs flattened in translation."
    user = f"""
{prconfig.politeness_schema}

You are given:
1) A source-language text (could be Language A or B)
2) Its English translation

Source language context (if known): {source_language_context}

Source Text:
\"\"\"{source_text}\"\"\"

English Translation:
\"\"\"{english_translation}\"\"\"

Return ONLY a JSON object with this exact shape:

{{
  "feature_changes": {{
    "addressee_elevation": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "speaker_self_lowering": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "directness_strategy": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "face_management": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "politeness_redundancy": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "obligation_softening": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}},
    "grammaticalized_politeness_origin": {{"status": "preserved|weakened|lost|unknown", "explanation": "..."}}
  }},
  "english_compensation": ["..."],
  "overall_resistance": {{
    "level": "low|medium|high",
    "rationale": "..."
  }}
}}

Rules:
- If the source text is not in English, you may reason about honorific/speech-level cues if visible.
- If you cannot infer, use "unknown" status.
"""
    return prutils.llm_json(client, system=system, user=user, temperature=0.2)

# Step 3: attribution A vs B
def attribute_language_A_vs_B(
    client: OpenAI,
    fingerprint: Dict[str, Any],
    language_A_profile: str,
    language_B_profile: str,
) -> Dict[str, Any]:
    system = "You are a comparative pragmatics expert. You attribute which politeness system better explains a pragmatic fingerprint."
    user = f"""
{prconfig.politeness_schema}

You will compare:
- An unknown text fingerprint (already analyzed)
- A politeness profile for Language A
- A politeness profile for Language B

Unknown Text Fingerprint (JSON):
{json.dumps(fingerprint, ensure_ascii=False, indent=2)}

Language A Politeness Profile:
\"\"\"{language_A_profile}\"\"\"

Language B Politeness Profile:
\"\"\"{language_B_profile}\"\"\"

Return ONLY a JSON object with this exact shape:

{{
  "attribution": {{
    "winner": "A|B|unclear",
    "confidence": 0.0,
    "decisive_features": ["..."],
    "reasoning": "..."
  }},
  "diagnostics": {{
    "matches_A": ["..."],
    "matches_B": ["..."],
    "missing_information": ["..."]
  }}
}}

Rules:
- Confidence is a number from 0.0 to 1.0 (not a percentage).
- Prefer "unclear" if evidence is weak or symmetric.
- Do NOT use stereotypes about cultures; rely on the provided profiles + the fingerprint.
"""
    return prutils.llm_json(client, system=system, user=user, temperature=0.1)
