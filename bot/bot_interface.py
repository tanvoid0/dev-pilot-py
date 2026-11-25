from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Iterator


class ChatUser(Enum):
    User = "User"
    Bot = "Bot"


class ChatItem:
    # Role - User, Bot
    role: ChatUser
    # Message - message
    message: str
    timestamp: datetime

    def __init__(self, role: ChatUser, message: str, timestamp=datetime.now()):
        self.role = role
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(
            role=data['role'],
            message=data['message'],
            timestamp=data['timestamp']
        )

    def to_json(self):
        return {
            'role': self.role,
            'message': self.message,
            'timestamp': self.timestamp
        }


class ChatHistory:
    messages: [ChatItem] = []

    def __init__(self, user_name='User', bot_name='Dev Bot', system_instruction=None, messages=None):
        if messages is None:
            messages = []
        self.user_name = user_name
        self.bot_name = bot_name
        self.system_instruction = system_instruction
        self.messages = messages

    @classmethod
    def from_json(cls, data):
        return cls(
            user_name=data['user_name'],
            bot_name=data['bot_name'],
            system_instruction=data['system_instruction'],
            messages=[ChatItem.from_json(item) for item in data['history']]
        )

    def to_json(self):
        return {
            'user_name': self.user_name,
            'bot_name': self.bot_name,
            'system_instruction': self.system_instruction,
            'history': [item.to_json() for item in self.messages]
        }


class BotInterface(ABC):
    api_key: str
    history: ChatHistory

    def __init__(self, api_key: str, history: ChatHistory):
        self.api_key = api_key
        self.history = history

    @abstractmethod
    def convert_history(self):
        raise NotImplementedError("This method must be implemented in subclass")

    @abstractmethod
    def send_message(self, message: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def send_message_stream(self, message: str) -> Iterator[str]:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def append_chat(self, chats: [ChatItem]):
        self.history.messages.append(chats)

    def start_interactive_conversation(self):
        while True:
            message = input(f"{self.history.user_name}: ")
            print(f"{self.history.bot_name}: ", end="")
            question = ChatItem(role=ChatUser.User, message=message)
            response = ""
            for message in self.send_message_stream(message):
                print(message, end="")
                response += message
            response = ChatItem(role=ChatUser.Bot, message=response)
            self.append_chat([question, response])
            print("\n")

    def start_conversation(self):
        while True:
            message = input(f"{self.history.user_name}: ")
            print(f"{self.history.bot_name}: ", end="")
            question = ChatItem(role=ChatUser.Bot, message=message)
            response = self.send_message(message)
            print(response, end="")
            response = ChatItem(role=ChatUser.Bot, message=response)
            self.append_chat([question, response])
            print("\n")
