import fnmatch
from typing import List
VERSION = "1.0.0"

# Metric weights for chaos / cleanup calculation
PESO_TAMANHO = 1
PESO_PARAMETROS = 1
PESO_COMPLEXIDADE = 2
PESO_PROFUNDIDADE = 2
PESO_MANUTENIBILIDADE = 1

MAX_PARAMETERS = 4


def load_exclusion_patterns() -> List[str]:
    """
    Carrega os padrões de exclusão padrão.
    Pode ser estendido para ler de um arquivo .gitignore ou config.
    """
    return [
        "*.tmp",
        "*.log",
        "node_modules/",
        "__pycache__/",
        ".git/",
        "venv/",
        ".venv/",
        "*.pyc",
        ".pytest_cache/",
    ]


def should_ignore(file_path: str, exclusion_patterns: List[str]) -> bool:
    """
    Verifica se um caminho de arquivo deve ser ignorado baseado nos padrões.
    
    Args:
        file_path: Caminho do arquivo a verificar
        exclusion_patterns: Lista de padrões glob para exclusão
        
    Returns:
        True se o arquivo deve ser ignorado, False caso contrário
    """
    for pattern in exclusion_patterns:
        if fnmatch.fnmatch(file_path, pattern) or file_path.startswith(pattern):
            return True
    return False