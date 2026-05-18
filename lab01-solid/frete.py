from abc import ABC, abstractmethod

class CalculadoraFrete(ABC):
    @abstractmethod
    def calcular(self) -> float: pass

class FreteNorte(CalculadoraFrete):
    def calcular(self) -> float: return 50.0

class FreteNordeste(CalculadoraFrete):
    def calcular(self) -> float: return 40.0

class FreteSul(CalculadoraFrete):
    def calcular(self) -> float: return 30.0

class FretePadrao(CalculadoraFrete):
    def calcular(self) -> float: return 20.0