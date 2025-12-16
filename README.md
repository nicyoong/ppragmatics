# 🧭 Pragmatics Discord Bot

## Overview

This Discord bot analyzes pragmatic meaning in text, defined as how speakers manage politeness, obligation, face, and indirectness, even when that text is written in English or translated into English.

Rather than classifying text or scoring politeness, the bot produces structured analytic output describing:

- What pragmatic strategies are present

- How strongly they are encoded

- Where meaning may be implicit or uncertain

- How a translation preserves or alters pragmatic meaning

The bot is intended for:

- Linguistic research and experimentation

- Translation studies

- Pragmatics and discourse analysis

- Careful inspection of meaning, not automation or moderation

What this bot is not

- Not a politeness score

- Not a language detector

- Not a sentiment or tone analyzer

- Not a cultural stereotype engine

All outputs are interpretive analyses, grounded in explicit theory schemas.

## Commands

`/pragmatics`

Analyze the pragmatic structure of a sentence or short text.

What it does

1. Extracts a pragmatic fingerprint describing:

    - Addressee elevation

    - Speaker self-lowering

    - Directness strategy

    - Face management

    - Politeness redundancy

    - Obligation softening

    - Likelihood of grammaticalized politeness origin

2. Compares that fingerprint against two explicit theory profiles (Language A vs Language B).

This allows you to ask:

- What pragmatic strategies are present?

- Does this English sentence feel “translation-like”?

- Which politeness system better explains the structure?

## How to use

1. Type /pragmatics

2. Paste the text you want to analyze

3. Submit the command

4. Wait for the analysis (requests run serially)

Example input: 

`/pragmatics At your convenience, help me look over this document.`

## Output format

The bot returns one or more messages containing JSON output, split automatically if long.

## Sections

- `input_text`

The original text you submitted.

- `fingerprint.features`

A structured breakdown of pragmatic strategies, each with:

1. a normalized value

2. textual evidence

- `fingerprint.notes`

1. Observations about:

compensatory English strategies

uncertainty or alternative readings

- `attribution`

A comparison between Language A and Language B profiles, including:

a winner (A, B, or unclear)

confidence level

decisive features

diagnostic notes

`/translation_resistance`

Analyze how much pragmatic meaning survives translation into English.

What it does

Compares:

- A source-language sentence

- Its English translation

And determines:

- Which pragmatic features are preserved

- Which are weakened or lost

- Whether English compensates in other ways

This is especially useful for:

- Translation studies

- Cross-linguistic pragmatics

- Identifying “flattened” politeness

## How to use

1. Type `/translation_resistance`

2. Enter:

- `source`: the original text
- `translation`: the English version

3. Submit

## Example

Source:

`你方便的时候帮我看一下这个文件吧。`

Translation:

`When you have time, could you take a look at this document?`

## Output format

JSON output includes:

- `feature_changes`
Per-feature assessment (preserved, weakened, lost, unknown)

- `english_compensation`
Strategies English uses to make up for missing grammatical politeness

- `overall_resistance`
A qualitative assessment (low, medium, high) with rationale

## Execution model (important)

- All analyses run serially

- If multiple commands are sent quickly:

- They queue

- Execute one at a time

- This ensures:

- Deterministic behavior

- Clean experimental conditions

- Rate-limit safety

## Output length & formatting

- Long JSON outputs are automatically split

- No data is truncated

- Outputs can be copy-pasted and recombined

- Future versions may optionally attach JSON files

## Interpretation notes

- Values are theory-relative, not absolute truth

- Ambiguity is preserved and surfaced

- Uncertainty is explicitly noted

- “Unclear” is a valid and meaningful outcome

You are encouraged to:

- Compare multiple variants

- Use minimal pairs

- Treat outputs as hypotheses, not judgments

## Example use cases

- Why does this sentence feel polite but still awkward?

- Which pragmatic features survive translation?

- Is this English sentence compensating for missing honorifics?

- Do two similar sentences differ pragmatically in meaningful ways?

## Privacy & permissions

- The bot does not read messages

- It only processes text explicitly submitted via slash commands

- No message history or user data is accessed

- No data is stored

## Development status

- Designed for research and experimentation

- Stable schemas, evolving theory profiles

- New analytic modules may be added over time
