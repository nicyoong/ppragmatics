import json
import pragmatics
import prconfig
import sys
import textwrap

def run_demo():
    client = prconfig._client()

    # -------------------------
    # Test strings (edit freely)
    # -------------------------
    english_text_1 = "When you have time, could you take a look at this document?"
    english_text_2 = "If it’s convenient for you, could I trouble you to take a look at this document?"

    # Language A / B profiles are THEORY PRIORS you write.
    # Later you’ll replace these with real, well-sourced profiles.
    language_A_profile = textwrap.dedent("""
    Language A (Northern Mandarin–leaning):
    - Politeness primarily pragmatic and contextual
    - Fewer explicit imposition-softening expressions
    - Sentence-final particles used for mitigation
    - Moderate politeness redundancy
    """).strip()

    language_B_profile = textwrap.dedent("""
    Language B (Southern Mandarin–leaning):
    - Politeness often expressed through lexical softeners
    - Frequent use of conditional framing
    - Higher politeness redundancy
    - Stronger explicit mitigation of imposition
    """).strip()

    # -------------------------
    # 1) Fingerprints
    # -------------------------
    fp1 = pragmatics.extract_pragmatic_fingerprint(client, english_text_1, language_context="English (possibly translated)")
    fp2 = pragmatics.extract_pragmatic_fingerprint(client, english_text_2, language_context="English (possibly translated)")

    # -------------------------
    # 2) Attribution
    # -------------------------
    attrib1 = pragmatics.attribute_language_A_vs_B(client, fp1, language_A_profile, language_B_profile)
    attrib2 = pragmatics.attribute_language_A_vs_B(client, fp2, language_A_profile, language_B_profile)

    # -------------------------
    # Print results
    # -------------------------
    print("\n=== TEXT 1 ===")
    print(english_text_1)
    print("\n--- Fingerprint (JSON) ---")
    print(json.dumps(fp1, ensure_ascii=False, indent=2))
    print("\n--- Attribution (JSON) ---")
    print(json.dumps(attrib1, ensure_ascii=False, indent=2))

    print("\n\n=== TEXT 2 ===")
    print(english_text_2)
    print("\n--- Fingerprint (JSON) ---")
    print(json.dumps(fp2, ensure_ascii=False, indent=2))
    print("\n--- Attribution (JSON) ---")
    print(json.dumps(attrib2, ensure_ascii=False, indent=2))

    # -------------------------
    # Optional: translation resistance demo
    # (Replace source_text with real Language A/B text when you have it)
    # -------------------------
    source = "你方便的时候帮我看一下这个文件吧。"
    translation = "When you have time, could you take a look at this document?"
    resistance = pragmatics.analyze_translation_resistance(client, source, translation, source_language_context="unknown")

    print("\n\n=== TRANSLATION RESISTANCE DEMO ===")
    print("\n--- Resistance (JSON) ---")
    print(json.dumps(resistance, ensure_ascii=False, indent=2))
