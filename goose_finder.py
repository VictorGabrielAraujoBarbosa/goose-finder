"""
Entry point of Goose Finder.

Use:
    python goose_finder.py <path_or_repository> [options]
"""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from src.cli import configure_stdout, parser_arguments
from src.analyzer import analyse_repository
from src.reporter import print_report


def main() -> None:
    configure_stdout()
    target_repo = parser_arguments()

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"🦆 Investigating commits in [italic]{target_repo}[/italic]...",
            total=None,
        )
        try:
            data = analyse_repository(target_repo, progress=progress, task_id=task)
        except ValueError as exc:
            Console(stderr=True).print(Panel(
                f"[bold]{exc}[/bold]",
                title="[bold red]❌ Invalid Repository[/bold red]",
                border_style="red",
                padding=(0, 2),
            ))
            sys.exit(1)

    print_report(data)


if __name__ == "__main__":
    main()
