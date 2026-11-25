from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class MessageBubble(QWidget):
    def __init__(self, text, is_user_message, timestamp, name):
        super().__init__()

        # Create and configure the layout for the bubble
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a label to show the message content
        message_label = QLabel(f"<b>{name} [{timestamp}]:</b><br>{text}")
        message_label.setWordWrap(True)  # Ensure text wraps within the bubble
        message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply layout to the bubble
        layout.addWidget(message_label)

        # Set style based on message type
        self.apply_styles(is_user_message)

    def apply_styles(self, is_user_message):
        # Configure the bubble appearance
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Set background color and other styling properties
        if is_user_message:
            self.setStyleSheet("""
                background-color: #e0f7fa;
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
                text-align: right;
            """)
        else:
            self.setStyleSheet("""
                background-color: #f1f8e9;
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
                text-align: left;
            """)

        # Optional: Set the minimum height of the bubble for better visibility
        self.setMinimumHeight(40)
