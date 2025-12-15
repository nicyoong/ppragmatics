import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

model = "openai/gpt-oss-20b:free"
BASE_URL = "https://openrouter.ai/api/v1"