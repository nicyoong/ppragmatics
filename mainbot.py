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