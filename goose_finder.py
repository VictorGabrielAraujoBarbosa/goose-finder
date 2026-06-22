"""
Entry point of Goose Finder.

Use:
    python goose_finder.py <path_or_repository> [options]
"""

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from src.cli import configurar_stdout, parsear_argumentos
from src.analyzer import analisar_repositorio
from src.reporter import imprimir_relatorio


def main() -> None:
    configurar_stdout()
    target_repo = parsear_argumentos()

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
        data = analisar_repositorio(target_repo, progress=progress, task_id=task)

    imprimir_relatorio(data)


if __name__ == "__main__":
    main()
