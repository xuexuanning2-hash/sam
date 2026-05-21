"""Terminal display utilities using Rich."""

import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Force UTF-8 at import time so Rich renders Chinese correctly.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

console = Console(force_terminal=True, legacy_windows=False)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    title = Text("Sam.test", style="bold")
    subtitle = Text("Psychology Experiment System", style="dim italic")
    panel = Panel(
        Align.center(Text.assemble(title, "\n", subtitle)),
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def print_case(content: str) -> None:
    panel = Panel(
        content.strip(),
        title="Case Study",
        title_align="left",
        border_style="yellow",
        padding=(1, 2),
    )
    console.print(panel)


def print_round_header(round_num: int, total: int = 6) -> None:
    console.rule(f"[bold]Round {round_num} / {total}[/bold]", style="dim")


def print_reflection(content: str) -> None:
    """Display Sam's reflection with visual framing."""
    console.print()
    console.rule(
        "[bold bright_cyan]Sam's Reflection[/bold bright_cyan]", style="cyan"
    )
    console.print()
    console.print(content.strip())
    console.print()


def print_response(content: str) -> None:
    """Display Sam's response with visual framing."""
    console.rule(
        "[bold bright_green]Sam's Response[/bold bright_green]", style="green"
    )
    console.print()
    console.print(content.strip())
    console.print()


def print_rating_prompt() -> None:
    """Display the transparency rating screen, visually distinct from chat."""
    console.print()
    console.rule(
        "[bold bright_yellow]Transparency Rating[/bold bright_yellow]", style="yellow"
    )
    console.print()
    console.print(
        "Sam在对话中向您展示其内部思考过程的程度有多高？",
        justify="center",
    )
    console.print()
    console.print("[dim]1 = 完全没有展示[/dim]", justify="center")
    console.print("[dim]7 = 充分展示[/dim]", justify="center")
    console.print()


def get_rating_input() -> str:
    """Get a validated 1-7 rating.  Re-prompts until valid input is given."""
    valid = {"1", "2", "3", "4", "5", "6", "7"}
    while True:
        raw = console.input(
            "\n[bold bright_yellow]请输入 1-7：[/bold bright_yellow] "
        ).strip()
        if raw in valid:
            return raw
        console.print("[red]输入无效，请输入 1 到 7 之间的数字。[/red]")


def print_goodbye(participant_id: str, group: str) -> None:
    console.print()
    console.rule("[bold]Experiment Complete[/bold]", style="bright_blue")
    console.print(
        f"\n  Participant: [bold]{participant_id}[/bold]"
        f"\n  Group:       [bold]{group}[/bold]"
        f"\n\n  Data saved to [dim]data/{participant_id}.csv[/dim]"
        f"\n\n  Thank you for your participation.\n",
        justify="center",
    )


def get_user_input() -> str:
    console.print()
    return console.input("[bold bright_blue]You:[/bold bright_blue] ").strip()
