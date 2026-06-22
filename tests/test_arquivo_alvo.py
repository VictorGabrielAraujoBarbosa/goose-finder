import pytest
from src.metrics import eh_arquivo_alvo
from tests.helpers import arquivo_mock


class TestEhArquivoAlvo:

    def test_ALVO01_arquivo_py_valido(self):
        """ALVO-01: Arquivo .py com código antes e depois deve ser aceito."""
        arq = arquivo_mock("foo.py", "x = 1", "x = 0")
        assert eh_arquivo_alvo(arq) is True

    def test_ALVO02_extensao_diferente_rejeitada(self):
        """ALVO-02: Arquivo .js com código presente deve ser rejeitado."""
        arq = arquivo_mock("foo.js", "console.log(1)", "console.log(0)")
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO03_sem_codigo_atual_rejeitado(self):
        """ALVO-03: Arquivo deletado (source_code=None) deve ser rejeitado."""
        arq = arquivo_mock("foo.py", source_code=None, source_code_before="x = 0")
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO04_sem_codigo_anterior_rejeitado(self):
        """ALVO-04: Arquivo novo (source_code_before=None) deve ser rejeitado."""
        arq = arquivo_mock("foo.py", source_code="x = 1", source_code_before=None)
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO05_filename_none_rejeitado(self):
        """ALVO-05: filename=None deve ser rejeitado imediatamente."""
        arq = arquivo_mock(filename=None)
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO06_py_com_ambos_codes_nulos(self):
        """ALVO-06: Arquivo .py mas ambos os codes nulos deve ser rejeitado."""
        arq = arquivo_mock("foo.py", source_code=None, source_code_before=None)
        assert eh_arquivo_alvo(arq) is False
