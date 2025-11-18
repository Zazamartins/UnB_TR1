import unittest

import numpy as np
from matplotlib import pyplot as plt

from CamadaFisica import Gray

class GrayTest(unittest.TestCase):
    def test_gray_binario(self):
        gray_2bits = Gray(bits_por_simbolo=2, flag_binario=True)
        tabela_2bits = gray_2bits.tabela_gray

        bits_esperados_2bits = [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0],
        ]

        np.testing.assert_array_equal(tabela_2bits, bits_esperados_2bits)

        gray_3bits = Gray(bits_por_simbolo=3, flag_binario=True)
        tabela_3bits = gray_3bits.tabela_gray

        bits_esperados_3bits = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
            [1, 0, 1],
            [1, 0, 0],
        ]

        np.testing.assert_array_equal(tabela_3bits, bits_esperados_3bits)

        gray_4bits = Gray(bits_por_simbolo=4, flag_binario=True)
        tabela_4bits = gray_4bits.tabela_gray
        bits_esperados_4bits = [
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 0],
            [1, 0, 1, 0],
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 0],
        ]
        np.testing.assert_array_equal(tabela_4bits, bits_esperados_4bits)

        plt.figure(figsize=(6, 12))
        plt.subplot(2, 1, 1)
        plt.title("Codificação Gray (2 bits por símbolo)")
        plt.xlabel("Componente I")
        plt.ylabel("Componente Q")
        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        for i in range(len(tabela_2bits)):
            angle = (2 * np.pi / len(tabela_2bits)) * i
            x = np.cos(angle)
            y = np.sin(angle)
            plt.plot(x, y, "bo")
            plt.text(
                x * 1.1,
                y * 1.1,
                str(tabela_2bits[i]),
                ha="center",
                va="center",
            )
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.title("Codificação Gray (4 bits por símbolo)")
        plt.xlabel("Componente I")
        plt.ylabel("Componente Q")
        plt.xlim(-1.5, 1.5)
        plt.ylim(-1.5, 1.5)
        for i in range(len(tabela_4bits)):
            angle = (2 * np.pi / len(tabela_4bits)) * i
            x = np.cos(angle)
            y = np.sin(angle)
            plt.plot(x, y, "bo")
            plt.text(
                x * 1.1,
                y * 1.1,
                str(tabela_4bits[i]),
                ha="center",
                va="center",
            )
        plt.grid()
        plt.savefig("images/tests/camada_fisica/gray_binario.png")
        plt.close()
