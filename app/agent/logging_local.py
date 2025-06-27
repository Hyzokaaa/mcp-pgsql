import json
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from datetime import datetime

console = Console()

# Estilos para diferentes tipos de logs
blue_border_style = "bold blue"
green_border_style = "bold green"
yellow_border_style = "bold yellow"
magenta_border_style = "bold magenta"

def log_panel(title: str, content: any, border_style: str, log_file: str = "agent_tools.log"):
    """Registra eventos en consola y en archivo de log estructurado"""
    timestamp = datetime.now().isoformat()
    
    # Formato para consola
    panel_content = Text.from_ansi(str(content))
    console.print(Panel(panel_content, title=title, border_style=border_style))
    
    # Formato estructurado para archivo
    log_entry = {
        "timestamp": timestamp,
        "type": title.lower().replace(" ", "_"),
        "content": str(content) if not isinstance(content, dict) else content
    }
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")