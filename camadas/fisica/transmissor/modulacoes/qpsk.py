import numpy as np

from camadas.fisica.transmissor.modulacoes.base import ModulacaoBase


class QPSK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        super().__init__(bits_por_simbolo)

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação QPSK (Quadrature Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 graus a 360 graus
        seguindo a codificação de Gray.
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        
        
        return fases
