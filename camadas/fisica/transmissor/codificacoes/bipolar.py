import numpy as np

from .base import CodificacaoBase


class Bipolar(CodificacaoBase):
    """Codificação Bipolar ou AMI:
    Se clock é baixo, transmite 0. Do contrário:
    - Se bits 1, transmite pulsos positivos e negativos alternados. Se bit 0, transmite 0.
    """

    def __init__(self):
        self._ultimo_sinal = 1.0  # alterna +1/-1 para bits 1

    def codificar(self, bits: np.ndarray) -> np.ndarray:
        # Diferente de 0 somente quando clock é alto
        self._ultimo_sinal = 1.0
        clock = self.__clock(bits)
        saida = []

        for i, clk in enumerate(clock):
            # Cada símbolo dura um ciclo de clock (rising + falling edges)
            i_mensagem = i // 2
            simbolo = bits[i_mensagem]
            mais_de_um_bit_por_simbolo = (
                simbolo.ndim > 0 if i_mensagem < len(bits) else False
            )

            # Quando clock é alto, transmite 1 ou -1 de forma alternada
            if clk == 1.0:
                if mais_de_um_bit_por_simbolo and simbolo.any():
                    simbolo_saida = simbolo * self._ultimo_sinal
                    self._ultimo_sinal *= -1.0

                    saida.append(simbolo_saida)
                elif mais_de_um_bit_por_simbolo:
                    saida.append([0.0] * len(simbolo))
                else:
                    if simbolo == 1:
                        saida.append(self._ultimo_sinal)
                        self._ultimo_sinal *= -1.0
                    else:
                        saida.append(0.0)
            # Quando clock é baixo, transmite 0
            else:
                if mais_de_um_bit_por_simbolo:
                    saida.append([0.0] * len(simbolo))
                else:
                    saida.append(0.0)

        return np.array(saida)

    def __clock(self, bits: np.ndarray) -> np.ndarray:
        clock = np.zeros(len(bits) * 2)

        for i in range(len(clock)):
            if i % 2 == 0:
                clock[i] = 1.0
            else:
                clock[i] = 0.0

        return clock
