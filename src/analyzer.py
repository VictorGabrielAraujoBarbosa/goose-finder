from pydriller import Repository

from src.config import (
    PESO_COMPLEXIDADE,
    PESO_TAMANHO,
    PESO_MANUTENIBILIDADE,
    PESO_PARAMETROS,
    PESO_PROFUNDIDADE,
)

from src.metrics import (
    calcular_complexidade,
    calcular_tamanho,
    calcular_manutenibilidade,
    contar_parametros_excessivos,
    calcular_profundidade_maxima,
    eh_arquivo_alvo,
)


def analisar_repositorio(repo_alvo: str) -> dict:
    """
    Percorre todos os commits do repositório e acumula os dados de análise.

    Retorna um dicionário com as seguintes chaves:
        - 'placar_gooses'       : { autor: pontos_totais }
        - 'placar_janitors'     : { autor: pontos_totais }
        - 'campos_de_batalha'   : { arquivo: {'caos_acumulado': int, 'tamanho_final': int} }
        - 'historico_annoyances': [ { hash, autor, arquivo, pontos, motivos, mensagem_commit } ]
    """
    placar_gooses = {}
    placar_janitors = {}
    campos_de_batalha = {}
    historico_annoyances = []

    for commit in Repository(repo_alvo).traverse_commits():
        for arquivo in commit.modified_files:

            if not eh_arquivo_alvo(arquivo):
                continue

            # --- Calcula deltas de cada métrica ---
            delta_cc = calcular_complexidade(arquivo.source_code) - calcular_complexidade(arquivo.source_code_before)

            tam_depois = calcular_tamanho(arquivo.source_code)
            delta_tam = tam_depois - calcular_tamanho(arquivo.source_code_before)

            delta_mi = (calcular_manutenibilidade(arquivo.source_code) -
                        calcular_manutenibilidade(arquivo.source_code_before))

            delta_param = (contar_parametros_excessivos(arquivo.source_code) -
                           contar_parametros_excessivos(arquivo.source_code_before))

            delta_prof = (calcular_profundidade_maxima(arquivo.source_code) -
                          calcular_profundidade_maxima(arquivo.source_code_before))

            mensagens_caos = []
            caos_neste_arquivo = 0
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

            # Análise de Manutenibilidade (MI menor = pior)
            if delta_mi < 0:
                pontos = round(abs(delta_mi) * PESO_MANUTENIBILIDADE, 1)
                caos_neste_arquivo += pontos
                mensagens_caos.append(f"+{pontos} Manutenibilidade")
            elif delta_mi > 0:
                limpeza_neste_arquivo += round(delta_mi * PESO_MANUTENIBILIDADE, 1)

            # Análise de Parâmetros
            if delta_param > 0:
                pontos = delta_param * PESO_PARAMETROS
                caos_neste_arquivo += pontos
                mensagens_caos.append(f"+{pontos} Parâmetros")
            elif delta_param < 0:
                limpeza_neste_arquivo += abs(delta_param) * PESO_PARAMETROS

            # Análise de Profundidade
            if delta_prof > 0:
                pontos = delta_prof * PESO_PROFUNDIDADE
                caos_neste_arquivo += pontos
                mensagens_caos.append(f"+{pontos} Aninhamento")
            elif delta_prof < 0:
                limpeza_neste_arquivo += abs(delta_prof) * PESO_PROFUNDIDADE

            autor = commit.author.name

            # Acumula dados de caos
            if caos_neste_arquivo > 0:
                placar_gooses[autor] = placar_gooses.get(autor, 0) + caos_neste_arquivo

                historico_annoyances.append({
                    'hash': commit.hash[:7],
                    'autor': autor,
                    'arquivo': arquivo.filename,
                    'pontos': caos_neste_arquivo,
                    'motivos': " e ".join(mensagens_caos),
                    'mensagem_commit': commit.msg.split('\n')[0],
                })

                if arquivo.filename not in campos_de_batalha:
                    campos_de_batalha[arquivo.filename] = {
                        'caos_acumulado': 0, 'tamanho_final': 0}
                campos_de_batalha[arquivo.filename]['caos_acumulado'] += caos_neste_arquivo

            # Acumula dados de limpeza
            if limpeza_neste_arquivo > 0:
                placar_janitors[autor] = placar_janitors.get(autor, 0) + limpeza_neste_arquivo

            # Atualiza o tamanho final do arquivo para o heatmap
            if arquivo.filename in campos_de_batalha:
                campos_de_batalha[arquivo.filename]['tamanho_final'] = tam_depois

    return {
        'placar_gooses': placar_gooses,
        'placar_janitors': placar_janitors,
        'campos_de_batalha': campos_de_batalha,
        'historico_annoyances': historico_annoyances,
    }
