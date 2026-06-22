import io
import sys
import argparse

from src.config import VERSION


BANNER = r"""
     __
   >(' )    HONK! Welcome to GOOSE FINDER!
     )/
    /(      "Peace was never an option."
   /  `----/
   \  ~=- /
 ~^~^~^~^~^~^~
"""

MANUAL = f"""
USE:
   python goose_finder.py <path_of_repository> [options]

ARGUMENTS:
   <path_of_repository>       Where to release the goose (local path or git URL)

OPTIONS:
   -h, --help                 Show this message and let it quack at you.
   -v, --version              Displays the current version of the tool (v{VERSION}).

HOW IT WORKS:
   The goose searches the git history for 'Annoyances' (code smells).
   \U0001fabf Gooses: Developers who increase the complexity or size of the code..
   \U0001f9f9 Janitors: Devs who untangle the knots and clean up the mess.
"""


def configure_stdout() -> None:
    """Ensures that stdout uses UTF-8 on any operating system."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def parser_arguments() -> str:
    """
    Parses command-line arguments.

    Returns the path/URL of the target repository.
    Terminates the process (sys.exit) if --help or --version are passed,
    or if no repository is provided.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("target_repo", nargs="?", help="Path of repository (local or URL)")
    parser.add_argument("-h", "--help", action="store_true", help="Shows help")
    parser.add_argument("-v", "--version", action="store_true", help="Shows the actual version")

    args = parser.parse_args()

    if args.version:
        print(f"\U0001fabf  Goose Finder v{VERSION} - 'Honk Edition'")
        print("Developed to prove that peace was never an option in code review.")
        sys.exit(0)

    if args.help or not args.target_repo:
        print(BANNER)
        print(MANUAL)
        sys.exit(0 if args.help else 1)

    return args.target_repo
