import pytest
from src.extensibility import (
    CodeSmellDetector,
    CostFunction,
    LinearCostFunction,
    ComplexityDetector,
    SizeDetector,
    get_default_detectors,
)


class CustomDetector(CodeSmellDetector):
    """Detector customizado para testes"""
    
    def calculate_delta(self, code_before: str, code_after: str):
        lines_before = len(code_before.split('\n'))
        lines_after = len(code_after.split('\n'))
        delta = lines_after - lines_before
        return (delta, f"{abs(delta)} lines")
    
    def get_weight(self):
        return 5
    
    def get_name(self):
        return "Custom Line Counter"


class TestCodeSmellDetector:
    """Testes para detectores de code smells"""
    
    def test_default_detectors_exist(self):
        """Deve retornar 5 detectores padrão"""
        detectors = get_default_detectors()
        assert len(detectors) == 5
    
    def test_complexity_detector(self):
        """Deve detectar mudanças de complexidade"""
        detector = ComplexityDetector()
        
        code_before = "def foo():\n    pass"
        code_after = "def foo():\n    if True:\n        pass"
        
        delta, desc = detector.calculate_delta(code_before, code_after)
        assert delta > 0
        assert "Complexity" in desc
    
    def test_custom_detector(self):
        """Deve permitir detector customizado"""
        detector = CustomDetector()
        
        code_before = "line1\nline2"
        code_after = "line1\nline2\nline3"
        
        delta, desc = detector.calculate_delta(code_before, code_after)
        assert delta == 1
        assert "1 lines" in desc


class TestCostFunction:
    """Testes para funções de custo"""
    
    def test_linear_cost_function(self):
        """Deve calcular custo linear"""
        cost_func = LinearCostFunction()
        deltas = [
            (5, 2, "Complexity"),
            (-3, 1, "LLOC"),
            (2, 3, "Nesting")
        ]
        
        chaos, cleanup, reasons = cost_func.calculate_cost(deltas)
        assert chaos == 16  # (5*2) + (2*3)
        assert cleanup == 3  # 3*1
        assert len(reasons) == 2