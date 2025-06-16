# logging_local.py
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
import json

blue_border_style = Style(color="#0EA5E9")
green_border_style = Style(color="#10B981")

console = Console()

def log_panel(
        title: str,
        content: str | dict,
        border_style: Style = blue_border_style,
):
    # Si content es dict, lo formateamos como JSON legible
    text = json.dumps(content, indent=2, default=str) if isinstance(content, dict) else content
    console.log(
        Panel(
            text,
            title=title,
            border_style=border_style,
            expand=False
        )
    )
