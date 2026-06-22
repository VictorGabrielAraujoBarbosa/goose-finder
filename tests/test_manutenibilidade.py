import pytest
from src.metrics import calculate_maintainability


class TestCalculateMaintainability:

    def test_MI01_simple_function_returns_float(self):
        """MI-01: Simple function should return a float in [0, 100]."""
        result = calculate_maintainability("def foo(): pass")
        assert isinstance(result, float)
        assert 0.0 <= result <= 100.0

    def test_MI02_complex_code_has_lower_mi(self):
        """MI-02: Complex code should have a lower MI than simple code."""
        simple = "def foo(): pass"
        complex_code = (
            "def foo(a, b, c, d, e):\n"
            "    for i in range(100):\n"
            "        if i % 2 == 0:\n"
            "            for j in range(50):\n"
            "                if j > a:\n"
            "                    b = c + d * e\n"
            "    return b\n" * 5
        )
        assert calculate_maintainability(complex_code) < calculate_maintainability(simple)

    def test_MI03_empty_string_returns_100(self):
        """MI-03: Empty string should return 100.0 (default value)."""
        assert calculate_maintainability("") == 100.0

    def test_MI04_none_returns_100(self):
        """MI-04: None should return 100.0 without raising an exception."""
        assert calculate_maintainability(None) == 100.0

    def test_MI05_invalid_syntax_returns_100(self):
        """MI-05: Code with syntax error should return 100.0."""
        assert calculate_maintainability("def foo(:") == 100.0
