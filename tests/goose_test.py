import os
import sys
import pytest
from unittest.mock import MagicMock

from src.goose import (
    calcular_complexidade,
    calcular_tamanho,
    calcular_manutenibilidade,
    contar_parametros_excessivos,
    calcular_profundidade_maxima,
    eh_arquivo_alvo,
    gerar_barra_heatmap,
)


def _arquivo_mock(filename="foo.py", source_code="x = 1", source_code_before="x = 0"):
    """Cria um mock de ModifiedFile do PyDriller."""
    arq = MagicMock()
    arq.filename = filename
    arq.source_code = source_code
    arq.source_code_before = source_code_before
    return arq


class TestCalcularComplexidade:

    def test_CC01_funcao_simples_sem_ramificacoes(self):
        """CC-01: Função sem ramificações deve ter CC == 1."""
        codigo = "def foo(): pass"
        assert calcular_complexidade(codigo) == 1

    def test_CC02_funcao_com_um_if(self):
        """CC-02: Função com um `if` deve ter CC == 2."""
        codigo = "def foo(x):\n    if x:\n        return 1\n    return 0"
        assert calcular_complexidade(codigo) == 2

    def test_CC03_multiplas_funcoes_acumulam_cc(self):
        """CC-03: Múltiplas funções acumulam a CC total."""
        codigo = (
            "def foo(x):\n    if x: return 1\n    return 0\n"
            "def bar(y):\n    if y: return 2\n    return 0\n"
        )
        # Cada função com um `if` tem CC=2; total = 4
        assert calcular_complexidade(codigo) == 4

    def test_CC04_string_vazia_retorna_zero(self):
        """CC-04: String vazia deve retornar 0."""
        assert calcular_complexidade("") == 0

    def test_CC05_none_retorna_zero(self):
        """CC-05: None deve retornar 0 sem levantar exceção."""
        assert calcular_complexidade(None) == 0

    def test_CC06_sintaxe_invalida_retorna_zero(self):
        """CC-06: Código com erro de sintaxe deve retornar 0."""
        assert calcular_complexidade("def foo(:") == 0


class TestCalcularTamanho:

    def test_TAM01_tres_instrucoes_logicas(self):
        """TAM-01: Três atribuições devem resultar em LLOC == 3."""
        codigo = "x = 1\ny = 2\nz = x + y"
        assert calcular_tamanho(codigo) == 3

    def test_TAM02_comentarios_e_linhas_em_branco_ignorados(self):
        """TAM-02: Comentários e linhas em branco não contam como LLOC."""
        codigo = "# comentário\n\nx = 1\n\n# outro\ny = 2"
        resultado = calcular_tamanho(codigo)
        assert resultado == 2

    def test_TAM03_string_vazia_retorna_zero(self):
        """TAM-03: String vazia deve retornar 0."""
        assert calcular_tamanho("") == 0

    def test_TAM04_apenas_comentarios_retorna_zero(self):
        """TAM-04: Código com só comentários deve retornar 0."""
        codigo = "# linha 1\n# linha 2\n# linha 3"
        assert calcular_tamanho(codigo) == 0

    def test_TAM05_sintaxe_invalida_retorna_zero(self):
        """TAM-05: Código sintaticamente inválido deve retornar 0."""
        assert calcular_tamanho("def foo(:") == 0


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
