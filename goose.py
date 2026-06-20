from pydriller import Repository
from radon.complexity import cc_visit
from radon.raw import analyze
from radon.metrics import mi_visit
import argparse
import sys
import io

# Garante que o stdout usa UTF-8 em qualquer sistema operacional
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace")

# --- 1. DETECTORES DE ANNOYANCE E LIMPEZA (Métricas) ---


def calcular_complexidade(codigo: str) -> int:
    """Métrica 1: Complexidade Ciclomática (Ganso confuso)"""
    if not codigo:
        return 0
    try:
        return sum(b.complexity for b in cc_visit(codigo))
    except Exception:
        return 0


def calcular_tamanho(codigo: str) -> int:
    """Métrica 2: Linhas Lógicas de Código - LLOC (Ganso bloqueando o caminho)"""
    if not codigo:
        return 0
    try:
        return analyze(codigo).lloc
    except Exception:
        return 0


def calcular_manutenibilidade(codigo: str) -> float:
    """Métrica 3: Índice de Manutenibilidade - MI (Ganso confunde o mapa todo)"""
    if not codigo:
        return 100.0
    try:
        return mi_visit(codigo, True)
    except Exception:
        return 100.0

# --- 2. REGRAS DO JOGO ---


# Lógica confusa gera mais caos (ou mais pontos de limpeza se reduzida)
PESO_COMPLEXIDADE = 2
PESO_TAMANHO = 1      # Código longo gera caos normal
PESO_MANUTENIBILIDADE = 1  # Queda no MI = ganso espalhou confusão pelo arquivo todo

# --- 3. FILTRO ESTRITO DE ARQUIVOS ---


def eh_arquivo_alvo(arquivo) -> bool:
    """Garante que só vamos processar arquivos .py que foram MODIFICADOS"""
    if arquivo.filename is None:
        return False

    return (
        arquivo.filename.endswith('.py') and
        arquivo.source_code is not None and
        arquivo.source_code_before is not None
    )

# --- 4. CLI E CHARME (INTERFACE DO USUÁRIO) ---


def mostrar_charme_e_parsear_argumentos():
    """Gerencia os menus de Help, Info e os argumentos passados no terminal."""
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("repo_alvo", nargs="?",
                        help="Caminho do repositório (local ou URL)")
    parser.add_argument("-h", "--help", action="store_true",
                        help="Mostra a ajuda")
    parser.add_argument("-v", "--version",
                        action="store_true", help="Mostra a versão")

    args = parser.parse_args()

    if args.version:
        print("\U0001fabf  Goose Finder v1.0.0 - 'Honk Edition'")
        print("Desenvolvido para provar que a paz nunca foi uma opcao no code review.")
        sys.exit(0)

    if args.help or not args.repo_alvo:
        print(r"""
     __
   >(' )    HONK! Bem-vindo ao GOOSE FINDER!
     )/
    /(      "Peace was never an option."
   /  `----/
   \  ~=- /
 ~^~^~^~^~^~^~
""")
        print("""
 USO:
   python goose_finder.py <caminho_do_repositorio> [opções]

 ARGUMENTOS:
   <caminho_do_repositorio>   Onde soltar o ganso (caminho local ou URL do git)

 OPÇÕES:
   -h, --help                 Mostra essa mensagem e grasna para você.
   -v, --version              Mostra a versão atual da ferramenta.

 COMO FUNCIONA:
   O ganso vasculha o historico do git em busca de 'Annoyances' (code smells).
   \U0001fabf Gansos (Gooses): Devs que aumentam a complexidade ou tamanho do codigo.
   \U0001f9f9 Zeladores (Janitors): Devs que desatam os nos e limpam a baguna.
        """)
        sys.exit(0 if args.help else 1)

    return args.repo_alvo

# --- 5. MOTOR PRINCIPAL ---


if __name__ == "__main__":
    repo_alvo = mostrar_charme_e_parsear_argumentos()

    # Estruturas de dados para o relatório
    placar_gooses = {}
    placar_janitors = {}
    campos_de_batalha = {}  # { 'arquivo.py': {'caos_acumulado': 0, 'tamanho_final': 0} }
    historico_annoyances = []  # Lista de piores commits

    print(
        f"🦆 O ganso está investigando furtivamente o repositório: {repo_alvo}...")
    print("⏳ Isso pode levar um tempo dependendo do tamanho da bagunça...\n")

    for commit in Repository(repo_alvo).traverse_commits():
        for arquivo in commit.modified_files:

            if eh_arquivo_alvo(arquivo):
                # Calcula deltas
                cc_antes = calcular_complexidade(arquivo.source_code_before)
                cc_depois = calcular_complexidade(arquivo.source_code)
                delta_cc = cc_depois - cc_antes

                tam_antes = calcular_tamanho(arquivo.source_code_before)
                tam_depois = calcular_tamanho(arquivo.source_code)
                delta_tam = tam_depois - tam_antes

                mi_antes = calcular_manutenibilidade(
                    arquivo.source_code_before)
                mi_depois = calcular_manutenibilidade(arquivo.source_code)
                delta_mi = mi_depois - mi_antes  # MI menor = pior

                caos_neste_arquivo = 0
                mensagens_caos = []
                limpeza_neste_arquivo = 0

                # Análise de Complexidade
                if delta_cc > 0:
                    pontos = delta_cc * PESO_COMPLEXIDADE
                    caos_neste_arquivo += pontos
                    mensagens_caos.append(f"+{pontos} Complexidade")
                elif delta_cc < 0:
                    limpeza_neste_arquivo += abs(delta_cc) * PESO_COMPLEXIDADE

                # Análise de Tamanho
                if delta_tam > 0:
                    pontos = delta_tam * PESO_TAMANHO
                    caos_neste_arquivo += pontos
                    mensagens_caos.append(f"+{pontos} LLOC")
                elif delta_tam < 0:
                    limpeza_neste_arquivo += abs(delta_tam) * PESO_TAMANHO

                # Análise de Manutenibilidade
                if delta_mi < 0:
                    pontos = round(abs(delta_mi) * PESO_MANUTENIBILIDADE, 1)
                    caos_neste_arquivo += pontos
                    mensagens_caos.append(f"+{pontos} Manutenibilidade")
                elif delta_mi > 0:
                    limpeza_neste_arquivo += round(delta_mi *
                                                   PESO_MANUTENIBILIDADE, 1)

                autor = commit.author.name

                # --- COLETANDO DADOS DE CAOS ---
                if caos_neste_arquivo > 0:
                    placar_gooses[autor] = placar_gooses.get(
                        autor, 0) + caos_neste_arquivo

                    historico_annoyances.append({
                        'hash': commit.hash[:7],
                        'autor': autor,
                        'arquivo': arquivo.filename,
                        'pontos': caos_neste_arquivo,
                        'motivos': " e ".join(mensagens_caos),
                        'mensagem_commit': commit.msg.split('\n')[0]
                    })

                    if arquivo.filename not in campos_de_batalha:
                        campos_de_batalha[arquivo.filename] = {
                            'caos_acumulado': 0, 'tamanho_final': 0}
                    campos_de_batalha[arquivo.filename]['caos_acumulado'] += caos_neste_arquivo

                # --- COLETANDO DADOS DE LIMPEZA ---
                if limpeza_neste_arquivo > 0:
                    placar_janitors[autor] = placar_janitors.get(
                        autor, 0) + limpeza_neste_arquivo

                # Atualiza o tamanho final do arquivo para o heatmap
                if arquivo.filename in campos_de_batalha:
                    campos_de_batalha[arquivo.filename]['tamanho_final'] = tam_depois

    # --- 6. GERAÇÃO DO RELATÓRIO (Telas Finais) ---

    def gerar_barra_heatmap(score: float, max_score: float, tamanho_barra: int = 20) -> str:
        """Gera uma barra visual ASCII para representar o quão crítico é o arquivo."""
        if max_score == 0:
            return "[░"*tamanho_barra + "]"

        proporcao = score / max_score
        blocos_cheios = int(proporcao * tamanho_barra)
        blocos_vazios = tamanho_barra - blocos_cheios

        if proporcao > 0.7:
            cor = "\033[91m"  # Vermelho
        elif proporcao > 0.3:
            cor = "\033[93m"  # Amarelo
        else:
            cor = "\033[90m"  # Cinza

        reset = "\033[0m"
        barra = f"{cor}{'█'*blocos_cheios}{'░'*blocos_vazios}{reset}"
        return f"[{barra}]"

    print("\n" + "="*60)
    print("📊 RELATÓRIO OFICIAL DO GANSO (GOOSE REPORT)")
    print("="*60)

    # SECÃO 1: CAMPOS DE BATALHA
    print("\n🔥 TOP 5 CAMPOS DE BATALHA (Arquivos mais problemáticos por tamanho)")

    batalhas_ativas = []
    for arq, stats in campos_de_batalha.items():
        if stats['tamanho_final'] > 0:
            densidade = stats['caos_acumulado'] / stats['tamanho_final']
            batalhas_ativas.append({
                'arquivo': arq,
                'densidade': densidade,
                'caos': stats['caos_acumulado'],
                'tamanho': stats['tamanho_final']
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
                f"    └─ Caos Histórico: {b['caos']} pts | LLOC Atual: {b['tamanho']} | Densidade: {b['densidade']:.2f} pts/linha\n")

    # SEÇÃO 2: MAIORES ANNOYANCES
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

    # SEÇÃO 3: PLACARES
    print("🏆 HALL DA FAMA (E DA INFÂMIA)")

    goose_vencedor = max(placar_gooses.items(), key=lambda x: x[1])[
        0] if placar_gooses else "Ninguém"
    janitor_vencedor = max(placar_janitors.items(), key=lambda x: x[1])[
        0] if placar_janitors else "Ninguém"

    print(f"👑 MASTER GOOSE (Maior causador de caos) : {goose_vencedor}")
    print(f"🥇 MASTER JANITOR (Maior limpador)       : {janitor_vencedor}")
    print("="*60 + "\n")
