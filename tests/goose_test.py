import os
import sys
import pytest
from unittest.mock import MagicMock

from src.metrics import (
    calcular_complexidade,
    calcular_tamanho,
    calcular_manutenibilidade,
    contar_parametros_excessivos,
    calcular_profundidade_maxima,
    eh_arquivo_alvo,
)
from src.reporter import gerar_barra_heatmap


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


class TestEhArquivoAlvo:

    def test_ALVO01_arquivo_py_valido(self):
        """ALVO-01: Arquivo .py com código antes e depois deve ser aceito."""
        arq = _arquivo_mock("foo.py", "x = 1", "x = 0")
        assert eh_arquivo_alvo(arq) is True

    def test_ALVO02_extensao_diferente_rejeitada(self):
        """ALVO-02: Arquivo .js com código presente deve ser rejeitado."""
        arq = _arquivo_mock("foo.js", "console.log(1)", "console.log(0)")
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO03_sem_codigo_atual_rejeitado(self):
        """ALVO-03: Arquivo deletado (source_code=None) deve ser rejeitado."""
        arq = _arquivo_mock("foo.py", source_code=None, source_code_before="x = 0")
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO04_sem_codigo_anterior_rejeitado(self):
        """ALVO-04: Arquivo novo (source_code_before=None) deve ser rejeitado."""
        arq = _arquivo_mock("foo.py", source_code="x = 1", source_code_before=None)
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO05_filename_none_rejeitado(self):
        """ALVO-05: filename=None deve ser rejeitado imediatamente."""
        arq = _arquivo_mock(filename=None)
        assert eh_arquivo_alvo(arq) is False

    def test_ALVO06_py_com_ambos_codes_nulos(self):
        """ALVO-06: Arquivo .py mas ambos os codes nulos deve ser rejeitado."""
        arq = _arquivo_mock("foo.py", source_code=None, source_code_before=None)
        assert eh_arquivo_alvo(arq) is False


class TestGerarBarraHeatmap:

    def _contar_blocos(self, barra: str) -> tuple[int, int]:
        """Conta blocos cheios (█) e vazios (░) na barra retornada."""
        cheios = barra.count('█')
        vazios = barra.count('░')
        return cheios, vazios

    def test_BARRA01_score_maximo_barra_cheia(self):
        """BARRA-01: score == max_score deve produzir 20 blocos cheios."""
        barra = gerar_barra_heatmap(100, 100)
        cheios, vazios = self._contar_blocos(barra)
        assert cheios == 20
        assert vazios == 0

    def test_BARRA02_score_zero_barra_vazia(self):
        """BARRA-02: score == 0 deve produzir 0 blocos cheios e 20 vazios."""
        barra = gerar_barra_heatmap(0, 100)
        cheios, vazios = self._contar_blocos(barra)
        assert cheios == 0
        assert vazios == 20

    def test_BARRA03_score_acima_70_cor_vermelha(self):
        """BARRA-03: Proporção > 70% deve usar cor vermelha (\\033[91m)."""
        barra = gerar_barra_heatmap(80, 100)
        assert "\033[91m" in barra

    def test_BARRA04_score_entre_30_e_70_cor_amarela(self):
        """BARRA-04: Proporção entre 30% e 70% deve usar cor amarela (\\033[93m)."""
        barra = gerar_barra_heatmap(50, 100)
        assert "\033[93m" in barra

    def test_BARRA05_score_abaixo_30_cor_cinza(self):
        """BARRA-05: Proporção < 30% deve usar cor cinza (\\033[90m)."""
        barra = gerar_barra_heatmap(20, 100)
        assert "\033[90m" in barra

    def test_BARRA06_max_score_zero_nao_levanta_excecao(self):
        """BARRA-06: max_score == 0 não deve levantar ZeroDivisionError."""
        barra = gerar_barra_heatmap(0, 0)
        assert isinstance(barra, str)
        assert '░' in barra

    def test_BARRA07_tamanho_customizado(self):
        """BARRA-07: tamanho_barra=10 deve resultar em exatamente 10 blocos."""
        barra = gerar_barra_heatmap(50, 100, tamanho_barra=10)
        cheios, vazios = self._contar_blocos(barra)
        assert cheios + vazios == 10
