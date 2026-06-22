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
