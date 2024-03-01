import difflib
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QTextBrowser


class DiffApp(QMainWindow):
    def __init__(self):
        super(DiffApp, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.text_edit1 = QTextEdit()
        self.text_edit2 = QTextEdit()
        self.text_edit1.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_edit2.setLineWrapMode(QTextEdit.WidgetWidth)

        compare_button = QPushButton('Compare', self)
        compare_button.clicked.connect(self.compare_texts)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit1)
        layout.addWidget(self.text_edit2)
        layout.addWidget(compare_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Text Diff Checker')
        self.show()

    def compare_texts(self):
        text1 = self.text_edit1.toPlainText()
        text2 = self.text_edit2.toPlainText()

        differ = difflib.Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

        diff_html = self.generate_diff_html(diff)
        self.show_diff_result(diff_html)

    def generate_diff_html(self, diff):
        html = "<html><body><pre>"
        for line in diff:
            if line.startswith('  '):
                html += line[2:] + "<br>"
            elif line.startswith('- '):
                html += f'<span style="color:red;">{line[2:]}</span><br>'
            elif line.startswith('+ '):
                html += f'<span style="color:green;">{line[2:]}</span><br>'
        html += "</pre></body></html>"
        return html

    def show_diff_result(self, diff_html):
        result_window = QMainWindow(self)
        result_text_browser = QTextBrowser(result_window)
        result_text_browser.setHtml(diff_html)
        result_text_browser.setLineWrapMode(QTextEdit.WidgetWidth)  # Set line wrap mode

        result_window.setCentralWidget(result_text_browser)
        result_window.setGeometry(200, 200, 800, 600)
        result_window.setWindowTitle('Text Diff Result')
        result_window.show()

    @staticmethod
    def launch():
        app = QApplication([])
        window = DiffApp()
        app.exec_()


if __name__ == '__main__':
    DiffApp.launch()