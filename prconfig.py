import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

model = "openai/gpt-oss-20b:free"
BASE_URL = "https://openrouter.ai/api/v1"

politeness_schema = """
You are analyzing politeness pragmatics using the following feature dimensions:

1) Addressee Elevation:
   - explicit (honorifics, titles)
   - implicit (indirect forms)
   - absent

2) Speaker Self-Lowering:
   - grammatical
   - lexical
   - absent

3) Directness Strategy:
   - direct
   - mitigated
   - highly indirect

4) Face Management:
   - positive-face oriented
   - negative-face oriented
   - neutral

5) Politeness Redundancy:
   - low
   - moderate
   - high

6) Obligation Softening:
   - modal-based
   - lexical hedging
   - absent

7) Likelihood of Grammaticalized Politeness Origin:
   - low
   - medium
   - high

Definitions:
- "Grammaticalized politeness origin" means the source language likely encodes politeness via mandatory grammatical
  devices (speech levels, honorific morphology, addressee indexing), not merely optional lexical choices.
"""

def _ensure_env() -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Put it in your .env file:\n"
            "  OPENAI_API_KEY=your_key_here"
        )
    return api_key


def _client() -> OpenAI:
    api_key = _ensure_env()
    return OpenAI(api_key=api_key, base_url=BASE_URL)