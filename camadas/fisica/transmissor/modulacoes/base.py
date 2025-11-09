from abc import ABC, abstractmethod

import numpy as np


class ModulacaoBase(ABC):
    def __init__(self, bits_por_simbolo: int = 1):
        self.bits_por_simbolo = bits_por_simbolo

    @abstractmethod
    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Retorna, para cada símbolo, o valor do parâmetro utilizado na modulação da portadora."""
        pass
