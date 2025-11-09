import numpy as np

from .base import ModulacaoBase


class PSK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        super().__init__(bits_por_simbolo)

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação PSK (Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 graus a 180 graus
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        parametros = []
        passo_de_fase = 180 / (2**self.bits_por_simbolo - 1)

        for simbolo in simbolos_decimais:
            fase = simbolo * passo_de_fase
            parametros.append(fase)

        return np.array(parametros)
