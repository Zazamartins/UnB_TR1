import numpy as np

from .base import ModulacaoBase


class ASK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        super().__init__(bits_por_simbolo)

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação ASK (Amplitude Shift Keying).
        A amplitude da portadora pode variar entre 0 e 1
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as amplitudes correspondentes a cada símbolo.
        """
        parametros = []
        passo_de_amplitude = 1 / (2**self.bits_por_simbolo - 1)

        for simbolo in simbolos_decimais:
            amplitude = simbolo * passo_de_amplitude
            parametros.append(amplitude)

        return np.array(parametros)
