from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Markdown


class Help(Screen):
    BINDINGS = [('escape,space,q,question_mark', 'app.pop_screen', 'Close')]

    def compose(self) -> ComposeResult:
        ## Reads The File's Help.md e.g., if used on app.py it'll read app.md
        yield Markdown(Path(__file__).with_suffix(".md").read_text())
