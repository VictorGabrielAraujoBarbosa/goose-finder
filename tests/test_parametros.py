import pytest
from src.metrics import contar_parametros_excessivos


class TestContarParametrosExcessivos:

    def test_PARAM01_funcao_dentro_do_limite(self):
        """PARAM-01: Função com 3 parâmetros (limite=4) deve retornar 0."""
        codigo = "def foo(a, b, c): pass"
        assert contar_parametros_excessivos(codigo, limite=4) == 0

    def test_PARAM02_um_parametro_a_mais(self):
        """PARAM-02: Função com 5 parâmetros (limite=4) deve retornar 1."""
        codigo = "def foo(a, b, c, d, e): pass"
        assert contar_parametros_excessivos(codigo, limite=4) == 1

    def test_PARAM03_dois_parametros_a_mais(self):
        """PARAM-03: Função com 6 parâmetros (limite=4) deve retornar 2."""
        codigo = "def foo(a, b, c, d, e, f): pass"
        assert contar_parametros_excessivos(codigo, limite=4) == 2

    def test_PARAM04_args_e_kwargs_contam(self):
        """PARAM-04: *args e **kwargs devem contar como parâmetros extras."""
        # a, b, c, d = 4 (no limite); *args = +1; **kw = +1 → excedente = 2
        codigo = "def foo(a, b, c, d, *args, **kw): pass"
        assert contar_parametros_excessivos(codigo, limite=4) == 2

    def test_PARAM05_multiplas_funcoes_somam_excedentes(self):
        """PARAM-05: Excedentes de múltiplas funções devem ser somados."""
        codigo = (
            "def foo(a, b, c, d, e): pass\n"   # +1
            "def bar(x, y, z, w, v, u): pass\n"  # +2
        )
        assert contar_parametros_excessivos(codigo, limite=4) == 3

    def test_PARAM06_limite_customizado(self):
        """PARAM-06: Limite customizado deve ser respeitado."""
        codigo = "def foo(a, b): pass"
        assert contar_parametros_excessivos(codigo, limite=1) == 1

    def test_PARAM07_string_vazia_retorna_zero(self):
        """PARAM-07: String vazia deve retornar 0."""
        assert contar_parametros_excessivos("") == 0

    def test_PARAM08_none_retorna_zero(self):
        """PARAM-08: None deve retornar 0 sem levantar exceção."""
        assert contar_parametros_excessivos(None) == 0

    def test_PARAM09_sintaxe_invalida_retorna_zero(self):
        """PARAM-09: Código com erro de sintaxe deve retornar 0."""
        assert contar_parametros_excessivos("def foo(:") == 0
