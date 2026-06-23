"""
Sistema extensível para detectores de code smells e funções de custo.
Permite que usuários criem detectores personalizados e customizem o cálculo de caos.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from src.config import (
    PESO_COMPLEXIDADE,
    PESO_TAMANHO,
    PESO_MANUTENIBILIDADE,
    PESO_PARAMETROS,
    PESO_PROFUNDIDADE,
)
from src.metrics import (
    calculate_complexity,
    calculate_size,
    calculate_maintainability,
    count_excessive_parameters,
    calculate_max_depth,
)


# ==================== INTERFACES ABSTRATAS ====================

class CodeSmellDetector(ABC):
    """
    Interface abstrata para detectores de code smells.
    Usuários podem estender esta classe para criar detectores personalizados.
    """
    
    @abstractmethod
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        """
        Calcula a diferença (delta) de uma métrica entre duas versões de código.
        
        Args:
            code_before: Código antes da modificação
            code_after: Código depois da modificação
            
        Returns:
            Tuple[float, str]: (delta_value, description)
            - delta_value: Valor positivo = caos, negativo = limpeza
            - description: Descrição legível do que foi detectado
        """
        pass
    
    @abstractmethod
    def get_weight(self) -> int:
        """Retorna o peso desta métrica no cálculo de caos."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome legível desta métrica."""
        pass


class CostFunction(ABC):
    """
    Interface abstrata para funções de custo.
    Usuários podem criar suas próprias funções para calcular o "caos".
    """
    
    @abstractmethod
    def calculate_cost(self, deltas: List[Tuple[float, int, str]]) -> Tuple[float, float, List[str]]:
        """
        Calcula o custo total baseado nos deltas das métricas.
        
        Args:
            deltas: Lista de tuplas (delta_value, weight, description)
            
        Returns:
            Tuple[float, float, List[str]]: (chaos, cleanup, reasons)
        """
        pass


# ==================== DETECTORES PADRÃO ====================

class ComplexityDetector(CodeSmellDetector):
    """Detecta mudanças na complexidade ciclomática."""
    
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        before = calculate_complexity(code_before)
        after = calculate_complexity(code_after)
        delta = after - before
        
        if delta != 0:
            description = f"{abs(delta)} Complexity"
            return (delta, description)
        return (0.0, "")
    
    def get_weight(self) -> int:
        return PESO_COMPLEXIDADE
    
    def get_name(self) -> str:
        return "Cyclomatic Complexity"


class SizeDetector(CodeSmellDetector):
    """Detecta mudanças no tamanho (LLOC)."""
    
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        before = calculate_size(code_before)
        after = calculate_size(code_after)
        delta = after - before
        
        if delta != 0:
            description = f"{abs(delta)} LLOC"
            return (delta, description)
        return (0.0, "")
    
    def get_weight(self) -> int:
        return PESO_TAMANHO
    
    def get_name(self) -> str:
        return "Code Size (LLOC)"


class MaintainabilityDetector(CodeSmellDetector):
    """Detecta mudanças no índice de manutenibilidade."""
    
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        before = calculate_maintainability(code_before)
        after = calculate_maintainability(code_after)
        # MI menor = pior, então invertemos o sinal
        delta = -(after - before)
        
        if delta != 0:
            description = f"{abs(round(delta, 1))} Maintainability"
            return (delta, description)
        return (0.0, "")
    
    def get_weight(self) -> int:
        return PESO_MANUTENIBILIDADE
    
    def get_name(self) -> str:
        return "Maintainability Index"


class ParametersDetector(CodeSmellDetector):
    """Detecta mudanças em parâmetros excessivos."""
    
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        before = count_excessive_parameters(code_before)
        after = count_excessive_parameters(code_after)
        delta = after - before
        
        if delta != 0:
            description = f"{abs(delta)} Parameters"
            return (delta, description)
        return (0.0, "")
    
    def get_weight(self) -> int:
        return PESO_PARAMETROS
    
    def get_name(self) -> str:
        return "Excessive Parameters"


class DepthDetector(CodeSmellDetector):
    """Detecta mudanças na profundidade de aninhamento."""
    
    def calculate_delta(self, code_before: str, code_after: str) -> Tuple[float, str]:
        before = calculate_max_depth(code_before)
        after = calculate_max_depth(code_after)
        delta = after - before
        
        if delta != 0:
            description = f"{abs(delta)} Nesting"
            return (delta, description)
        return (0.0, "")
    
    def get_weight(self) -> int:
        return PESO_PROFUNDIDADE
    
    def get_name(self) -> str:
        return "Nesting Depth"


# ==================== FUNÇÃO DE CUSTO PADRÃO ====================

class LinearCostFunction(CostFunction):
    """Função de custo linear padrão: cost = sum(delta * weight)"""
    
    def calculate_cost(self, deltas: List[Tuple[float, int, str]]) -> Tuple[float, float, List[str]]:
        total_chaos = 0.0
        total_cleanup = 0.0
        chaos_reasons = []
        
        for delta, weight, description in deltas:
            if delta > 0:
                points = delta * weight
                total_chaos += points
                chaos_reasons.append(f"+{points} {description}")
            elif delta < 0:
                total_cleanup += abs(delta) * weight
        
        return (total_chaos, total_cleanup, chaos_reasons)


# ==================== FUNÇÕES AUXILIARES ====================

def get_default_detectors() -> List[CodeSmellDetector]:
    """Retorna a lista padrão de detectores de code smells."""
    return [
        ComplexityDetector(),
        SizeDetector(),
        MaintainabilityDetector(),
        ParametersDetector(),
        DepthDetector(),
    ]