"""
Goose Finder — Ponto de entrada principal.

"Peace was never an option."
"""

from src.cli import configurar_stdout, parsear_argumentos
from src.analyzer import analisar_repositorio
from src.reporter import imprimir_relatorio


def main() -> None:
    configurar_stdout()

    repo_alvo = parsear_argumentos()

    print(f"🦆 O ganso está investigando furtivamente o repositório: {repo_alvo}...")
    print("⏳ Isso pode levar um tempo dependendo do tamanho da bagunça...\n")

    dados = analisar_repositorio(repo_alvo)
    imprimir_relatorio(dados)


if __name__ == "__main__":
    main()
