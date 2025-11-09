import numpy as np

from .base import ModulacaoBase


class FSK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        super().__init__(bits_por_simbolo)

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação FSK (Frequency Shift Keying).
        A frequência da portadora pode variar entre a frequencia da portadora e 2 vezes essa frequência,
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as frequências correspondentes a cada símbolo.
        """
        parametros = []
        passo_de_frequencia = 1 / (2**self.bits_por_simbolo - 1)

        for simbolo in simbolos_decimais:
            frequencia = simbolo * passo_de_frequencia
            parametros.append(frequencia)

        return np.array(parametros)
