from contextlib import contextmanager

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text
from rich.theme import Theme


@contextmanager
def bar():
    with Progress(
        SpinnerColumn(finished_text=":dna:"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    ) as progress:
        yield progress


class RichLogger:
    def __init__(self, console):
        self.console = console

    def info(self, message, with_panel=False):
        if with_panel:
            self._print_panel(message, "info")
        else:
            self.console.print(message, style="info")

    def error(self, message, with_panel=False):
        if with_panel:
            self._print_panel(message, "error")
        else:
            self.console.print(message, style="error")

    def warning(self, message, with_panel=False):
        if with_panel:
            self._print_panel(message, "warning")
        else:
            self.console.print(message, style="warning")

    def fancy(self, message, with_panel=False):
        if with_panel:
            self._print_panel(message, "fancy")
        else:
            self.console.print(message, style="fancy")

    def _print_panel(self, message, style):
        panel_text = "panel_text_" + style
        panel_border = "panel_border_" + style

        text = Text.from_markup(message, justify="center", style=panel_text)
        panel = Panel(
            text,
            border_style=panel_border,
            expand=False,
            box=box.ROUNDED,
        )
        self.console.print(panel)


custom_theme = Theme(
    {
        "info": "white",
        "error": "bold red",
        "warning": "yellow",
        "fancy": "bold cyan",
        "panel_border_info": "green",
        "panel_border_error": "bright_red",
        "panel_border_warning": "bright_yellow",
        "panel_border_fancy": "bright_cyan",
        "panel_text_info": "white",
        "panel_text_error": "bold red",
        "panel_text_warning": "yellow",
        "panel_text_fancy": "bright_cyan",
    }
)


console = Console(theme=custom_theme)
log = RichLogger(console)
