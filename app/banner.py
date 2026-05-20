import pyfiglet
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("INDEXED", font="small").rstrip()

    art = Text(ascii_art, style="bold #66b3ff")
    subtitle = Text("codebase retrieval, but make it crisp", style="bold #8bd3ff")
    hint = Text("clone  index  ask", style="#7c8aa5")

    banner = Group(
        Align.center(art),
        Text(""),
        Align.center(subtitle),
        Align.center(hint),
    )

    console.clear()
    console.print(
        Panel(
            banner,
            border_style="#315c85",
            padding=(1, 2),
            title="[bold #8bd3ff]INDEXED[/]",
            subtitle="[bold #7c8aa5]CLI[/]",
            expand=True,
        )
    )
