import unittest

from camadas.fisica.receptor.demodulador import Demodulador
from camadas.fisica.transmissor.modulador import Modulador
from camadas.fisica.receptor.decodificador import Decodificador
from camadas.fisica.transmissor.banda_base import TransmissorBandaBase

import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt

from util.sinal import Sinal


class TestReceptor(unittest.TestCase):

    def test_demodulador_ask(self):
        # Gera o sinal modulado em ASK
        modulador = Modulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (ASK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            print(bits_demodulados)
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_ask.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_ask_4bits(self):
        modulador = Modulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="ask",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (ASK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_ask_4bits.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_fsk(self):
        # Gera o sinal modulado em FSK
        modulador = Modulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (FSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_fsk.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_fsk_4bits(self):
        modulador = Modulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="fsk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (FSK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_fsk_4bits.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_psk(self):
        # Gera o sinal modulado em PSK
        modulador = Modulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(bits=[0, 1, 0, 1, 0, 1, 0, 0])  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (PSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_demodulados:
            forma_onda = formas_de_onda.get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados)
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_psk.png")
        plt.close()

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_psk_4bits(self):
        modulador = Modulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="psk",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (PSK 4 bits por símbolo)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_psk_4bits.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_qpsk(self):
        # Gera o sinal modulado em QPSK
        modulador = Modulador(
            modulacao="qpsk",
            frequencia_portadora=1000,
            bits_por_simbolo=2,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 1, 1, 0, 1, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="qpsk",
            frequencia_portadora=1000,
            bits_por_simbolo=2,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=2, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (QPSK)")
        plt.plot(sinal_modulado)
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**2 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_qpsk.png")
        plt.close()

        expected_bits = np.array([[0, 0], [1, 1], [0, 1], [1, 0]])

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_demodulador_qam16(self):
        # Gera o sinal modulado em QAM16
        modulador = Modulador(
            modulacao="16-qam",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        )  # "T"
        formas_de_onda = modulador.gerar_dicionario_de_formas_de_onda()

        demodulador = Demodulador(
            modulacao="16-qam",
            frequencia_portadora=1000,
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=100 * 1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=100 * 1000)
        bits_demodulados = demodulador.processar_sinal(sinal_modulado)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Modulado (QAM16)")
        plt.plot(sinal_modulado)
        # plota em volts um envelope das formas de onda do dicionário
        envelope_superior = []
        envelope_inferior = []
        for simbolo_decimal in sinal.binario_para_decimal(bits_demodulados):
            forma_onda = formas_de_onda.get(simbolo_decimal * (2**4 - 1))
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Demodulados")
        plt.stem(bits_demodulados.flatten())
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/demodulador_qam16.png")
        plt.close()

        expected_bits = np.array(
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]]
        )

        npt.assert_array_equal(bits_demodulados, expected_bits)

    def test_decodificador_nrz_polar(self):
        # Gera o sinal codificado em NRZ Polar
        banda_base = TransmissorBandaBase(
            codificacao="nrz_polar",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )

        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        decodificador = Decodificador(
            codificacao="nrz_polar",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )

        bits_decodificados = decodificador.processar_sinal(sinal_codificado)

        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Codificado (NRZ Polar)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_decodificados:
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(2, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados, bits_decodificados[-1]), drawstyle="steps-post")
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_nrz_polar.png")
        plt.close()

        npt.assert_array_equal(bits_decodificados, expected_bits)

    def test_decodificador_manchester(self):
        # Gera o sinal codificado em Manchester
        banda_base = TransmissorBandaBase(
            codificacao="manchester",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        print(sinal_codificado.shape)

        decodificador = Decodificador(
            codificacao="manchester",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        bits_decodificados = decodificador.processar_sinal(sinal_codificado)
        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Sinal Codificado (Manchester)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        for bit in bits_decodificados:
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(bit)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(3, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados, bits_decodificados[-1]), drawstyle="steps-post")
        plt.subplot(3, 1, 3)
        plt.title("Sinal de Clock")
        clock = np.tile(
            np.concatenate((np.ones(500), np.zeros(500))),
            8,
        )
        plt.plot(clock[: len(sinal_codificado.flatten())])
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_manchester.png")
        plt.close()

        npt.assert_array_equal(bits_decodificados, expected_bits)

    def test_decodificador_bipolar(self):
        # Gera o sinal codificado em Bipolar
        banda_base = TransmissorBandaBase(
            codificacao="bipolar",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        decodificador = Decodificador(
            codificacao="bipolar",
            bits_por_simbolo=1,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        bits_decodificados = decodificador.processar_sinal(sinal_codificado)
        expected_bits = np.array([0, 1, 0, 1, 0, 1, 0, 0])
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Sinal Codificado (Bipolar)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        flip = False
        for bit in bits_decodificados:
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(bit)
            if flip:
                forma_onda = forma_onda * (-1)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
            if bit == 1:
                flip = not flip
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(3, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados, bits_decodificados[-1]), drawstyle="steps-post")
        # Sinal de clock
        plt.subplot(3, 1, 3)
        plt.title("Sinal de Clock")
        clock = np.tile(
            np.concatenate((np.ones(500), np.zeros(500))),
            8,
        )
        plt.plot(clock[: len(sinal_codificado.flatten())])
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_bipolar.png")
        plt.close()

        npt.assert_array_equal(bits_decodificados, expected_bits)

    def test_decodificador_nrz_polar_4bits(self):
        # Gera o sinal codificado em NRZ Polar
        banda_base = TransmissorBandaBase(
            codificacao="nrz_polar",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )

        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        decodificador = Decodificador(
            codificacao="nrz_polar",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )

        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=1000)

        bits_decodificados = decodificador.processar_sinal(sinal_codificado)

        expected_bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Sinal Codificado (NRZ Polar)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        for bits in bits_decodificados:
            valor_simbolo = sinal.binario_para_decimal(bits)[0] * (2**4 - 1)
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(valor_simbolo)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.ylim(-4, 4)
        plt.subplot(2, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados.flatten(), bits_decodificados.flatten()[-1]), drawstyle="steps-post")
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_nrz_polar_4bits.png")
        plt.close()

        npt.assert_array_equal(bits_decodificados, expected_bits)
    
    def test_decodificador_manchester_4bits(self):
        # Gera o sinal codificado em Manchester
        banda_base = TransmissorBandaBase(
            codificacao="manchester",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        decodificador = Decodificador(
            codificacao="manchester",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=1000)
        bits_decodificados = decodificador.processar_sinal(sinal_codificado)
        expected_bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Sinal Codificado (Manchester)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        for bits in bits_decodificados:
            valor_simbolo = sinal.binario_para_decimal(bits)[0] * (2**4 - 1)
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(valor_simbolo)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(3, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados.flatten(), bits_decodificados.flatten()[-1]), drawstyle="steps-post")
        plt.subplot(3, 1, 3)
        plt.title("Sinal de Clock")
        clock = np.tile(
            np.concatenate((np.ones(250), np.zeros(250))),
            8,
        )
        plt.plot(clock[: len(sinal_codificado.flatten())])
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_manchester_4bits.png")
        plt.close()
        
        npt.assert_array_equal(bits_decodificados, expected_bits)
        
    def test_decodificador_bipolar_4bits(self):
        # Gera o sinal codificado em Bipolar
        banda_base = TransmissorBandaBase(
            codificacao="bipolar",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal_codificado = banda_base.processar_sinal(
            bits=np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        )  # "T"

        decodificador = Decodificador(
            codificacao="bipolar",
            bits_por_simbolo=4,
            tensao_pico=3.3,
            taxa_amostragem=1000,
        )
        sinal = Sinal(bits_por_simbolo=4, taxa_amostragem=1000)
        bits_decodificados = decodificador.processar_sinal(sinal_codificado)
        expected_bits = np.array([[0, 1, 0, 1], [0, 1, 0, 0]])
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Sinal Codificado (Bipolar)")
        plt.plot(sinal_codificado.flatten())
        envelope_superior = []
        envelope_inferior = []
        flip = False
        for bits in bits_decodificados:
            valor_simbolo = sinal.binario_para_decimal(bits)[0] * (2**4 - 1)
            forma_onda = banda_base.gerar_dicionario_de_formas_de_onda().get(valor_simbolo)
            if flip:
                forma_onda = forma_onda * (-1)
            envelope_superior.append(forma_onda + 10 ** (1 / 20))  # 1 dBV
            envelope_inferior.append(forma_onda - 10 ** (1 / 20))  # 1 dBV
            if valor_simbolo != 0:
                flip = not flip
        plt.plot(np.array(envelope_superior).flatten(), color="black", linestyle="--")
        plt.plot(np.array(envelope_inferior).flatten(), color="black", linestyle="--")
        plt.subplot(3, 1, 2)
        plt.title("Bits Decodificados")
        plt.plot(np.append(bits_decodificados.flatten(), bits_decodificados.flatten()[-1]), drawstyle="steps-post")
        plt.subplot(3, 1, 3)
        plt.title("Sinal de Clock")
        clock = np.tile(
            np.concatenate((np.ones(250), np.zeros(250))),
            8,
        )
        plt.plot(clock[: len(sinal_codificado.flatten())])
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/decodificador_bipolar_4bits.png")
        plt.close()
        
        npt.assert_array_equal(bits_decodificados, expected_bits)
        

if __name__ == "__main__":
    unittest.main()
