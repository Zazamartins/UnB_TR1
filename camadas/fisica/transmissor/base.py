from abc import ABC, abstractmethod

import numpy as np


class TransmissorBase(ABC):
    @abstractmethod
    def processar_sinal(self, mensagem: str) -> np.ndarray:
        """Processa a mensagem de entrada e retorna o sinal modulado"""
        pass