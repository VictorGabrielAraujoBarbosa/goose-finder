"""
Report generation for Goose Finder using Rich.

Receives the raw data produced by the analyzer and presents it
to the user in the terminal with tables, panels and semantic colours.
It has no knowledge of PyDriller, analysis logic or CLI arguments.
"""

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# Central console instance — shared by all functions in this module
console = Console()

# Colour thresholds for chaos density (ratio relative to the maximum)
_RED_THRESHOLD = 0.7
_YELLOW_THRESHOLD = 0.3


# ---------------------------------------------------------------------------
# Private helper functions — build Rich components in isolation
# ---------------------------------------------------------------------------

def _density_colour(ratio: float) -> str:
    """Returns the Rich semantic colour for a density ratio."""
    if ratio > _RED_THRESHOLD:
        return "bold red"
    if ratio > _YELLOW_THRESHOLD:
        return "yellow"
    return "dim"


def _build_battlefields_table(battlefields: list) -> Table:
    """Builds the Rich table for the Top 5 Battlefields."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        expand=False,
        padding=(0, 1),
    )
    table.add_column("File", style="white", no_wrap=False, ratio=4)
    table.add_column("Chaos (pts)", justify="right", style="bold")
    table.add_column("LLOC", justify="right")
    table.add_column("Density", justify="right")
    table.add_column("Intensity", justify="left", min_width=22)

    max_density = battlefields[0]['density'] if battlefields else 1.0

    for b in battlefields:
        ratio = b['density'] / max_density if max_density else 0
        colour = _density_colour(ratio)

        full_blocks = int(ratio * 10)
        empty_blocks = 10 - full_blocks
        bar = Text()
        bar.append("█" * full_blocks, style=colour)
        bar.append("░" * empty_blocks, style="bright_black")

        table.add_row(
            Text(b['file'], style=colour),
            Text(str(b['chaos']), style=colour),
            str(b['size']),
            Text(f"{b['density']:.2f} pts/ln", style=colour),
            bar,
        )

    return table


def _build_annoyances_table(annoyances: list) -> Table:
    """Builds the Rich table for the Top 5 Biggest Annoyances."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        expand=False,
        padding=(0, 1),
    )
    table.add_column("#", justify="center", style="bold", width=3)
    table.add_column("Hash", style="magenta", width=8)
    table.add_column("Author", style="white")
    table.add_column("Points", justify="right", style="bold red")
    table.add_column("File", style="white")
    table.add_column("Reasons", style="yellow")
    table.add_column("Commit Message", style="dim", no_wrap=False)

    for i, ann in enumerate(annoyances, 1):
        table.add_row(
            str(i),
            ann['hash'],
            ann['author'],
            f"+{ann['points']}",
            ann['file'],
            ann['reasons'],
            f"\"{ann['commit_message']}\"",
        )

    return table


def _build_hall_of_fame_panel(goose: str, janitor: str) -> Panel:
    """Builds the Rich panel for the Hall of Fame."""
    content = Text()
    content.append("  👑  MASTER GOOSE   ", style="bold red")
    content.append("(Biggest chaos maker) : ", style="dim")
    content.append(f"{goose}\n", style="bold white")

    content.append("  🧹  MASTER JANITOR ", style="bold green")
    content.append("(Biggest cleaner)     : ", style="dim")
    content.append(f"{janitor}", style="bold white")

    return Panel(
        content,
        title="[bold yellow]🏆 Hall of Fame (and Infamy)[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    )


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def print_report(data: dict) -> None:
    """
    Prints the full Goose Finder report from the analyzer data.

    Sections:
        1. Top 5 Battlefields (most chaotic files by density)
        2. Top 5 Biggest Annoyances (worst commits)
        3. Hall of Fame — Master Goose and Master Janitor
    """
    gooses_score = data['gooses_score']
    janitors_score = data['janitors_score']
    battlefields = data['battlefields']
    annoyances_history = data['annoyances_history']

    # Header
    console.print()
    console.print(Panel(
        "[bold]Peace was never an option.[/bold]",
        title="[bold cyan]🪿  GOOSE REPORT[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    # --- Section 1: Battlefields ---
    console.print(Rule("[bold red]🔥 Top 5 Battlefields[/bold red]", style="red"))

    active_battlefields = []
    for filename, stats in battlefields.items():
        if stats['final_size'] > 0:
            density = stats['accumulated_chaos'] / stats['final_size']
            active_battlefields.append({
                'file': filename,
                'density': density,
                'chaos': stats['accumulated_chaos'],
                'size': stats['final_size'],
            })

    if not active_battlefields:
        console.print("  [dim]No problematic files found. Peace reigns. 🕊️[/dim]")
    else:
        active_battlefields.sort(key=lambda x: x['density'], reverse=True)
        console.print(_build_battlefields_table(active_battlefields[:5]))

    # --- Section 2: Biggest Annoyances ---
    console.print()
    console.print(Rule("[bold magenta]💥 Top 5 Biggest Annoyances[/bold magenta]", style="magenta"))

    if not annoyances_history:
        console.print("  [dim]No goose honked loud enough.[/dim]")
    else:
        annoyances_history.sort(key=lambda x: x['points'], reverse=True)
        console.print(_build_annoyances_table(annoyances_history[:5]))

    # --- Section 3: Hall of Fame ---
    console.print()
    winning_goose = (
        max(gooses_score.items(), key=lambda x: x[1])[0]
        if gooses_score else "Nobody"
    )
    winning_janitor = (
        max(janitors_score.items(), key=lambda x: x[1])[0]
        if janitors_score else "Nobody"
    )
    console.print(_build_hall_of_fame_panel(winning_goose, winning_janitor))
    console.print()
