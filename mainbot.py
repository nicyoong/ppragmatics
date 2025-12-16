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