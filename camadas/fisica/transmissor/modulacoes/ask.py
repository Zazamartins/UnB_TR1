import numpy as np

from .base import ModulacaoBase


class ASK(ModulacaoBase):
    def __init__(self):
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação ASK (Amplitude Shift Keying).
        A amplitude da portadora pode variar entre 0 e 1
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as amplitudes correspondentes a cada símbolo.
        """
        parametros = []

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            amplitude = simbolo
            parametros.append(amplitude)

        return np.array(parametros)
