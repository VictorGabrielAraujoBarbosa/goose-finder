import pytest
from src.metrics import calculate_max_depth


class TestCalculateMaxDepth:

    def test_PROF01_no_nesting(self):
        """PROF-01: Simple assignment has no nested blocks; should return 0."""
        assert calculate_max_depth("x = 1") == 0

    def test_PROF02_one_if(self):
        """PROF-02: A single `if` should have depth 1."""
        code = "if True:\n    pass"
        assert calculate_max_depth(code) == 1

    def test_PROF03_three_nesting_levels(self):
        """PROF-03: `if` inside `for` inside `def` should return 3."""
        code = (
            "def foo():\n"
            "    for i in range(10):\n"
            "        if i > 0:\n"
            "            pass\n"
        )
        assert calculate_max_depth(code) == 3

    def test_PROF04_sibling_blocks_return_maximum(self):
        """PROF-04: Two parallel `if` blocks should return 1, not 2."""
        code = "if True:\n    pass\nif False:\n    pass"
        assert calculate_max_depth(code) == 1

    def test_PROF05_try_counts_as_block(self):
        """PROF-05: `if` inside `try` should return depth 2."""
        code = (
            "try:\n"
            "    if True:\n"
            "        pass\n"
            "except Exception:\n"
            "    pass\n"
        )
        assert calculate_max_depth(code) == 2

    def test_PROF06_empty_string_returns_zero(self):
        """PROF-06: Empty string should return 0."""
        assert calculate_max_depth("") == 0

    def test_PROF07_none_returns_zero(self):
        """PROF-07: None should return 0 without raising an exception."""
        assert calculate_max_depth(None) == 0

    def test_PROF08_invalid_syntax_returns_zero(self):
        """PROF-08: Code with syntax error should return 0."""
        assert calculate_max_depth("def foo(:") == 0
