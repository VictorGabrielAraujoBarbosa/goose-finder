import pytest
from src.reporter import gerar_barra_heatmap


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
