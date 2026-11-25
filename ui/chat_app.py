from dotenv import load_dotenv

load_dotenv()

import sys

import markdown2
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, \
    QLabel, QSizePolicy

from py_helper.bot.bot_interface import BotInterface
from py_helper.bot.gemini_bot import GeminiBot
# Import the ChatHistory and ChatItem classes
from py_helper.models.chat_model import ChatHistory, ChatItem
from py_helper.service.config_file_service import ConfigFileService


class AvatarLabel(QLabel):
    def __init__(self, avatar_text: str, background_color: QColor, parent=None):
        super().__init__(parent)
        self.avatar_text = avatar_text
        self.background_color = background_color
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QBrush(self.background_color))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(QColor('white'), 2))
        painter.setFont(QFont('Arial', 18))
        painter.drawText(self.rect(), Qt.AlignCenter, self.avatar_text)


class MessageBubble(QWidget):
    def __init__(self, text: str, is_user_message: bool, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_user_message = is_user_message
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        self.label = QLabel()
        self.label.setTextFormat(Qt.RichText)
        self.label.setText(markdown2.markdown(self.text, extras=['code-friendly']))
        self.label.setWordWrap(True)
        self.label.setFont(QFont('Arial', 10))
        # Adjust size policy to control label's behavior
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        layout.addWidget(self.label)

        self.setLayout(layout)
        # Adjust size policy to control bubble's behavior
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # Style based on message role
        if self.is_user_message:
            self.setStyleSheet("background-color: #e0f7fa; border-radius: 15px; padding: 10px;")
        else:
            self.setStyleSheet("background-color: #f1f8e9; border-radius: 15px; padding: 10px;")


class ChatItemWidget(QWidget):
    def __init__(self, chat_item: ChatItem, is_user_message: bool):
        super().__init__()
        self.chat_item = chat_item
        self.is_user_message = is_user_message
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)  # Align items to the top of the row
        self.setLayout(layout)

        # Create avatar label
        avatar_text = '👤' if self.is_user_message else '🤖'
        background_color = QColor('#00796b') if self.is_user_message else QColor('#009688')
        avatar = AvatarLabel(avatar_text, background_color)

        # Create message bubble
        message_bubble = MessageBubble(self.chat_item.parts, self.is_user_message)

        if self.is_user_message:
            layout.addStretch()
            layout.addWidget(message_bubble)
            layout.addWidget(avatar)
        else:
            layout.addWidget(avatar)
            layout.addWidget(message_bubble)
            layout.addStretch()


class ChatbotUI(QWidget):
    config_file_service = ConfigFileService()
    chat_history = None
    bot: BotInterface = None

    def __init__(self):
        super().__init__()

        # Load chat history from file
        self.load_chat_history()
        self.bot = GeminiBot(self.chat_history)

        # Initialize UI components
        self.initUI()

        # Display chat history in message_container
        for item in self.chat_history.history:
            self.append_message(item)

    def initUI(self):
        # Create widgets
        self.message_container = QWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.message_container)
        self.scroll_area.setWidgetResizable(True)

        self.text_input = QLineEdit()
        self.send_button = QPushButton('Send')

        # Create layouts
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Add widgets to layouts
        hbox.addWidget(self.text_input)
        hbox.addWidget(self.send_button)

        vbox.addWidget(self.scroll_area)
        vbox.addLayout(hbox)

        # Set the main layout
        self.setLayout(vbox)

        # Set window properties
        self.setWindowTitle('Personal Chatbot')
        self.setGeometry(100, 100, 600, 400)

        # Connect button click event to a slot
        self.send_button.clicked.connect(self.on_send_button_click)

        # Connect Enter key press to Send button
        self.text_input.returnPressed.connect(self.on_send_button_click)

    def append_message(self, chat_item: ChatItem):
        is_user_message = chat_item.role == 'user'
        item_widget = ChatItemWidget(chat_item, is_user_message)

        # Create a container widget for the message
        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_widget.setLayout(container_layout)

        # Add the item widget to the container layout
        container_layout.addWidget(item_widget)

        # Create a horizontal layout to align the message widget
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if is_user_message:
            layout.addStretch()
            layout.addWidget(container_widget)
        else:
            layout.addWidget(container_widget)
            layout.addStretch()

        # Create a container widget for the message
        message_container_widget = QWidget()
        message_container_widget.setLayout(layout)

        # Add the message container widget to the message container
        current_layout = self.message_container.layout()
        if current_layout is None:
            current_layout = QVBoxLayout()
            self.message_container.setLayout(current_layout)
        current_layout.addWidget(message_container_widget)

        # Ensure the scroll area scrolls to the bottom
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def on_send_button_click(self):
        user_text = self.text_input.text()
        if user_text:
            timestamp = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')

            # Create and append user message
            user_message = ChatItem(
                role='user',
                parts=user_text,
                timestamp=timestamp
            )
            self.append_message(user_message)

            # Add user message to history
            self.chat_history.history.append(user_message)

            # Placeholder for bot response
            bot_response = self.bot.process(user_text, None)

            # Create and append bot message
            bot_message = ChatItem(
                role='model',
                parts=bot_response,
                timestamp=timestamp
            )
            self.append_message(bot_message)

            # Add bot response to history
            self.chat_history.history.append(bot_message)

            # Save chat history
            self.save_chat_history()

            # Clear input field
            self.text_input.clear()

    def save_chat_history(self):
        # Save chat history to JSON file
        self.config_file_service.save_bot_chat_history(self.chat_history.to_json())

    def load_chat_history(self):

        # Load chat history from JSON file
        try:
            data = self.config_file_service.get_chat_history()
        except FileNotFoundError:
            data = ChatHistory().to_json()
        self.chat_history = ChatHistory.from_json(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot = ChatbotUI()
    chatbot.show()
    sys.exit(app.exec_())
