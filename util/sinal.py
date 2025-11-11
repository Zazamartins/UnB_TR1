import numpy as np
from scipy.stats import norm


class Sinal:
    """Classe que converte uma mensagem de texto em um sinal digital."""

    def __init__(self, bits_por_simbolo: int = 1, taxa_amostragem: int = 1000):
        self._bits_por_simbolo = bits_por_simbolo
        self._taxa_amostragem = taxa_amostragem

    @property
    def bits_por_simbolo(self) -> int:
        return self._bits_por_simbolo

    @property
    def taxa_amostragem(self) -> int:
        return self._taxa_amostragem

    @bits_por_simbolo.setter
    def bits_por_simbolo(self, valor: int):
        self._bits_por_simbolo = valor

    def gerar_sinal_binario(self, mensagem: str) -> np.ndarray:
        """Converte a mensagem em uma sequência de bits."""
        bits = "".join(format(ord(c), "08b") for c in mensagem)
        bits = np.array([int(b) for b in bits])

        if self.bits_por_simbolo > 1:
            num_simbolos = len(bits) // self.bits_por_simbolo
            bits = bits[: num_simbolos * self.bits_por_simbolo]  # Trunca bits extras
            bits = bits.reshape((num_simbolos, self.bits_por_simbolo))

        return bits

    def gerar_pulso_tensao(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Gera uma curva sigma simulando um pulso elétrico."""
        sinal_com_curva = []

        for i, valor in enumerate(simbolos_decimais):
            duracao_pulso = 1.0
            num_amostras = int(self.taxa_amostragem * duracao_pulso)
            tempo = np.linspace(0, duracao_pulso, num_amostras)

            curva_sigma = norm.pdf(
                tempo, loc=duracao_pulso / 2, scale=duracao_pulso / 6
            )
            curva_sigma /= np.max(curva_sigma)  # Normaliza para o pico em 1
            curva_sigma *= valor  # Escala pelo valor decimal do símbolo

            sinal_com_curva.append(curva_sigma)

        sinal_com_curva = np.array(sinal_com_curva)

        return sinal_com_curva

    def binario_para_decimal(self, bits: np.ndarray) -> np.ndarray:
        """Converte uma sequência de símbolos em uma sequência de seus respectivos decimais, normalizados (de 0 a 1)."""
        sinal = []
        passo_de_tensao = 1 / (2**self.bits_por_simbolo - 1)

        if self.bits_por_simbolo > 1:
            for simbolo in bits:
                valor_simbolo = 0
                for i, bit in enumerate(simbolo):
                    valor_simbolo += bit * (2 ** (self.bits_por_simbolo - i - 1))
                nivel_tensao = valor_simbolo * passo_de_tensao
                sinal.append(nivel_tensao)
        else:
            for bit in bits:
                nivel_tensao = bit * passo_de_tensao
                sinal.append(nivel_tensao)

        return np.array(sinal)
