import numpy as np

from .base import ModulacaoBase


class FSK(ModulacaoBase):
    def __init__(self):
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação FSK (Frequency Shift Keying).
        A frequência da portadora pode variar entre a frequencia da portadora e 2 vezes essa frequência,
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com o multiplicador de frequência correspondentes a cada símbolo.
        """
        parametros = []

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            parametros.append(1 + simbolo)

        return np.array(parametros)
