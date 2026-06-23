from git.exc import InvalidGitRepositoryError
from pydriller import Repository
from src.config import load_exclusion_patterns, should_ignore

from src.config import (
    PESO_COMPLEXIDADE,
    PESO_TAMANHO,
    PESO_MANUTENIBILIDADE,
    PESO_PARAMETROS,
    PESO_PROFUNDIDADE,
)

from src.metrics import (
    calculate_complexity,
    calculate_size,
    calculate_maintainability,
    count_excessive_parameters,
    calculate_max_depth,
    is_target_file,
)


def analyse_repository(target_repo: str, progress=None, task_id=None) -> dict:
    """
    It iterates through all commits in the repository and accumulates the analysis data.

    It returns a dictionary with the following keys:
        - 'gooses_score' : { author: total_points }
        - 'janitors_score' : { author: total_points }
        - 'battlefields' : { file: {'accumulated_chaos': int, 'final_size': int} }
        - 'annoyances_history': [ { hash, author, file, points, reasons, commit_message } ]
    """
    gooses_score = {}
    janitors_score = {}
    battlefields = {}
    annoyances_history = []

    try:
        commits = list(Repository(target_repo).traverse_commits())
    except InvalidGitRepositoryError:
        raise ValueError(
            f"'{target_repo}' is not a valid Git repository. "
            "Make sure the path points to a directory that contains a '.git' folder."
        )

    for commit in commits:
        if progress is not None and task_id is not None:
            progress.advance(task_id)

        for file in commit.modified_files:

            if not is_target_file(file):
                continue

            # Calculates deltas for each metric
            delta_cc = calculate_complexity(file.source_code) - calculate_complexity(file.source_code_before)

            len_after = calculate_size(file.source_code)
            delta_len = len_after - calculate_size(file.source_code_before)

            delta_mi = (calculate_maintainability(file.source_code) -
                        calculate_maintainability(file.source_code_before))

            delta_param = (count_excessive_parameters(file.source_code) -
                           count_excessive_parameters(file.source_code_before))

            delta_prof = (calculate_max_depth(file.source_code) -
                          calculate_max_depth(file.source_code_before))

            chaos_messages = []
            chaos_on_this_file = 0
            cleanup_on_this_file = 0

            # Complexity Analysis
            if delta_cc > 0:
                points = delta_cc * PESO_COMPLEXIDADE
                chaos_on_this_file += points
                chaos_messages.append(f"+{points} Complexity")
            elif delta_cc < 0:
                cleanup_on_this_file += abs(delta_cc) * PESO_COMPLEXIDADE

            # Size Analysis
            if delta_len > 0:
                points = delta_len * PESO_TAMANHO
                chaos_on_this_file += points
                chaos_messages.append(f"+{points} LLOC")
            elif delta_len < 0:
                cleanup_on_this_file += abs(delta_len) * PESO_TAMANHO

            # Maintainability Analysis (lower MI = worse)
            if delta_mi < 0:
                points = round(abs(delta_mi) * PESO_MANUTENIBILIDADE, 1)
                chaos_on_this_file += points
                chaos_messages.append(f"+{points} Maintainability")
            elif delta_mi > 0:
                cleanup_on_this_file += round(delta_mi * PESO_MANUTENIBILIDADE, 1)

            # Parameter Analysis
            if delta_param > 0:
                points = delta_param * PESO_PARAMETROS
                chaos_on_this_file += points
                chaos_messages.append(f"+{points} Parameters")
            elif delta_param < 0:
                cleanup_on_this_file += abs(delta_param) * PESO_PARAMETROS

            # In-depth Analysis
            if delta_prof > 0:
                points = delta_prof * PESO_PROFUNDIDADE
                chaos_on_this_file += points
                chaos_messages.append(f"+{points} Nesting")
            elif delta_prof < 0:
                cleanup_on_this_file += abs(delta_prof) * PESO_PROFUNDIDADE

            author = commit.author.name

            # Accumulates data on chaos.
            if chaos_on_this_file > 0:
                gooses_score[author] = gooses_score.get(author, 0) + chaos_on_this_file

                annoyances_history.append({
                    'hash': commit.hash[:7],
                    'author': author,
                    'file': file.filename,
                    'points': chaos_on_this_file,
                    'reasons': ", ".join(chaos_messages),
                    'commit_message': commit.msg.split('\n')[0],
                })

                if file.filename not in battlefields:
                    battlefields[file.filename] = {
                        'accumulated_chaos': 0, 'final_size': 0}
                battlefields[file.filename]['accumulated_chaos'] += chaos_on_this_file

            # Acumula dados de limpeza
            if cleanup_on_this_file > 0:
                janitors_score[author] = janitors_score.get(author, 0) + cleanup_on_this_file

            # Atualiza o tamanho final do file para o heatmap
            if file.filename in battlefields:
                battlefields[file.filename]['final_size'] = len_after

    return {
        'gooses_score': gooses_score,
        'janitors_score': janitors_score,
        'battlefields': battlefields,
        'annoyances_history': annoyances_history,
    }



def analyze_files(file_paths: list, exclusion_patterns: list = None) -> list:
    """
    Filtra arquivos removendo aqueles que correspondem aos padrões de exclusão.
    
    Args:
        file_paths: Lista de caminhos de arquivo para analisar
        exclusion_patterns: Padrões de exclusão personalizados (opcional)
        
    Returns:
        Lista de arquivos que não devem ser ignorados
    """
    if exclusion_patterns is None:
        exclusion_patterns = load_exclusion_patterns()
    
    filtered_files = []
    for file_path in file_paths:
        if not should_ignore(file_path, exclusion_patterns):
            filtered_files.append(file_path)
    
    return filtered_files