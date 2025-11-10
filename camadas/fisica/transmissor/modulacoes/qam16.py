import numpy as np

from camadas.fisica.transmissor.modulacoes.base import ModulacaoBase


class QAM16(ModulacaoBase):
    def __init__(self):
        super().__init__()

        self._gray_16qam_decimal = np.array(
            [
                [7, 5, 13, 15],  # [[0, 1, 1, 1], [0, 1, 0, 1], [1,1,0,1], [1,1,1,1]],
                [6, 4, 12, 14],  # [[0, 1, 1, 0], [0, 1, 0, 0], [1,1,0,0], [1,1,1,0]],
                [2, 0, 8, 10],  # [[0, 0, 1, 0], [0, 0, 0, 0], [1,0,0,0], [1,0,1,0]],
                [3, 1, 9, 11],  # [[0, 0, 1, 1], [0, 0, 0, 1], [1,0,0,1], [1,0,1,1]]
            ]
        )

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação 16QAM (Quadrature Amplitude Modulation).
        A fase da portadora pode ser defasada de 0 a 360 graus
        em intervalos atrelados ao número de bits por símbolo (2 bits por símbolo para QPSK).
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        amplitudes = np.zeros_like(simbolos_decimais, dtype=float)
        fases = np.zeros_like(simbolos_decimais, dtype=float)

        if np.any(simbolos_decimais < 0) or np.any(simbolos_decimais > 15):
            raise ValueError("Símbolos decimais devem estar entre 0 e 15 para 16-QAM.")

        # Q > 0 === X1XX
        # Q < 0 === X0XX
        # I > 0 === 1XXX
        # I < 0 === 0XXX
        # I = 1/3sqrt(2) === XX0X
        # I = 1/sqrt(2) === XX1X
        # Q = 1/3sqrt(2) === XXX0
        # Q = 1/sqrt(2) === XXX1
        # 45deg === XX00 e XX11
        # 75deg === XX01
        # 15deg === XX10
        for i, simbolo in enumerate(simbolos_decimais):
            indices = np.argwhere(self._gray_16qam_decimal == simbolo)

            linha, coluna = indices[0]

            # Determina componente I
            if coluna in [0, 1]:  # I < 0
                componente_i = -1 / 3 * np.sqrt(2)
            else:  # I > 0
                componente_i = 1 / 3 * np.sqrt(2)
            if coluna % 2 == 0:  # I = 1/3sqrt(2)
                componente_i *= 1
            else:  # I = 1/sqrt(2)
                componente_i *= 3

            # Determina componente Q
            if linha in [0, 1]:  # Q > 0
                componente_q = 1 / 3 * np.sqrt(2)
            else:  # Q < 0
                componente_q = -1 / 3 * np.sqrt(2)
            if linha % 2 == 0:  # Q = 1/3sqrt(2)
                componente_q *= 1
            else:  # Q = 1/sqrt(2)
                componente_q *= 3

            amplitude = np.sqrt(componente_i**2 + componente_q**2)
            fase = np.degrees(np.arctan2(componente_q, componente_i)) % 360
            amplitudes[i] = amplitude
            fases[i] = fase

        return amplitudes, fases
