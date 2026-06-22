import pytest
from src.metrics import count_excessive_parameters


class TestCountExcessiveParameters:

    def test_PARAM01_function_within_limit(self):
        """PARAM-01: Function with 3 parameters (limit=4) should return 0."""
        code = "def foo(a, b, c): pass"
        assert count_excessive_parameters(code, limit=4) == 0

    def test_PARAM02_one_parameter_over_limit(self):
        """PARAM-02: Function with 5 parameters (limit=4) should return 1."""
        code = "def foo(a, b, c, d, e): pass"
        assert count_excessive_parameters(code, limit=4) == 1

    def test_PARAM03_two_parameters_over_limit(self):
        """PARAM-03: Function with 6 parameters (limit=4) should return 2."""
        code = "def foo(a, b, c, d, e, f): pass"
        assert count_excessive_parameters(code, limit=4) == 2

    def test_PARAM04_args_and_kwargs_count(self):
        """PARAM-04: *args and **kwargs should count as extra parameters."""
        # a, b, c, d = 4 (at limit); *args = +1; **kw = +1 → excess = 2
        code = "def foo(a, b, c, d, *args, **kw): pass"
        assert count_excessive_parameters(code, limit=4) == 2

    def test_PARAM05_multiple_functions_sum_excess(self):
        """PARAM-05: Excess parameters from multiple functions should be summed."""
        code = (
            "def foo(a, b, c, d, e): pass\n"   # +1
            "def bar(x, y, z, w, v, u): pass\n"  # +2
        )
        assert count_excessive_parameters(code, limit=4) == 3

    def test_PARAM06_custom_limit(self):
        """PARAM-06: Custom limit should be respected."""
        code = "def foo(a, b): pass"
        assert count_excessive_parameters(code, limit=1) == 1

    def test_PARAM07_empty_string_returns_zero(self):
        """PARAM-07: Empty string should return 0."""
        assert count_excessive_parameters("") == 0

    def test_PARAM08_none_returns_zero(self):
        """PARAM-08: None should return 0 without raising an exception."""
        assert count_excessive_parameters(None) == 0

    def test_PARAM09_invalid_syntax_returns_zero(self):
        """PARAM-09: Code with syntax error should return 0."""
        assert count_excessive_parameters("def foo(:") == 0
