from abc import ABC, abstractmethod

class CalculadoraDesconto(ABC):
    @abstractmethod
    def calcular(self, valor: float) -> float: pass

class DescontoVIP(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.85

class DescontoPremium(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.90

class DescontoComum(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.95