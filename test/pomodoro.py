from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Label


class PomodoroApp(App):
    """A simple Pomodoro timer."""

    CSS_PATH = "pomodoro.tcss"

    # Timer states and durations (non-reactive for time values)
    work_duration = 25 * 60  # 25 minutes
    short_break_duration = 5 * 60  # 5 minutes
    long_break_duration = 15 * 60  # 15 minutes
    current_time = work_duration  # Starts with work duration
    session_count = 0
    is_running = var(False)  # Reactive to control the start/stop button state
    session_type = var("Work")  # Reactive to update the session label

    def watch_current_time(self, value: int) -> None:
        """Updates the timer display when current_time changes."""
        mins, secs = divmod(value, 60)
        self.query_one("#timer_label", Label).update(f"{mins:02}:{secs:02}")

    def watch_session_type(self, session: str) -> None:
        """Updates the session label to show Work or Break."""
        self.query_one("#session_label", Label).update(session)

    def compose(self) -> ComposeResult:
        """Compose the UI components."""
        with Container(id="pomodoro_container"):
            yield Label("Pomodoro Timer", id="title")
            yield Label("25:00", id="timer_label")
            yield Label("Work", id="session_label")
            with Container(id="controls"):
                yield Button("Start", id="start_button", action="start_timer")
                yield Button("Stop", id="stop_button", action="stop_timer")
                yield Button("Reset", id="reset_button", action="reset_timer")

    @on(Button.Pressed, "#start_button")
    def start_timer(self) -> None:
        """Starts the timer countdown."""
        if not self.is_running:
            self.is_running = True
            self.timer = self.set_interval(1, self.update_timer)  # Start the timer to tick every second

    @on(Button.Pressed, "#stop_button")
    def stop_timer(self) -> None:
        """Stops the timer."""
        self.is_running = False
        if hasattr(self, "timer"):
            self.timer.stop()  # Stop the timer interval if it exists

    @on(Button.Pressed, "#reset_button")
    def reset_timer(self) -> None:
        """Resets the timer to the initial state."""
        self.stop_timer()
        self.session_count = 0
        self.session_type = "Work"
        self.current_time = self.work_duration
        self.watch_current_time(self.current_time)  # Trigger UI update manually

    def update_timer(self) -> None:
        """Handles the countdown and session transitions."""
        if self.current_time > 0:
            self.current_time -= 1
            self.watch_current_time(self.current_time)  # Update the display
        else:
            self.session_count += 1
            self.switch_session()

    def switch_session(self) -> None:
        """Switches between work, short break, and long break sessions."""
        self.is_running = False
        if hasattr(self, "timer"):
            self.timer.stop()  # Stop the current timer interval

        if self.session_count % 8 == 0:
            self.current_time = self.long_break_duration
            self.session_type = "Long Break"
        elif self.session_count % 2 == 0:
            self.current_time = self.short_break_duration
            self.session_type = "Short Break"
        else:
            self.current_time = self.work_duration
            self.session_type = "Work"

        self.watch_current_time(self.current_time)  # Update time display
        self.start_timer()  # Automatically start the next session


if __name__ == "__main__":
    PomodoroApp().run()
