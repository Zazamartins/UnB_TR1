import numpy as np


class Gray:
    def __init__(
        self,
        bits_por_simbolo: int,
        normalizado: bool = False,
        flag_binario: bool = False,
    ):
        self.bits_por_simbolo = bits_por_simbolo
        self.normalizado = normalizado
        self.flag_binario = flag_binario
        self._tabela_gray = self._gerar_tabela_gray()

    @property
    def tabela_gray(self) -> np.ndarray:
        return self._tabela_gray

    def _gerar_tabela_gray(self) -> np.ndarray:
        """
        Gera a tabela de códigos Gray para o número de bits por símbolo.
        Referência: https://stackoverflow.com/questions/38738835/generating-gray-codes-recursively-without-initialising-the-base-case-outside-of
        """
        num_simbolos = 2**self.bits_por_simbolo
        tabela = []

        for i in range(num_simbolos):
            gray_code = i ^ (i >> 1)
            if self.flag_binario:
                binario = format(gray_code, f"0{self.bits_por_simbolo}b")
                gray_code = [int(bit) for bit in binario]
            tabela.append(gray_code)

        tabela = np.array(tabela)

        if self.normalizado:
            tabela = tabela / (num_simbolos - 1)

        return tabela
