def gerar_barra_heatmap(score: float, max_score: float, tamanho_barra: int = 20) -> str:
    """Gera uma barra visual ASCII para representar o quão crítico é o arquivo."""
    if max_score == 0:
        return "[" + "░" * tamanho_barra + "]"

    proporcao = score / max_score
    blocos_cheios = int(proporcao * tamanho_barra)
    blocos_vazios = tamanho_barra - blocos_cheios

    if proporcao > 0.7:
        cor = "\033[91m"   # Vermelho
    elif proporcao > 0.3:
        cor = "\033[93m"   # Amarelo
    else:
        cor = "\033[90m"   # Cinza

    reset = "\033[0m"
    barra = f"{cor}{'█' * blocos_cheios}{'░' * blocos_vazios}{reset}"
    return f"[{barra}]"


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

    print("\n" + "=" * 60)
    print("📊 RELATÓRIO OFICIAL DO GANSO (GOOSE REPORT)")
    print("=" * 60)

    # --- Seção 1: Campos de Batalha ---
    print("\n🔥 TOP 5 CAMPOS DE BATALHA (Arquivos mais problemáticos por tamanho)")

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
        print("Nenhum arquivo problemático encontrado. Paz reina.")
    else:
        batalhas_ativas.sort(key=lambda x: x['densidade'], reverse=True)
        top_batalhas = batalhas_ativas[:5]
        max_densidade = top_batalhas[0]['densidade']

        for b in top_batalhas:
            barra = gerar_barra_heatmap(b['densidade'], max_densidade)
            print(f"{barra} {b['arquivo']}")
            print(
                f"    └─ Caos Histórico: {b['caos']} pts | "
                f"LLOC Atual: {b['tamanho']} | "
                f"Densidade: {b['densidade']:.2f} pts/linha\n"
            )

    # --- Seção 2: Maiores Annoyances ---
    print("\n💥 TOP 5 MAIORES ANNOYANCES (Os piores commits)")

    if not historico_annoyances:
        print("Nenhum ganso soltou um grasnado alto o suficiente.")
    else:
        historico_annoyances.sort(key=lambda x: x['pontos'], reverse=True)

        for i, ann in enumerate(historico_annoyances[:5], 1):
            print(f"{i}. 🪿 [+{ann['pontos']} pts] {ann['arquivo']}")
            print(f"   Autor: {ann['autor']} | Commit: {ann['hash']}")
            print(f"   Motivos: {ann['motivos']}")
            print(f"   Mensagem: \"{ann['mensagem_commit']}\"\n")

    # --- Seção 3: Hall da Fama ---
    print("🏆 HALL DA FAMA (E DA INFÂMIA)")

    goose_vencedor = (
        max(placar_gooses.items(), key=lambda x: x[1])[0]
        if placar_gooses else "Ninguém"
    )
    janitor_vencedor = (
        max(placar_janitors.items(), key=lambda x: x[1])[0]
        if placar_janitors else "Ninguém"
    )

    print(f"👑 MASTER GOOSE (Maior causador de caos) : {goose_vencedor}")
    print(f"🥇 MASTER JANITOR (Maior limpador)       : {janitor_vencedor}")
    print("=" * 60 + "\n")
