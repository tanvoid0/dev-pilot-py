from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label
from typing_extensions import Final


class GameHeader(Widget):
    """Header for the game.

    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    moves = reactive(0)
    """int: Keep track of how many moves the player has made."""

    filled = reactive(0)
    """int: Keep track of how many cells are filled."""

    def compose(self) -> ComposeResult:
        """Compose the game header.

        Returns:
            ComposeResult: The result of composing the game header.
        """
        with Horizontal():
            yield Label(self.app.title, id="app-title")
            yield Label(id="moves")
            yield Label(id="progress")

    def watch_moves(self, moves: int):
        """Watch the moves reactive and update when it changes.

        Args:
            moves (int): The number of moves made.
        """
        self.query_one("#moves", Label).update(f"Moves: {moves}")

    def watch_filled(self, filled: int):
        """Watch the on-count reactive and update when it changes.

        Args:
            filled (int): The number of cells that are currently on.
        """
        self.query_one("#progress", Label).update(f"Filled: {filled}")


class Game(Screen):
    SIZE: Final = 5

    def compose(self) -> ComposeResult:
        yield GameHeader
