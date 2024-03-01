import sys
import yaml
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton, QMessageBox


class YamlParserApp(QMainWindow):
    def __init__(self):
        super(YamlParserApp, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YAML Parser')
        self.setGeometry(100, 100, 600, 400)

        self.input_text_edit = QTextEdit()
        self.output_label = QLabel()

        parse_button = QPushButton('Parse')
        parse_button.clicked.connect(self.parse_yaml)

        copy_button = QPushButton('Copy')
        copy_button.clicked.connect(self.copy_to_clipboard)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Enter YAML String:'))
        layout.addWidget(self.input_text_edit)
        layout.addWidget(parse_button)
        layout.addWidget(copy_button)
        layout.addWidget(self.output_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def parse_yaml(self):
        input_text = self.input_text_edit.toPlainText()

        try:
            yaml_data = yaml.safe_load(input_text)
            formatted_yaml = self.format_yaml(yaml_data)
            self.output_label.setText(formatted_yaml)
        except yaml.YAMLError as e:
            self.output_label.setText(f'Error parsing YAML: {e}')

    def format_yaml(self, data, indent=0):
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                lines.append(' ' * indent + f'{key}:')
                lines.append(self.format_yaml(value, indent + 2))
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = []
            for item in data:
                lines.append(self.format_yaml(item, indent + 2))
            return '\n'.join(lines)
        elif isinstance(data, str):
            if self.is_yaml_string(data):
                return self.indent_yaml_string(data, indent)
        return ' ' * indent + f'"{data}"'


    def is_yaml_string(self, text):
        try:
            yaml.safe_load(text)
            return True
        except yaml.YAMLError:
            return False

    def indent_yaml_string(self, text, indent):
        lines = text.split('\n')
        indented_lines = [(' ' * indent) + line for line in lines]
        return '\n'.join(indented_lines)

    def copy_to_clipboard(self):
        formatted_text = self.output_label.text()
        QApplication.clipboard().setText(formatted_text)
        QMessageBox.information(self, "Copied", "Formatted YAML copied to clipboard!", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YamlParserApp()
    window.show()
    sys.exit(app.exec_())
