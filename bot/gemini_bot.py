import os
import time
from typing import Iterator

import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerationConfigType, GenerateContentResponse

from bot.bot_interface import BotInterface, ChatHistory, ChatItem, ChatUser


class GeminiBot(BotInterface):
    generation_config: GenerationConfigType = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model: GenerativeModel = None

    # Configure Gemini API key from environment
    def __init__(self, api_key, history: ChatHistory):
        super().__init__(api_key, history)

        genai.configure(api_key=self.api_key)
        self.update_model()
        # Start chat session with formatted history
        self.chat_session = self.model.start_chat(history=self.convert_history())

    def update_model(self):
        self.model = GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction=self.history.system_instruction,
        )

    def convert_history(self):
        items = []
        for item in self.history.messages:
            chat_item = {'role': 'user' if item['role'] == ChatUser.User.value else 'model', 'parts': [item['message']]}
            items.append(chat_item)
        return items

    def send_message(self, message: str) -> str:
        response: GenerateContentResponse = self.chat_session.send_message(message)
        return response.text

    def send_message_stream(self, message: str) -> Iterator[str]:
        response: GenerateContentResponse = self.model.generate_content(message, stream=True)
        for chunk in response:
            yield chunk.text
