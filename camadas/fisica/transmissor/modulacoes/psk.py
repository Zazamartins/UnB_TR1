import numpy as np

from util.gray import Gray

from .base import ModulacaoBase


class PSK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        self.bits_por_simbolo = bits_por_simbolo
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação PSK (Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 graus a 360 graus
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as fases (em graus) correspondentes a cada símbolo.
        """
        gray = Gray(
            bits_por_simbolo=self.bits_por_simbolo, normalizado=True
        )  # Codigo Gray com valores de 0 a 1
        tabela_gray = gray.tabela_gray
        parametros = []
        num_fases = 2**self.bits_por_simbolo

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            indice = np.where(tabela_gray == simbolo)[0][0]
            fase = indice * (360 / num_fases)
            parametros.append(fase)

        return np.array(parametros)
