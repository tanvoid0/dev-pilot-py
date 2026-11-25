# bot/factory.py
from bot.bot_interface import BotInterface, ChatHistory
from bot.gemini_bot import GeminiBot


class BotFactory:
    def __init__(self, config):
        self.config = config

    def create_bot(self, bot_type: str, history: ChatHistory) -> BotInterface:
        if bot_type == "gemini":
            return GeminiBot(self.config["gemini_api_key"], history)
        # elif bot_type == "chatgpt":
        #     return ChatGPTBot(self.config["chatgpt_api_key"])
        # elif bot_type == "ollama":
        #     return OllamaBot(self.config["ollama_api_key"])
        else:
            raise ValueError(f"Unsupported bot type: {bot_type}")
