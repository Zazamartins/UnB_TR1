import numpy as np

from camadas.fisica.transmissor.modulacoes.base import ModulacaoBase
from camadas.fisica.transmissor.modulacoes.psk import PSK

class QPSK(ModulacaoBase):
    def __init__(self):
        super().__init__()
        self.psk = PSK(bits_por_simbolo=2)  # QPSK usa 2 bits por símbolo

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação QPSK (Quadrature Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 a 360 graus
        em intervalos atrelados ao número de bits por símbolo (2 bits por símbolo para QPSK).
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        return self.psk.gerar_parametros(simbolos_decimais)
