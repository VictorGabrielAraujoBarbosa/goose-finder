"""
Ponto de entrada do Goose Finder.

Uso:
    python goose_finder.py <caminho_do_repositorio> [opções]
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
    repo_alvo = parsear_argumentos()

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"🦆 Investigando commits em [italic]{repo_alvo}[/italic]...",
            total=None,
        )
        dados = analisar_repositorio(repo_alvo, progress=progress, task_id=task)

    imprimir_relatorio(dados)


if __name__ == "__main__":
    main()
