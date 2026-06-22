import pytest
from src.metrics import calcular_profundidade_maxima


class TestCalcularProfundidadeMaxima:

    def test_PROF01_sem_aninhamento(self):
        """PROF-01: Atribuição simples não tem blocos aninhados; deve retornar 0."""
        assert calcular_profundidade_maxima("x = 1") == 0

    def test_PROF02_um_if(self):
        """PROF-02: Um único `if` deve ter profundidade 1."""
        codigo = "if True:\n    pass"
        assert calcular_profundidade_maxima(codigo) == 1

    def test_PROF03_tres_niveis_de_aninhamento(self):
        """PROF-03: `if` dentro de `for` dentro de `def` deve retornar 3."""
        codigo = (
            "def foo():\n"
            "    for i in range(10):\n"
            "        if i > 0:\n"
            "            pass\n"
        )
        assert calcular_profundidade_maxima(codigo) == 3

    def test_PROF04_blocos_irmaos_retornam_maximo(self):
        """PROF-04: Dois `if` paralelos devem retornar 1, não 2."""
        codigo = "if True:\n    pass\nif False:\n    pass"
        assert calcular_profundidade_maxima(codigo) == 1

    def test_PROF05_try_conta_como_bloco(self):
        """PROF-05: `if` dentro de `try` deve retornar profundidade 2."""
        codigo = (
            "try:\n"
            "    if True:\n"
            "        pass\n"
            "except Exception:\n"
            "    pass\n"
        )
        assert calcular_profundidade_maxima(codigo) == 2

    def test_PROF06_string_vazia_retorna_zero(self):
        """PROF-06: String vazia deve retornar 0."""
        assert calcular_profundidade_maxima("") == 0

    def test_PROF07_none_retorna_zero(self):
        """PROF-07: None deve retornar 0 sem levantar exceção."""
        assert calcular_profundidade_maxima(None) == 0

    def test_PROF08_sintaxe_invalida_retorna_zero(self):
        """PROF-08: Código com erro de sintaxe deve retornar 0."""
        assert calcular_profundidade_maxima("def foo(:") == 0
