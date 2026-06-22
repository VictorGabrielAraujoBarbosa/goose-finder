import pytest
from src.metrics import calculate_complexity


class TestCalculateComplexity:

    def test_CC01_simple_function_no_branches(self):
        """CC-01: Function with no branches should have CC == 1."""
        code = "def foo(): pass"
        assert calculate_complexity(code) == 1

    def test_CC02_function_with_one_if(self):
        """CC-02: Function with one `if` should have CC == 2."""
        code = "def foo(x):\n    if x:\n        return 1\n    return 0"
        assert calculate_complexity(code) == 2

    def test_CC03_multiple_functions_accumulate_cc(self):
        """CC-03: Multiple functions accumulate total CC."""
        code = (
            "def foo(x):\n    if x: return 1\n    return 0\n"
            "def bar(y):\n    if y: return 2\n    return 0\n"
        )
        # Each function with one `if` has CC=2; total = 4
        assert calculate_complexity(code) == 4

    def test_CC04_empty_string_returns_zero(self):
        """CC-04: Empty string should return 0."""
        assert calculate_complexity("") == 0

    def test_CC05_none_returns_zero(self):
        """CC-05: None should return 0 without raising an exception."""
        assert calculate_complexity(None) == 0

    def test_CC06_invalid_syntax_returns_zero(self):
        """CC-06: Code with syntax error should return 0."""
        assert calculate_complexity("def foo(:") == 0
