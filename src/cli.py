import io
import sys
import argparse

from src.config import VERSION


BANNER = r"""
     __
   >(' )    HONK! Bem-vindo ao GOOSE FINDER!
     )/
    /(      "Peace was never an option."
   /  `----/
   \  ~=- /
 ~^~^~^~^~^~^~
"""

MANUAL = f"""
USO:
   python goose_finder.py <caminho_do_repositorio> [opções]

ARGUMENTOS:
   <caminho_do_repositorio>   Onde soltar o ganso (caminho local ou URL do git)

OPÇÕES:
   -h, --help                 Mostra essa mensagem e grasna para você.
   -v, --version              Mostra a versão atual da ferramenta (v{VERSION}).

COMO FUNCIONA:
   O ganso vasculha o historico do git em busca de 'Annoyances' (code smells).
   \U0001fabf Gansos (Gooses): Devs que aumentam a complexidade ou tamanho do codigo.
   \U0001f9f9 Zeladores (Janitors): Devs que desatam os nos e limpam a baguna.
"""


def configurar_stdout() -> None:
    """Garante que o stdout usa UTF-8 em qualquer sistema operacional."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def parsear_argumentos() -> str:
    """
    Faz o parsing dos argumentos da linha de comando.

    Retorna o caminho/URL do repositório alvo.
    Encerra o processo (sys.exit) se --help ou --version forem passados,
    ou se nenhum repositório for fornecido.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("repo_alvo", nargs="?", help="Caminho do repositório (local ou URL)")
    parser.add_argument("-h", "--help", action="store_true", help="Mostra a ajuda")
    parser.add_argument("-v", "--version", action="store_true", help="Mostra a versão")

    args = parser.parse_args()

    if args.version:
        print(f"\U0001fabf  Goose Finder v{VERSION} - 'Honk Edition'")
        print("Desenvolvido para provar que a paz nunca foi uma opcao no code review.")
        sys.exit(0)

    if args.help or not args.repo_alvo:
        print(BANNER)
        print(MANUAL)
        sys.exit(0 if args.help else 1)

    return args.repo_alvo
