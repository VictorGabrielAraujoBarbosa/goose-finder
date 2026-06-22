import pytest
from src.metrics import calculate_size


class TestCalculateSize:

    def test_TAM01_three_logical_statements(self):
        """TAM-01: Three assignments should result in LLOC == 3."""
        code = "x = 1\ny = 2\nz = x + y"
        assert calculate_size(code) == 3

    def test_TAM02_comments_and_blank_lines_ignored(self):
        """TAM-02: Comments and blank lines do not count as LLOC."""
        code = "# comment\n\nx = 1\n\n# another\ny = 2"
        result = calculate_size(code)
        assert result == 2

    def test_TAM03_empty_string_returns_zero(self):
        """TAM-03: Empty string should return 0."""
        assert calculate_size("") == 0

    def test_TAM04_only_comments_returns_zero(self):
        """TAM-04: Code with only comments should return 0."""
        code = "# line 1\n# line 2\n# line 3"
        assert calculate_size(code) == 0

    def test_TAM05_invalid_syntax_returns_zero(self):
        """TAM-05: Syntactically invalid code should return 0."""
        assert calculate_size("def foo(:") == 0
