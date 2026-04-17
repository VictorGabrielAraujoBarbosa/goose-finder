from pydriller import Repository
from radon.complexity import cc_visit
from radon.raw import analyze
import sys

# --- 1. DETECTORES DE ANNOYANCE E LIMPEZA (Métricas) ---

def calcular_complexidade(codigo: str) -> int:
    """Métrica 1: Complexidade Ciclomática (Ganso confuso)"""
    if not codigo: return 0
    try:
        return sum(b.complexity for b in cc_visit(codigo))
    except Exception:
        return 0

def calcular_tamanho(codigo: str) -> int:
    """Métrica 2: Linhas Lógicas de Código - LLOC (Ganso bloqueando o caminho)"""
    if not codigo: return 0
    try:
        return analyze(codigo).lloc
    except Exception:
        return 0

# --- 2. REGRAS DO JOGO ---

PESO_COMPLEXIDADE = 2 # Lógica confusa gera mais caos (ou mais pontos de limpeza se reduzida)
PESO_TAMANHO = 1      # Código longo gera caos normal

placar_gooses = {}
placar_janitors = {} # Novo placar para os heróis da limpeza!

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

# --- 4. MOTOR PRINCIPAL ---
if len(sys.argv) < 2:
    print("🦆 ERRO: Você esqueceu de me dizer onde soltar o ganso!")
    print("Uso: python goose.py <caminho_do_repositorio>")
    sys.exit(1)

repo_alvo = sys.argv[1]

print(f"🦆 Soltando os gansos e chamando os zeladores no repositório: {repo_alvo}...\n")

for commit in Repository(repo_alvo).traverse_commits():
    for arquivo in commit.modified_files:

        if eh_arquivo_alvo(arquivo):

            # Calcula deltas de Complexidade
            cc_antes = calcular_complexidade(arquivo.source_code_before)
            cc_depois = calcular_complexidade(arquivo.source_code)
            delta_cc = cc_depois - cc_antes

            # Calcula deltas de Tamanho (LLOC)
            tam_antes = calcular_tamanho(arquivo.source_code_before)
            tam_depois = calcular_tamanho(arquivo.source_code)
            delta_tam = tam_depois - tam_antes

            # Contadores do arquivo atual
            caos_neste_arquivo = 0
            mensagens_caos = []

            limpeza_neste_arquivo = 0
            mensagens_limpeza = []

            # --- Análise de Complexidade ---
            if delta_cc > 0:
                pontos = delta_cc * PESO_COMPLEXIDADE
                caos_neste_arquivo += pontos
                mensagens_caos.append(f"+{pontos} por Complexidade")
            elif delta_cc < 0:
                pontos = abs(delta_cc) * PESO_COMPLEXIDADE
                limpeza_neste_arquivo += pontos
                mensagens_limpeza.append(f"+{pontos} por Desatar Nós")

            # --- Análise de Tamanho ---
            if delta_tam > 0:
                pontos = delta_tam * PESO_TAMANHO
                caos_neste_arquivo += pontos
                mensagens_caos.append(f"+{pontos} por Código Longo")
            elif delta_tam < 0:
                pontos = abs(delta_tam) * PESO_TAMANHO
                limpeza_neste_arquivo += pontos
                mensagens_limpeza.append(f"+{pontos} por Limpar Linhas")

            autor = commit.author.name

            # Se o autor gerou caos, atualiza o placar dos Gansos!
            if caos_neste_arquivo > 0:
                placar_gooses[autor] = placar_gooses.get(autor, 0) + caos_neste_arquivo
                motivos = " e ".join(mensagens_caos)
                print(f"HONK! 🪿 {autor} causou caos em '{arquivo.filename}' ({motivos})")

            # Se o autor limpou o código, atualiza o placar dos Janitors!
            if limpeza_neste_arquivo > 0:
                placar_janitors[autor] = placar_janitors.get(autor, 0) + limpeza_neste_arquivo
                motivos = " e ".join(mensagens_limpeza)
                print(f"🧹 SPARKLE! {autor} limpou a sujeira em '{arquivo.filename}' ({motivos})")


# --- 5. TELAS FINAIS ---

print("\n" + "="*40)
print("🏆 RANKING DE CAOS (MASTER GOOSES) 🏆")
print("="*40)

if not placar_gooses:
    print("Nenhum caos detectado! Este repositório é muito pacífico.")
else:
    ranking_gooses = sorted(placar_gooses.items(), key=lambda x: x[1], reverse=True)
    for i, (autor, pontuacao) in enumerate(ranking_gooses, 1):
        icone = "👑" if i == 1 else "🪿"
        print(f"{i}º LUGAR {icone}: {autor.ljust(20)} | {pontuacao} pontos de Annoyance")

print("\n" + "="*40)
print("🧼 RANKING DE LIMPEZA (MASTER JANITORS) 🧼")
print("="*40)

if not placar_janitors:
    print("Nenhuma limpeza detectada! A cidade foi dominada pelos gansos.")
else:
    ranking_janitors = sorted(placar_janitors.items(), key=lambda x: x[1], reverse=True)
    for i, (autor, pontuacao) in enumerate(ranking_janitors, 1):
        icone = "🥇" if i == 1 else "🧹"
        print(f"{i}º LUGAR {icone}: {autor.ljust(20)} | {pontuacao} pontos de Limpeza")
