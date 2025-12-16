import json
import textwrap
import discord
import os
from discord import app_commands
from dotenv import load_dotenv

import pragmatics
import prconfig

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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

@tree.command(
    name="pragmatics",
    description="Analyze pragmatic fingerprint and attribute Language A vs B"
)
@app_commands.describe(
    text="English text (possibly translated)"
)
async def pragmatics_command(interaction: discord.Interaction, text: str):
    await interaction.response.defer(thinking=True)

    try:
        pr_client = prconfig._client()

        fingerprint = pragmatics.extract_pragmatic_fingerprint(
            pr_client,
            text,
            language_context="English (possibly translated)"
        )

        attribution = pragmatics.attribute_language_A_vs_B(
            pr_client,
            fingerprint,
            language_A_profile,
            language_B_profile
        )

        response = {
            "input_text": text,
            "fingerprint": fingerprint,
            "attribution": attribution
        }

        # Discord messages max ~2000 chars → format carefully
        output = json.dumps(response, ensure_ascii=False, indent=2)

        if len(output) > 1900:
            output = output[:1900] + "\n… (truncated)"

        await interaction.followup.send(f"```json\n{output}\n```")

    except Exception as e:
        await interaction.followup.send(f"❌ Error: `{e}`")

@tree.command(
    name="translation_resistance",
    description="Analyze translation resistance between source and translation"
)
@app_commands.describe(
    source="Original text",
    translation="Translated text"
)
async def translation_resistance_command(
    interaction: discord.Interaction,
    source: str,
    translation: str
):
    await interaction.response.defer(thinking=True)

    pr_client = prconfig._client()

    result = pragmatics.analyze_translation_resistance(
        pr_client,
        source,
        translation,
        source_language_context="unknown"
    )

    output = json.dumps(result, ensure_ascii=False, indent=2)
    await interaction.followup.send(f"```json\n{output}\n```")