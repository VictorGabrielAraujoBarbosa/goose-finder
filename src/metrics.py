import ast

from radon.complexity import cc_visit
from radon.raw import analyze
from radon.metrics import mi_visit

from src.config import MAX_PARAMETERS


def calculate_complexity(code: str) -> int:
    """Cyclomatic Complexity (confused goose)."""
    if not code:
        return 0
    try:
        return sum(b.complexity for b in cc_visit(code))
    except Exception:
        return 0


def calculate_size(code: str) -> int:
    """Logical Lines of Code — LLOC (goose blocking the path)."""
    if not code:
        return 0
    try:
        return analyze(code).lloc
    except Exception:
        return 0


def calculate_maintainability(code: str) -> float:
    """Maintainability Index — MI (goose scrambling the whole map)."""
    if not code:
        return 100.0
    try:
        return mi_visit(code, True)
    except Exception:
        return 100.0


def count_excessive_parameters(code: str, limit: int = MAX_PARAMETERS) -> int:
    """Excess parameters in functions (goose spreading parameters everywhere)."""
    if not code:
        return 0
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0

    excess = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            total = len(node.args.args) + len(node.args.kwonlyargs)
            if node.args.vararg:
                total += 1
            if node.args.kwarg:
                total += 1
            if total > limit:
                excess += total - limit
    return excess


def calculate_max_depth(code: str) -> int:
    """Maximum nesting depth."""
    if not code:
        return 0
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0

    nestable_blocks = (
        ast.If, ast.For, ast.While, ast.Try, ast.With,
        ast.FunctionDef, ast.AsyncFunctionDef
    )

    def depth(node, current=0):
        max_depth = current
        for child in ast.iter_child_nodes(node):
            next_level = current + 1 if isinstance(child, nestable_blocks) else current
            max_depth = max(max_depth, depth(child, next_level))
        return max_depth

    return depth(tree)


def is_target_file(file) -> bool:
    """Ensures we only process .py files that were MODIFIED."""
    if file.filename is None:
        return False

    return (
        file.filename.endswith('.py') and
        file.source_code is not None and
        file.source_code_before is not None
    )
