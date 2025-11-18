import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt

from CamadaFisica import Sinal


class TestSinal(unittest.TestCase):
    # T = "01010100"
    # h = "01101000"
    # e = "01100101"
    #   = "00100000"
    # q = "01110001"
    # u = "01110101"
    # i = "01101001"
    # c = "01100011"
    # k = "01101011"
    #   = "00100000"
    # b = "01100010"
    # r = "01110010"
    # o = "01101111"
    # w = "01110111"
    # n = "01101110"
    #   = "00100000"
    # f = "01100110"
    # o = "01101111"
    # x = "01111000"
    #   = "00100000"
    # j = "01101010"
    # u = "01110101"
    # m = "01101101"
    # p = "01110000"
    # s = "01110011"
    #   = "00100000"
    # o = "01101111"
    # v = "01110110"
    # e = "01100101"
    # r = "01110010"
    #   = "00100000"
    # t = "01110100"
    # h = "01101000"
    # e = "01100101"
    #   = "00100000"
    # l = "01101100"
    # a = "01100001"
    # z = "01111010"
    # y = "01111001"
    #   = "00100000"
    # d = "01100100"
    # o = "01101111"
    # g = "01100111"
    def test_fluxo_bits_1_bit_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=1)
        sinal = fonte.gerar_sinal_binario(
            mensagem="The quick brown fox jumps over the lazy dog"
        )

        # T = "01010100"
        t = np.array(
            [
                0,
                1,
                0,
                1,
                0,
                1,
                0,
                0,
            ]
        )

        npt.assert_array_equal(sinal[:8], t)

    def test_fluxo_bits_2_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=2)
        bits = fonte.gerar_sinal_binario(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        sinal = fonte.sequencia_de_bits_para_simbolos(bits)

        # T = "01" "01" "01" "00" = 1110
        t = np.array(
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 0],
            ]
        )

        npt.assert_array_equal(sinal[:4], t)

    def test_fluxo_bits_4_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=4)
        bits = fonte.gerar_sinal_binario(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        sinal = fonte.sequencia_de_bits_para_simbolos(bits)

        # T = "0101" "0100" = 5 4
        t = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])

        npt.assert_array_equal(sinal[:2], t)

    def test_fluxo_bits_8_bits_por_simbolo(self):
        fonte = Sinal(bits_por_simbolo=8)
        bits = fonte.gerar_sinal_binario(
            mensagem="The quick brown fox jumps over the lazy dog"
        )
        sinal = fonte.sequencia_de_bits_para_simbolos(bits)

        # T = "01010100" = 84
        t = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])

        npt.assert_array_equal(sinal[:1], t)

    def test_gerar_curva_tensao_1bit(self):
        fonte = Sinal(bits_por_simbolo=1)
        simbolos = fonte.binario_para_decimal(np.array([0, 1, 1, 0, 0, 0, 1, 0]))
        sinal_com_curva = fonte.gerar_pulso_tensao(simbolos)

        # Plotar 1) o sinal completo e 2) cada símbolo individualmente
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Pulsos de tensão")
        plt.plot(sinal_com_curva.flatten())
        plt.xlabel("Amostras")
        plt.ylabel("Tensão")
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.title("Pulsos gerados por cada símbolo")
        plt.plot(sinal_com_curva[0:2].flatten(), label="01")
        plt.plot(
            sinal_com_curva[2:4].flatten(),
            label="10",
        )
        plt.plot(
            sinal_com_curva[4:6].flatten(),
            label="00",
        )
        plt.plot(
            sinal_com_curva[6:8].flatten(),
            label="10",
        )
        plt.ylabel("Tensão")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/sinal_com_curva_tensao_1bit.png")
        plt.close()

        self.assertEqual(len(sinal_com_curva[0]), fonte.taxa_amostragem)
        self.assertEqual(len(sinal_com_curva), len(simbolos))

    def test_gerar_curva_tensao_4bit(self):
        fonte = Sinal(bits_por_simbolo=4)
        simbolos = fonte.binario_para_decimal(np.array([[0, 1, 0, 1], [0, 1, 0, 0]]))
        sinal_com_curva = fonte.gerar_pulso_tensao(simbolos, tempo_de_simbolo=1)

        # Plotar 1) o sinal completo e 2) cada símbolo individualmente
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Pulsos de tensão (4 bits por símbolo)")
        plt.plot(sinal_com_curva.flatten())
        plt.xlabel("Amostras")
        plt.ylabel("Tensão")
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.title("Pulsos gerados por cada símbolo")
        plt.plot(sinal_com_curva[0], label='"0101"')
        plt.plot(
            sinal_com_curva[1],
            label='"0100"',
        )
        plt.xlabel("Amostras")
        plt.ylabel("Tensão")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/sinal_com_curva_tensao.png")
        plt.close()

        self.assertEqual(len(sinal_com_curva[0]), fonte.taxa_amostragem)
        self.assertEqual(len(sinal_com_curva), len(simbolos))
        
    def test_gerar_curva_mensagem_grande(self):
        fonte = Sinal(bits_por_simbolo=8)
        bits = fonte.gerar_sinal_binario(
            mensagem="The quick brown fox"
        )
        simbolos = fonte.binario_para_decimal(bits)
        sinal_com_curva = fonte.gerar_pulso_tensao(simbolos)

        plt.figure(figsize=(10, 6))
        plt.title("Pulsos de tensão para mensagem 'The quick brown fox'")
        plt.plot(sinal_com_curva.flatten())
        plt.xlabel("Amostras")
        plt.ylabel("Tensão")
        plt.grid()
        for i in range(
            0, len(sinal_com_curva) * int(fonte.taxa_amostragem + 1), int(fonte.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/sinal_com_curva_tensao_mensagem_grande.png")
        plt.close()

        self.assertEqual(len(sinal_com_curva[0]), fonte.taxa_amostragem)
        self.assertEqual(len(sinal_com_curva), len(simbolos))


if __name__ == "__main__":
    unittest.main()
