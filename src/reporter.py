"""
Geração do relatório do Goose Finder usando Rich.

Recebe os dados brutos produzidos pelo analyzer e os apresenta
ao usuário no terminal com tabelas, painéis e cores semânticas.
Não conhece PyDriller, lógica de análise ou argumentos de CLI.
"""

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# Instância central de console — compartilhada por todas as funções deste módulo
console = Console()

# Limiar de cores para densidade de caos (proporção em relação ao máximo)
_LIMIAR_VERMELHO = 0.7
_LIMIAR_AMARELO = 0.3


# ---------------------------------------------------------------------------
# Funções auxiliares privadas — constroem componentes Rich isoladamente
# ---------------------------------------------------------------------------

def _cor_densidade(proporcao: float) -> str:
    """Retorna a cor semântica Rich para uma proporção de densidade."""
    if proporcao > _LIMIAR_VERMELHO:
        return "bold red"
    if proporcao > _LIMIAR_AMARELO:
        return "yellow"
    return "dim"


def _construir_tabela_batalhas(batalhas: list) -> Table:
    """Constrói a tabela Rich de Top 5 Campos de Batalha."""
    tabela = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        expand=False,
        padding=(0, 1),
    )
    tabela.add_column("Arquivo", style="white", no_wrap=False, ratio=4)
    tabela.add_column("Caos (pts)", justify="right", style="bold")
    tabela.add_column("LLOC", justify="right")
    tabela.add_column("Densidade", justify="right")
    tabela.add_column("Intensidade", justify="left", min_width=22)

    max_densidade = batalhas[0]['densidade'] if batalhas else 1.0

    for b in batalhas:
        proporcao = b['densidade'] / max_densidade if max_densidade else 0
        cor = _cor_densidade(proporcao)

        blocos_cheios = int(proporcao * 10)
        blocos_vazios = 10 - blocos_cheios
        barra = Text()
        barra.append("█" * blocos_cheios, style=cor)
        barra.append("░" * blocos_vazios, style="bright_black")

        tabela.add_row(
            Text(b['arquivo'], style=cor),
            Text(str(b['caos']), style=cor),
            str(b['tamanho']),
            Text(f"{b['densidade']:.2f} pts/ln", style=cor),
            barra,
        )

    return tabela


def _construir_tabela_annoyances(annoyances: list) -> Table:
    """Constrói a tabela Rich de Top 5 Maiores Annoyances."""
    tabela = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        expand=False,
        padding=(0, 1),
    )
    tabela.add_column("#", justify="center", style="bold", width=3)
    tabela.add_column("Hash", style="magenta", width=8)
    tabela.add_column("Autor", style="white")
    tabela.add_column("Pontos", justify="right", style="bold red")
    tabela.add_column("Arquivo", style="white")
    tabela.add_column("Motivos", style="yellow")
    tabela.add_column("Mensagem do Commit", style="dim", no_wrap=False)

    for i, ann in enumerate(annoyances, 1):
        tabela.add_row(
            str(i),
            ann['hash'],
            ann['autor'],
            f"+{ann['pontos']}",
            ann['arquivo'],
            ann['motivos'],
            f"\"{ann['mensagem_commit']}\"",
        )

    return tabela


def _construir_panel_hall_da_fama(goose: str, janitor: str) -> Panel:
    """Constrói o painel Rich do Hall da Fama."""
    conteudo = Text()
    conteudo.append("  👑  MASTER GOOSE   ", style="bold red")
    conteudo.append("(Maior causador de caos) : ", style="dim")
    conteudo.append(f"{goose}\n", style="bold white")

    conteudo.append("  🧹  MASTER JANITOR ", style="bold green")
    conteudo.append("(Maior limpador)         : ", style="dim")
    conteudo.append(f"{janitor}", style="bold white")

    return Panel(
        conteudo,
        title="[bold yellow]🏆 Hall da Fama (e da Infâmia)[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    )


# ---------------------------------------------------------------------------
# Função pública principal
# ---------------------------------------------------------------------------

def imprimir_relatorio(dados: dict) -> None:
    """
    Imprime o relatório completo do Goose Finder a partir dos dados do analyzer.

    Seções:
        1. Top 5 Campos de Batalha (arquivos mais caóticos por densidade)
        2. Top 5 Maiores Annoyances (piores commits)
        3. Hall da Fama — Master Goose e Master Janitor
    """
    placar_gooses = dados['placar_gooses']
    placar_janitors = dados['placar_janitors']
    campos_de_batalha = dados['campos_de_batalha']
    historico_annoyances = dados['historico_annoyances']

    # Cabeçalho
    console.print()
    console.print(Panel(
        "[bold]Peace was never an option.[/bold]",
        title="[bold cyan]🪿  GOOSE REPORT[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    # --- Seção 1: Campos de Batalha ---
    console.print(Rule("[bold red]🔥 Top 5 Campos de Batalha[/bold red]", style="red"))

    batalhas_ativas = []
    for arq, stats in campos_de_batalha.items():
        if stats['tamanho_final'] > 0:
            densidade = stats['caos_acumulado'] / stats['tamanho_final']
            batalhas_ativas.append({
                'arquivo': arq,
                'densidade': densidade,
                'caos': stats['caos_acumulado'],
                'tamanho': stats['tamanho_final'],
            })

    if not batalhas_ativas:
        console.print("  [dim]Nenhum arquivo problemático encontrado. Paz reina. 🕊️[/dim]")
    else:
        batalhas_ativas.sort(key=lambda x: x['densidade'], reverse=True)
        console.print(_construir_tabela_batalhas(batalhas_ativas[:5]))

    # --- Seção 2: Maiores Annoyances ---
    console.print()
    console.print(Rule("[bold magenta]💥 Top 5 Maiores Annoyances[/bold magenta]", style="magenta"))

    if not historico_annoyances:
        console.print("  [dim]Nenhum ganso soltou um grasnado alto o suficiente.[/dim]")
    else:
        historico_annoyances.sort(key=lambda x: x['pontos'], reverse=True)
        console.print(_construir_tabela_annoyances(historico_annoyances[:5]))

    # --- Seção 3: Hall da Fama ---
    console.print()
    goose_vencedor = (
        max(placar_gooses.items(), key=lambda x: x[1])[0]
        if placar_gooses else "Ninguém"
    )
    janitor_vencedor = (
        max(placar_janitors.items(), key=lambda x: x[1])[0]
        if placar_janitors else "Ninguém"
    )
    console.print(_construir_panel_hall_da_fama(goose_vencedor, janitor_vencedor))
    console.print()
