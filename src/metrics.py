import ast

from radon.complexity import cc_visit
from radon.raw import analyze
from radon.metrics import mi_visit

from src.config import LIMITE_PARAMETROS


def calcular_complexidade(codigo: str) -> int:
    """Complexidade Ciclomática (Ganso confuso)."""
    if not codigo:
        return 0
    try:
        return sum(b.complexity for b in cc_visit(codigo))
    except Exception:
        return 0


def calcular_tamanho(codigo: str) -> int:
    """Linhas Lógicas de Código — LLOC (Ganso bloqueando o caminho)."""
    if not codigo:
        return 0
    try:
        return analyze(codigo).lloc
    except Exception:
        return 0


def calcular_manutenibilidade(codigo: str) -> float:
    """Índice de Manutenibilidade — MI (Ganso confunde o mapa todo)."""
    if not codigo:
        return 100.0
    try:
        return mi_visit(codigo, True)
    except Exception:
        return 100.0


def contar_parametros_excessivos(codigo: str, limite: int = LIMITE_PARAMETROS) -> int:
    """Excesso de parâmetros em funções (Ganso espalhando parâmetros)."""
    if not codigo:
        return 0
    try:
        arvore = ast.parse(codigo)
    except SyntaxError:
        return 0

    excedentes = 0
    for node in ast.walk(arvore):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            total = len(node.args.args) + len(node.args.kwonlyargs)
            if node.args.vararg:
                total += 1
            if node.args.kwarg:
                total += 1
            if total > limite:
                excedentes += total - limite
    return excedentes


def calcular_profundidade_maxima(codigo: str) -> int:
    """Profundidade máxima de aninhamento."""
    if not codigo:
        return 0
    try:
        arvore = ast.parse(codigo)
    except SyntaxError:
        return 0

    blocos_aninhaveis = (
        ast.If, ast.For, ast.While, ast.Try, ast.With,
        ast.FunctionDef, ast.AsyncFunctionDef
    )

    def profundidade(node, atual=0):
        max_prof = atual
        for filho in ast.iter_child_nodes(node):
            prox = atual + 1 if isinstance(filho, blocos_aninhaveis) else atual
            max_prof = max(max_prof, profundidade(filho, prox))
        return max_prof

    return profundidade(arvore)


def eh_arquivo_alvo(arquivo) -> bool:
    """Garante que só vamos processar arquivos .py que foram MODIFICADOS."""
    if arquivo.filename is None:
        return False

    return (
        arquivo.filename.endswith('.py') and
        arquivo.source_code is not None and
        arquivo.source_code_before is not None
    )
