import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt

from CamadaFisica import Bipolar, Manchester, NRZPolar

class TestCodificacoes(unittest.TestCase):
    def test_nrz_polar(self):
        codificador = NRZPolar()

        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado_8bits = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(sinal_codificado_8bits[0], [-1, 1, -1, 1, -1, 1, -1, -1])

        sinal_codificado_4bits = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado_4bits[0], [-1, 1, -1, 1])
        npt.assert_array_equal(sinal_codificado_4bits[1], [-1, 1, -1, -1])

        sinal_codificado_1bit = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado_1bit[0], [-1])
        npt.assert_array_equal(sinal_codificado_1bit[1], [1])
        npt.assert_array_equal(sinal_codificado_1bit[2], [-1])
        npt.assert_array_equal(sinal_codificado_1bit[3], [1])
        npt.assert_array_equal(sinal_codificado_1bit[4], [-1])
        npt.assert_array_equal(sinal_codificado_1bit[5], [1])
        npt.assert_array_equal(sinal_codificado_1bit[6], [-1])
        npt.assert_array_equal(sinal_codificado_1bit[7], [-1])

        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("NRZ Polar - 8 bits por símbolo")
        # Repete último bit somente para plotar com steps-post
        plt.plot(
            np.append(
                sinal_codificado_8bits.flatten(), sinal_codificado_8bits.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("NRZ Polar - 4 bits por símbolo")
        # Repete último bit somente para plotar com steps-post
        plt.plot(
            np.append(
                sinal_codificado_4bits.flatten(), sinal_codificado_4bits.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("NRZ Polar - 1 bit por símbolo")
        # Repete último bit somente para plotar com steps-post
        plt.plot(
            np.append(
                sinal_codificado_1bit.flatten(), sinal_codificado_1bit.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/codificacao_nrz_polar.png")
        plt.close()

    def test_bipolar(self):
        codificador = Bipolar()

        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado_8bits = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(sinal_codificado_8bits[0], [0, 1, 0, 1, 0, 1, 0, 0])
        npt.assert_array_equal(sinal_codificado_8bits[1], [0, 0, 0, 0, 0, 0, 0, 0])
        npt.assert_array_equal(
            sinal_codificado_8bits[2], [-0, -1, -1, -0, -1, -0, -0, -0]
        )
        npt.assert_array_equal(sinal_codificado_8bits[3], [0, 0, 0, 0, 0, 0, 0, 0])

        sinal_codificado_4bits = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado_4bits[0], [0, 1, 0, 1])
        npt.assert_array_equal(sinal_codificado_4bits[1], [0, 0, 0, 0])
        npt.assert_array_equal(sinal_codificado_4bits[2], [0, -1, 0, 0])

        sinal_codificado_1bit = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado_1bit[0], [0])
        npt.assert_array_equal(sinal_codificado_1bit[1], [0])
        npt.assert_array_equal(sinal_codificado_1bit[2], [1])
        npt.assert_array_equal(sinal_codificado_1bit[3], [0])
        npt.assert_array_equal(sinal_codificado_1bit[4], [0])
        npt.assert_array_equal(sinal_codificado_1bit[5], [0])
        npt.assert_array_equal(sinal_codificado_1bit[6], [-1])
        npt.assert_array_equal(sinal_codificado_1bit[7], [0])
        npt.assert_array_equal(sinal_codificado_1bit[8], [0])
        npt.assert_array_equal(sinal_codificado_1bit[9], [0])
        npt.assert_array_equal(sinal_codificado_1bit[10], [1])
        npt.assert_array_equal(sinal_codificado_1bit[11], [0])
        npt.assert_array_equal(sinal_codificado_1bit[12], [0])
        npt.assert_array_equal(sinal_codificado_1bit[13], [0])
        npt.assert_array_equal(sinal_codificado_1bit[14], [0])
        npt.assert_array_equal(sinal_codificado_1bit[15], [0])

        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Bipolar - 8 bits por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_8bits.flatten(), sinal_codificado_8bits.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Bipolar - 4 bits por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_4bits.flatten(), sinal_codificado_4bits.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Bipolar - 1 bit por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_1bit.flatten(), sinal_codificado_1bit.flatten()[-1]
            ),
            drawstyle="steps-post",
        )
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/codificacao_bipolar.png")
        plt.close()

    def test_manchester(self):
        codificador = Manchester()

        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0]])
        mensagem_4bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        sinal_codificado_8bits = codificador.codificar(mensagem_8bits)
        npt.assert_array_equal(
            sinal_codificado_8bits[0], [1, 0, 1, 0, 1, 0, 1, 1]
        )  # 01010100 ^ 1 = 01010100
        npt.assert_array_equal(
            sinal_codificado_8bits[1], [0, 1, 0, 1, 0, 1, 0, 0]
        )  # 01010100 ^ 0 = 10101011

        sinal_codificado_4bits = codificador.codificar(mensagem_4bits)
        npt.assert_array_equal(sinal_codificado_4bits[0], [1, 0, 1, 0])
        npt.assert_array_equal(sinal_codificado_4bits[1], [0, 1, 0, 1])

        sinal_codificado_1bit = codificador.codificar(mensagem_1bit)
        npt.assert_array_equal(sinal_codificado_1bit[0], [1])
        npt.assert_array_equal(sinal_codificado_1bit[1], [0])

        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Manchester - 8 bits por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_8bits.flatten(), sinal_codificado_8bits.flatten()[-1]
            ),
            drawstyle="steps-post",
            label="Clock = [1,0]",
        )
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Manchester - 4 bits por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_4bits.flatten(), sinal_codificado_4bits.flatten()[-1]
            ),
            drawstyle="steps-post",
            label="Clock = [1,0,1,0]",
        )
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Manchester - 1 bit por símbolo")
        plt.plot(
            np.append(
                sinal_codificado_1bit.flatten(), sinal_codificado_1bit.flatten()[-1]
            ),
            drawstyle="steps-post",
            label="Clock = [1,0,1,0,1,0,1,0]",
        )
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/codificacao_manchester.png")
        plt.close()


if __name__ == "__main__":
    unittest.main()
