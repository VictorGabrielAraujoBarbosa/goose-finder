import pytest
from src.metrics import calcular_tamanho


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
