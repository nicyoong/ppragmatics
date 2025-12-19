import asyncio
import json
import textwrap
import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import pragmatics
import prconfig
import prutils

load_dotenv()
analysis_lock = asyncio.Lock()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="p!",
    intents=intents
)
tree = bot.tree

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

def split_message(text: str, limit: int = 1900):
    """
    Splits text into chunks that fit within Discord's message limit.
    Leaves room for code block markers.
    """
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks

async def run_pragmatics(text: str):
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

    return {
        "input_text": text,
        "fingerprint": fingerprint,
        "attribution": attribution
    }

@tree.command(
    name="pragmatics",
    description="Analyze pragmatic fingerprint and attribute Language A vs B"
)
@app_commands.describe(text="English text (possibly translated)")
async def pragmatics_slash(
    interaction: discord.Interaction,
    text: str
):
    await interaction.response.defer(thinking=True)

    async with analysis_lock:
        try:
            result = await run_pragmatics(text)
            output = json.dumps(result, ensure_ascii=False, indent=2)

            for chunk in split_message(output):
                await interaction.followup.send(f"```json\n{chunk}\n```")

        except Exception as e:
            await interaction.followup.send(f"❌ Error: `{e}`")

@bot.command(name="pragmatics")
async def pragmatics_prefix(
    ctx: commands.Context,
    *,
    text: str
):
    async with ctx.typing():
        async with analysis_lock:
            try:
                result = await run_pragmatics(text)
                output = json.dumps(result, ensure_ascii=False, indent=2)

                for chunk in split_message(output):
                    await ctx.send(f"```json\n{chunk}\n```")

            except Exception as e:
                await ctx.send(f"❌ Error: `{e}`")

async def run_translation_resistance(source: str, translation: str):
    pr_client = prconfig._client()

    return pragmatics.analyze_translation_resistance(
        pr_client,
        source,
        translation,
        source_language_context="unknown"
    )

@tree.command(
    name="translationresistance",
    description="Analyze translation resistance between source and translation"
)
@app_commands.describe(
    source="Original text",
    translation="Translated text"
)
async def translation_resistance_slash(
    interaction: discord.Interaction,
    source: str,
    translation: str
):
    await interaction.response.defer(thinking=True)

    async with analysis_lock:
        try:
            result = await run_translation_resistance(source, translation)
            output = json.dumps(result, ensure_ascii=False, indent=2)

            chunks = split_message(output)
            for i, chunk in enumerate(chunks, start=1):
                await interaction.followup.send(
                    f"**Part {i}/{len(chunks)}**\n```json\n{chunk}\n```"
                )

        except Exception as e:
            await interaction.followup.send(f"❌ Error: `{e}`")

@bot.command(name="translationresistance")
async def translation_resistance_prefix(
    ctx: commands.Context,
    *,
    args: str
):
    """
    Usage:
    p!translation_resistance <source text> ||| <translation text>
    """

    if "|||" not in args:
        await ctx.send(
            "❌ Usage:\n"
            "`p!translation_resistance <source text> ||| <translation text>`"
        )
        return

    source, translation = map(str.strip, args.split("|||", 1))

    async with ctx.typing():
        async with analysis_lock:
            try:
                result = await run_translation_resistance(source, translation)
                output = json.dumps(result, ensure_ascii=False, indent=2)

                chunks = split_message(output)
                for i, chunk in enumerate(chunks, start=1):
                    await ctx.send(
                        f"**Part {i}/{len(chunks)}**\n```json\n{chunk}\n```"
                    )

            except Exception as e:
                await ctx.send(f"❌ Error: `{e}`")

@bot.event
async def on_ready():
    asyncio.create_task(prutils.checktime())
    await tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)
