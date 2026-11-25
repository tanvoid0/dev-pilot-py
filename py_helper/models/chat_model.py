class ChatItem:
    def __init__(self, role, parts, timestamp):
        self.role = role
        self.parts = parts
        self.timestamp = timestamp

    @classmethod
    def from_json(cls, data):
        return cls(
            role=data['role'],
            parts=data['parts'],
            timestamp=data['timestamp']
        )

    def to_json(self):
        return {
            'role': self.role,
            'parts': self.parts,
            'timestamp': self.timestamp
        }


class ChatHistory:
    history: [ChatItem] = []

    def __init__(self, user_name='User', bot_name='Dev Bot', system_instruction=None, history=None):
        if history is None:
            history = []
        self.user_name = user_name
        self.bot_name = bot_name
        self.system_instruction = system_instruction
        self.history = history

    @classmethod
    def from_json(cls, data):
        return cls(
            user_name=data['user_name'],
            bot_name=data['bot_name'],
            system_instruction=data['system_instruction'],
            history=[ChatItem.from_json(item) for item in data['history']]
        )

    def to_json(self):
        return {
            'user_name': self.user_name,
            'bot_name': self.bot_name,
            'system_instruction': self.system_instruction,
            'history': [item.to_json() for item in self.history]
        }
