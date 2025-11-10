import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt

import camadas.fisica.transmissor.modulacoes as modulacoes
from util.gray import Gray
from util.sinal import Sinal


class TestModulacoes(unittest.TestCase):
    def test_ask_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=1)
        decimal_mensagem_1bit = sinal.binario_para_decimal(
            np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0])
        )
        sinal.bits_por_simbolo = 4
        decimal_mensagem_4bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0]])
        )
        sinal.bits_por_simbolo = 8
        decimal_mensagem_8bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        )

        ask_1bit = modulacoes.ASK()
        ask_4bits = modulacoes.ASK()
        ask_8bits = modulacoes.ASK()

        amplitudes_1bit = ask_1bit.gerar_parametros(decimal_mensagem_1bit)
        amplitudes_4bits = ask_4bits.gerar_parametros(decimal_mensagem_4bits)
        amplitudes_8bits = ask_8bits.gerar_parametros(decimal_mensagem_8bits)

        npt.assert_array_almost_equal(amplitudes_1bit, decimal_mensagem_1bit)

        npt.assert_array_almost_equal(amplitudes_4bits, decimal_mensagem_4bits)

        npt.assert_array_almost_equal(amplitudes_8bits, decimal_mensagem_8bits)

        plt.figure(figsize=(10, 12))
        plt.subplot(3, 1, 1)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (1 bit por símbolo)")
        plt.stem(amplitudes_1bit)
        plt.ylim(-0.5, 1.5)
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (4 bits por símbolo)")
        plt.stem(amplitudes_4bits)
        plt.ylim(-0.5, 1.5)
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Modulação ASK - Amplitudes dos Símbolos (8 bits por símbolo)")
        plt.stem(amplitudes_8bits)
        plt.ylim(-0.5, 1.5)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_ask.png")

    def test_fsk_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=1)
        decimal_mensagem_1bit = sinal.binario_para_decimal(
            np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0])
        )
        sinal.bits_por_simbolo = 4
        decimal_mensagem_4bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0]])
        )
        sinal.bits_por_simbolo = 8
        decimal_mensagem_8bits = sinal.binario_para_decimal(
            np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        )

        fsk_1bit = modulacoes.FSK()
        fsk_4bits = modulacoes.FSK()
        fsk_8bits = modulacoes.FSK()

        frequencias_1bit = fsk_1bit.gerar_parametros(decimal_mensagem_1bit)
        frequencias_4bits = fsk_4bits.gerar_parametros(decimal_mensagem_4bits)
        frequencias_8bits = fsk_8bits.gerar_parametros(decimal_mensagem_8bits)

        npt.assert_array_almost_equal(
            frequencias_1bit,
            decimal_mensagem_1bit + 1,
        )

        npt.assert_array_almost_equal(frequencias_4bits, decimal_mensagem_4bits + 1)

        npt.assert_array_almost_equal(frequencias_8bits, decimal_mensagem_8bits + 1)

        plt.figure(figsize=(10, 12))
        plt.subplot(3, 1, 1)
        plt.title("Modulação FSK - Frequências dos Símbolos (1 bit por símbolo)")
        plt.stem(frequencias_1bit, label="$f$ = $y\cdot f_c$")
        plt.ylim(-0.5, 2.5)
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Modulação FSK - Frequências dos Símbolos (4 bits por símbolo)")
        plt.stem(frequencias_4bits, label="$f$ = $y\cdot f_c$")
        plt.ylim(-0.5, 2.5)
        plt.legend()
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Modulação FSK - Frequências dos Símbolos (8 bits por símbolo)")
        plt.stem(frequencias_8bits, label="$f$ = $y\cdot f_c$")
        plt.ylim(-0.5, 2.5)
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_fsk.png")

    def test_psk_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=1)
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0])
        decimal_mensagem_1bit = sinal.binario_para_decimal(mensagem_1bit)
        sinal.bits_por_simbolo = 4
        mensagem_4bits = np.array(
            [[0, 1, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0]]
        )
        decimal_mensagem_4bits = sinal.binario_para_decimal(mensagem_4bits)
        sinal.bits_por_simbolo = 8
        mensagem_8bits = np.array([[0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0]])
        decimal_mensagem_8bits = sinal.binario_para_decimal(mensagem_8bits)

        psk_1bit = modulacoes.PSK(bits_por_simbolo=1)
        psk_4bits = modulacoes.PSK(bits_por_simbolo=4)
        psk_8bits = modulacoes.PSK(bits_por_simbolo=8)

        fases_1bit = psk_1bit.gerar_parametros(decimal_mensagem_1bit)
        fases_4bits = psk_4bits.gerar_parametros(decimal_mensagem_4bits)
        fases_8bits = psk_8bits.gerar_parametros(decimal_mensagem_8bits)

        npt.assert_array_almost_equal(
            fases_1bit,
            decimal_mensagem_1bit * 180,
        )

        gray_4bits = Gray(bits_por_simbolo=4, normalizado=True)
        tabela_gray_4bits = gray_4bits.tabela_gray
        fases_esperadas_4bits = [
            np.where(tabela_gray_4bits == simbolo)[0][0] * (360 / 16)
            for simbolo in decimal_mensagem_4bits
        ]

        npt.assert_array_almost_equal(fases_4bits, np.array(fases_esperadas_4bits))

        gray_8bits = Gray(bits_por_simbolo=8, normalizado=True)
        tabela_gray_8bits = gray_8bits.tabela_gray
        fases_esperadas_8bits = [
            np.where(tabela_gray_8bits == simbolo)[0][0] * (360 / 256)
            for simbolo in decimal_mensagem_8bits
        ]

        npt.assert_array_almost_equal(fases_8bits, np.array(fases_esperadas_8bits))
        print(fases_8bits)

        plt.figure(figsize=(10, 12))
        plt.subplot(3, 1, 1)
        plt.title("Modulação PSK - Fases dos Símbolos (1 bit por símbolo)")
        plt.stem(fases_1bit)
        plt.ylim(-10, 370)
        plt.yticks(np.arange(0, 361, 30))
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Modulação PSK - Fases dos Símbolos (4 bits por símbolo)")
        plt.stem(fases_4bits)
        plt.ylim(-10, 370)
        plt.yticks(np.arange(0, 361, 30))
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Modulação PSK - Fases dos Símbolos (8 bits por símbolo)")
        plt.stem(fases_8bits)
        plt.ylim(-10, 370)
        plt.yticks(np.arange(0, 361, 30))
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_psk.png")

    def test_qpsk_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=2)
        decimal_mensagem_2bits = sinal.binario_para_decimal(
            np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0, 1], [1, 0]])
        )

        qpsk = modulacoes.QPSK()

        fases_2bits = qpsk.gerar_parametros(decimal_mensagem_2bits)

        npt.assert_array_almost_equal(
            fases_2bits,
            decimal_mensagem_2bits * (360 / (2**2)),
        )

        plt.figure(figsize=(10, 4))
        plt.title("Modulação QPSK - Fases dos Símbolos (2 bits por símbolo)")
        plt.stem(fases_2bits)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_qpsk.png")

    def test_qam16_gerar_parametros(self):
        sinal = Sinal(bits_por_simbolo=4)
        decimal_mensagem_4bits = sinal.binario_para_decimal(
            np.array(
                [
                    [0, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 1],
                    [0, 1, 0, 0],
                    [0, 1, 0, 1],
                    [0, 1, 1, 0],
                    [0, 1, 1, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 1],
                    [1, 0, 1, 0],
                    [1, 0, 1, 1],
                    [1, 1, 0, 0],
                    [1, 1, 0, 1],
                    [1, 1, 1, 0],
                    [1, 1, 1, 1],
                ]
            )
        )

        qam16 = modulacoes.QAM16()

        amplitudes_4bits, fases_4bits = qam16.gerar_parametros(decimal_mensagem_4bits)

        amplitude_I = np.array(
            [
                -1 / (3 * np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                -1 / (np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                -1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
                1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
                1 / (np.sqrt(2)),
            ]
        )

        amplitude_Q = np.array(
            [
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                -1 / (3 * np.sqrt(2)),
                -1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
                1 / (3 * np.sqrt(2)),
                1 / (np.sqrt(2)),
            ]
        )

        amplitudes_esperadas = np.sqrt(amplitude_I**2 + amplitude_Q**2)
        fases_esperadas = np.degrees(np.arctan2(amplitude_Q, amplitude_I)) % 360

        npt.assert_array_almost_equal(amplitudes_4bits, amplitudes_esperadas)

        npt.assert_array_almost_equal(
            fases_4bits,
            fases_esperadas,
        )

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Modulação 16-QAM - Amplitudes dos Símbolos (4 bits por símbolo)")
        plt.stem(amplitudes_4bits)
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.title("Modulação 16-QAM - Fases dos Símbolos (4 bits por símbolo)")
        plt.stem(fases_4bits)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/modulacao_16qam.png")
