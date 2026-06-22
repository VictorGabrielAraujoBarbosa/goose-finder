import pytest
from src.metrics import is_target_file
from tests.helpers import arquivo_mock


class TestIsTargetFile:

    def test_ALVO01_valid_py_file(self):
        """ALVO-01: .py file with code before and after should be accepted."""
        file = arquivo_mock("foo.py", "x = 1", "x = 0")
        assert is_target_file(file) is True

    def test_ALVO02_different_extension_rejected(self):
        """ALVO-02: .js file with code present should be rejected."""
        file = arquivo_mock("foo.js", "console.log(1)", "console.log(0)")
        assert is_target_file(file) is False

    def test_ALVO03_no_current_code_rejected(self):
        """ALVO-03: Deleted file (source_code=None) should be rejected."""
        file = arquivo_mock("foo.py", source_code=None, source_code_before="x = 0")
        assert is_target_file(file) is False

    def test_ALVO04_no_previous_code_rejected(self):
        """ALVO-04: New file (source_code_before=None) should be rejected."""
        file = arquivo_mock("foo.py", source_code="x = 1", source_code_before=None)
        assert is_target_file(file) is False

    def test_ALVO05_filename_none_rejected(self):
        """ALVO-05: filename=None should be rejected immediately."""
        file = arquivo_mock(filename=None)
        assert is_target_file(file) is False

    def test_ALVO06_py_with_both_codes_null(self):
        """ALVO-06: .py file but both codes null should be rejected."""
        file = arquivo_mock("foo.py", source_code=None, source_code_before=None)
        assert is_target_file(file) is False
