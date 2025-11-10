from abc import ABC, abstractmethod

import numpy as np


class ModulacaoBase(ABC):
    @abstractmethod
    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Retorna, para cada símbolo, o valor do parâmetro utilizado na modulação da portadora."""
        pass
