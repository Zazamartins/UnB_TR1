from abc import ABC, abstractmethod

import numpy as np

class CodificacaoBase(ABC):
    @abstractmethod
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        """Retorna as palavras de bits codificadas."""
        pass
