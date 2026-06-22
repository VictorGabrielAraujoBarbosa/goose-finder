import pytest
from src.metrics import calcular_manutenibilidade


class TestCalcularManutenibilidade:

    def test_MI01_funcao_simples_retorna_float(self):
        """MI-01: Função simples deve retornar float no intervalo [0, 100]."""
        resultado = calcular_manutenibilidade("def foo(): pass")
        assert isinstance(resultado, float)
        assert 0.0 <= resultado <= 100.0

    def test_MI02_codigo_complexo_tem_mi_menor(self):
        """MI-02: Código complexo deve ter MI menor que código simples."""
        simples = "def foo(): pass"
        complexo = (
            "def foo(a, b, c, d, e):\n"
            "    for i in range(100):\n"
            "        if i % 2 == 0:\n"
            "            for j in range(50):\n"
            "                if j > a:\n"
            "                    b = c + d * e\n"
            "    return b\n" * 5
        )
        assert calcular_manutenibilidade(complexo) < calcular_manutenibilidade(simples)

    def test_MI03_string_vazia_retorna_100(self):
        """MI-03: String vazia deve retornar 100.0 (valor padrão)."""
        assert calcular_manutenibilidade("") == 100.0

    def test_MI04_none_retorna_100(self):
        """MI-04: None deve retornar 100.0 sem levantar exceção."""
        assert calcular_manutenibilidade(None) == 100.0

    def test_MI05_sintaxe_invalida_retorna_100(self):
        """MI-05: Código com erro de sintaxe deve retornar 100.0."""
        assert calcular_manutenibilidade("def foo(:") == 100.0
