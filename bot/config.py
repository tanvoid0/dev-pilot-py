# bot/config.py
import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
    "chatgpt_api_key": os.getenv("OPENAI_API_KEY"),
    "ollama_api_key": os.getenv("OLLAMA_API_KEY")
}
