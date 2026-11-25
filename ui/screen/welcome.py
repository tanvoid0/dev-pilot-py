from textual.app import App

from ui.screen.game import Game
from ui.screen.help import Help


class WelcomeApp(App[None]):
    CSS_PATH = 'welcome.tcss'
    SCREENS = {'help', Help}
    BINDINGS = [('ctrl+d', 'toggle_dark', 'Toggle Dark Mode')]
    TITLE = "Dev Pilot - AI"

    def on_mount(self) -> None:
        self.push_screen(Game())
