import unittest

import numpy as np
import numpy.testing as npt
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

from CamadaFisica import TransmissorBandaBase, QAM16, Modulador, Gray, Sinal


class TestTransmissorBandaBase(unittest.TestCase):
    def test_nrz_polar(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_4bits = transmissor_4bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_1bit = transmissor_1bit.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )

        self.assertEqual(out_8bits.shape[0], 43)  # 43 símbolos de 8 bits
        self.assertEqual(out_4bits.shape[0], 86)  # 86 símbolos de 4 bits
        self.assertEqual(out_1bit.shape[0], 344)  # 344 símbolos de 1 bit

        # [-1, 1, -1, 1, -1, 1, -1, -1] = -128 + 64 - 32 + 16 - 8 + 4 - 2 - 1 = -87
        # 1/(2**8-1) = 0.00392156862
        # => -87 * 0.00392156862 = -0.34117647058
        npt.assert_array_almost_equal(
            out_8bits[0][np.argmax(np.abs(out_8bits[0]))],
            [-0.34117647058 * transmissor_8bits.tensao_pico],
        )

        # [-1, 1, -1, 1] = -8 + 4 - 2 + 1 = -5
        # 1/(2**4-1) = 0.06666666667
        # => -5 * 0.06666666667 = -0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[0][np.argmax(np.abs(out_4bits[0]))],
            [-0.33333333335 * transmissor_4bits.tensao_pico],
        )

        # [-1] = -1
        # 1/(2**1-1) = 1
        # => -1 * 1 = -1
        npt.assert_array_equal(
            out_1bit[0][np.argmax(np.abs(out_1bit[0]))],
            [-1.0 * transmissor_1bit.tensao_pico],
        )

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação NRZ Polar - 8 bits por símbolo")
        tempo = np.arange(0, len(out_8bits) * transmissor_8bits.taxa_amostragem + 1) / (
            transmissor_8bits.frequencia_de_simbolo * transmissor_8bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação NRZ Polar - 4 bits por símbolo")
        tempo = np.arange(0, len(out_4bits) * transmissor_4bits.taxa_amostragem + 1) / (
            transmissor_4bits.frequencia_de_simbolo * transmissor_4bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação NRZ Polar - 1 bit por símbolo")
        tempo = np.arange(0, len(out_1bit) * transmissor_1bit.taxa_amostragem + 1) / (
            transmissor_1bit.frequencia_de_simbolo * transmissor_1bit.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/transmissor_codificacao_nrz_polar.png")
        plt.close()

    def test_bipolar(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_4bits = transmissor_4bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_1bit = transmissor_1bit.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )

        # [0, 1, 0, 1, 0, 1, 0, 0] = 64 + 16 + 4 = 84
        # 1/(2**8-1) = 0.00392156862
        # => 84 * 0.00392156862 = 0.32941176408
        npt.assert_array_almost_equal(
            out_8bits[0][np.argmax(np.abs(out_8bits[0]))],
            [0.32941176408 * transmissor_8bits.tensao_pico],
        )

        npt.assert_array_equal(np.max(np.abs(out_8bits[1])), [0.0])

        # [0, -1, -1, 0, -1, 0, 0, 0] = -64 -32 -8 = -104
        # 1/(2**8-1) = 0.00392156862
        # => -104 * 0.00392156862 = -0.40784313748
        npt.assert_array_almost_equal(
            out_8bits[2][np.argmax(np.abs(out_8bits[2]))],
            [-0.40784313748 * transmissor_8bits.tensao_pico],
        )

        # [0, 1, 0, 1] = 4 + 1 = 5
        # 1/(2**4-1) = 0.06666666667
        # => 5 * 0.06666666667 = 0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[0][np.argmax(np.abs(out_4bits[0]))],
            [0.33333333335 * transmissor_4bits.tensao_pico],
        )
        npt.assert_array_equal(out_4bits[1][np.argmax(np.abs(out_4bits[1]))], [0.0])
        # [0, -1, 0, 0] = -4
        # 1/(2**4-1) = 0.06666666667
        # => -4 * 0.06666666667 = -0.26666666668
        npt.assert_array_almost_equal(
            out_4bits[2][np.argmax(np.abs(out_4bits[2]))],
            [-0.26666666668 * transmissor_4bits.tensao_pico],
        )

        npt.assert_array_equal(out_1bit[0][np.argmax(np.abs(out_1bit[0]))], [0.0])
        npt.assert_array_equal(out_1bit[1][np.argmax(np.abs(out_1bit[1]))], [0.0])
        npt.assert_array_equal(
            out_1bit[2][np.argmax(np.abs(out_1bit[2]))],
            [1.0 * transmissor_1bit.tensao_pico],
        )

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação Bipolar - 8 bits por símbolo")
        # ValueError: x and y must have same first dimension, but have shapes (87,) and (86001,)
        tempo = np.arange(0, len(out_8bits) * transmissor_8bits.taxa_amostragem + 1) / (
            transmissor_8bits.frequencia_de_simbolo * transmissor_8bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.ylim(-4, 4)
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação Bipolar - 4 bits por símbolo")
        tempo = np.arange(0, len(out_4bits) * transmissor_4bits.taxa_amostragem + 1) / (
            transmissor_4bits.frequencia_de_simbolo * transmissor_4bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação Bipolar - 1 bit por símbolo")
        tempo = np.arange(0, len(out_1bit) * transmissor_1bit.taxa_amostragem + 1) / (
            transmissor_1bit.frequencia_de_simbolo * transmissor_1bit.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/transmissor_codificacao_bipolar.png")
        plt.close()

    def test_manchester(self):
        transmissor_8bits = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=8, debug=True
        )
        transmissor_4bits = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=4, debug=True
        )
        transmissor_1bit = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=1, debug=True
        )

        out_8bits = transmissor_8bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_4bits = transmissor_4bits.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )
        out_1bit = transmissor_1bit.processar_sinal(
            bits=Sinal.gerar_sinal_binario(
                "The quick brown fox jumps over the lazy dog"
            )
        )

        # 01010100 ^ 1 = 01010100
        # [1, 0, 1, 0, 1, 0, 1, 1] = 128 + 0 + 32 + 0 + 8 + 0 + 2 + 1 = 171
        # 1/(2**8-1) = 0.00392156862
        # => 171 * 0.00392156862 = 0.67058823502
        npt.assert_array_almost_equal(
            out_8bits[0][np.argmax(np.abs(out_8bits[0]))],
            [0.67058823502 * transmissor_8bits.tensao_pico],
        )
        # 01010100 ^ 0 = 10101011
        # [0, 1, 0, 1, 0, 1, 0, 0] = 64 + 16 + 4 = 84
        # 1/(2**8-1) = 0.00392156862
        # => 84 * 0.00392156862 = 0.32941176408
        npt.assert_array_almost_equal(
            out_8bits[1][np.argmax(np.abs(out_8bits[1]))],
            [0.32941176408 * transmissor_8bits.tensao_pico],
        )

        # 0101 ^ 1 = 0101
        # [1, 0, 1, 0] = 8 + 0 + 2 + 0 = 10
        # 1/(2**4-1) = 0.06666666667
        # => 10 * 0.06666666667 = 0.6666666667
        npt.assert_array_almost_equal(
            out_4bits[0][np.argmax(np.abs(out_4bits[0]))],
            [0.6666666667 * transmissor_4bits.tensao_pico],
        )
        # 0101 ^ 0 = 1010
        # [0, 1, 0, 1] = 4 + 0 + 1 = 5
        # 1/(2**4-1) = 0.06666666667
        # => 5 * 0.06666666667 = 0.33333333335
        npt.assert_array_almost_equal(
            out_4bits[1][np.argmax(np.abs(out_4bits[1]))],
            [0.33333333335 * transmissor_4bits.tensao_pico],
        )

        npt.assert_array_equal(
            out_1bit[0][np.argmax(np.abs(out_1bit[0]))],
            [1.0 * transmissor_1bit.tensao_pico],
        )
        npt.assert_array_equal(
            out_1bit[1][np.argmax(np.abs(out_1bit[1]))],
            [0.0 * transmissor_1bit.tensao_pico],
        )

        plt.figure(figsize=(20, 6))
        plt.subplot(3, 1, 1)
        plt.title("Codificação Manchester - 8 bits por símbolo")
        tempo = np.arange(0, len(out_8bits) * transmissor_8bits.taxa_amostragem + 1) / (
            transmissor_8bits.frequencia_de_simbolo * transmissor_8bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_8bits.flatten(), out_8bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Codificação Manchester - 4 bits por símbolo")
        tempo = np.arange(0, len(out_4bits) * transmissor_4bits.taxa_amostragem + 1) / (
            transmissor_4bits.frequencia_de_simbolo * transmissor_4bits.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_4bits.flatten(), out_4bits.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Codificação Manchester - 1 bit por símbolo")
        tempo = np.arange(0, len(out_1bit) * transmissor_1bit.taxa_amostragem + 1) / (
            transmissor_1bit.frequencia_de_simbolo * transmissor_1bit.taxa_amostragem
        )
        plt.plot(
            tempo,
            np.append(out_1bit.flatten(), out_1bit.flatten()[-1]),
            drawstyle="steps-post",
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/transmissor_codificacao_manchester.png")
        plt.close()

    def test_modulador_ask(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=1,
            modulacao="ask",
            debug=True,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=Sinal.gerar_sinal_binario("The")
        )

        picos, _ = find_peaks(sinal_modulado)

        self.assertEqual(
            len(picos), 10
        )  # [0,1,0,1,0,1,0,0, 0,1,1,0,1,0,0,0, 0,1,1,0,0,1,0,1] = 10 1's

        plt.figure(figsize=(15, 4))
        plt.title("Modulação ASK")
        plt.plot(sinal_modulado, label="Mensagem: 'The'")
        for i in range(
            0, len(sinal_modulado), int(modulador.portadora.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/transmissor_modulacao_ask.png")
        plt.close()

    def test_modulador_fsk(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=1,
            modulacao="fsk",
            debug=True,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=Sinal.gerar_sinal_binario("The")
        )

        picos, _ = find_peaks(sinal_modulado)

        self.assertEqual(
            len(picos), 34
        )  # [0,1,0,1,0,1,0,0, 0,1,1,0,1,0,0,0, 0,1,1,0,0,1,0,1] = dois picos quando 1 e um pico quando 0 = 10*2 + 14*1 = 34

        plt.figure(figsize=(15, 4))
        plt.title("Modulação FSK")
        plt.plot(sinal_modulado, label="Mensagem: 'The'")
        for i in range(
            0, len(sinal_modulado), int(modulador.portadora.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/transmissor_modulacao_fsk.png")
        plt.close()

    def test_modulador_psk(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=1,
            modulacao="psk",
            debug=True,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=Sinal.gerar_sinal_binario("The")
        )

        # Essa parte remove máximos locais
        picos, _ = find_peaks(sinal_modulado)
        pico_maximo = picos[np.argmax(sinal_modulado[picos])]
        picos_maximos = picos[
            np.where(sinal_modulado[picos] == sinal_modulado[pico_maximo])
        ]

        self.assertEqual(
            len(picos_maximos), 24
        )  # [0,1,0,1,0,1,0,0, 0,1,1,0,1,0,0,0, 0,1,1,0,0,1,0,1] = um pico por símbolo = 8*3 = 24

        plt.figure(figsize=(15, 4))
        plt.title("Modulação PSK")
        plt.plot(sinal_modulado, label="Mensagem: 'The'")
        for i in range(
            0, len(sinal_modulado), int(modulador.portadora.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/transmissor_modulacao_psk.png")
        plt.close()

    def test_modulador_qpsk(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=2,
            modulacao="qpsk",
            debug=True,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=Sinal.gerar_sinal_binario("The")
        )

        simbolos = [
            [0, 1],  # T
            [0, 1],  # T
            [0, 1],  # T
            [0, 0],  # T
            [0, 1],  # h
            [1, 0],  # h
            [1, 0],  # h
            [0, 0],  # h
            [0, 1],  # e
            [1, 0],  # e
            [0, 1],  # e
            [0, 1],  # e
        ]
        gray = Gray(bits_por_simbolo=2, flag_binario=True).tabela_gray
        simbolos_gray = [gray.tolist().index(s) for s in simbolos]

        plt.figure(figsize=(15, 4))
        plt.title("Modulação QPSK")
        plt.plot(sinal_modulado, label="Mensagem: 'The'")
        for i in range(
            0, len(sinal_modulado), int(modulador.portadora.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
            # Fase
            simbolo_index = i // int(modulador.portadora.taxa_amostragem)
            if simbolo_index < len(simbolos_gray):
                plt.text(
                    i + int(0.4 * modulador.portadora.taxa_amostragem),
                    3.5,
                    f"{simbolos_gray[simbolo_index] * 90}°",
                    color="blue",
                    fontsize=12,
                )
        plt.legend()
        plt.ylim(-4, 4)
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/transmissor_modulacao_qpsk.png")
        plt.close()

    def test_modulador_16qam(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=4,
            modulacao="16-qam",
            debug=True,
        )

        sinal_modulado = modulador.processar_sinal(
            bits=Sinal.gerar_sinal_binario("The")
        )

        simbolos = [
            5,  # [0, 1, 0, 1]  T
            4,  # [0, 1, 0, 0]  T
            6,  # [0, 1, 1, 0]  h
            8,  # [1, 0, 0, 0]  h
            6,  # [0, 1, 1, 0]  e
            5,  # [0, 1, 0, 1]  e
        ]

        picos = []

        for i in range(len(simbolos)):
            inicio = i * int(modulador.portadora.taxa_amostragem)
            fim = (i + 1) * int(modulador.portadora.taxa_amostragem)
            pico = np.max(sinal_modulado[inicio:fim])
            picos.append(pico)

        amplitudes, fases = QAM16().gerar_parametros(np.array(simbolos) / (2**4 - 1))

        npt.assert_array_almost_equal(
            picos,
            amplitudes * 3.3,
            decimal=3,
        )

        plt.figure(figsize=(15, 4))
        plt.title("Modulação 16-QAM")
        plt.plot(sinal_modulado, label="Mensagem: 'The'")
        for i in range(
            0, len(sinal_modulado), int(modulador.portadora.taxa_amostragem)
        ):  # Linhas verticais separando cada símbolo
            plt.axvline(x=i, color="red", linestyle="--", alpha=0.5)
            # Fase e amplitude
            simbolo_index = i // int(modulador.portadora.taxa_amostragem)
            if simbolo_index < len(amplitudes):
                amplitude = round(amplitudes[simbolo_index], 2)
                fase = round(fases[simbolo_index], 1)
            plt.text(
                i + int(0.25 * modulador.portadora.taxa_amostragem),
                3.1,
                f"$A$ = {amplitude}\n$\\Theta$ = {fase}°",
                color="blue",
                fontsize=12,
            )
        plt.legend()
        plt.ylim(-4, 4)
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/transmissor_modulacao_16qam.png")
        plt.close()

    def test_banda_base_dicionario_de_formas_de_onda(self):
        transmissor = TransmissorBandaBase(
            codificacao="nrz_polar", bits_por_simbolo=4, debug=True
        )

        dicionario = transmissor.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                transmissor.frequencia_de_simbolo,
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na codificação NRZ Polar")
            plt.ylim(-4, 4)
            plt.plot(forma_de_onda.flatten())
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_banda_base_forma_de_onda_simbolo.png"
        )
        plt.close()

    def test_banda_base_dicionario_de_formas_de_onda_manchester(self):
        transmissor = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=4, debug=True
        )

        dicionario = transmissor.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                transmissor.frequencia_de_simbolo * 2,  # *2 devido ao clock
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na codificação Manchester")
            plt.ylim(-4, 4)
            plt.plot(forma_de_onda.flatten())
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_banda_base_manchester_forma_de_onda_simbolo.png"
        )
        plt.close()

    def test_banda_base_dicionario_de_formas_de_onda_manchester_1bit(self):
        transmissor = TransmissorBandaBase(
            codificacao="manchester", bits_por_simbolo=1, debug=True
        )

        dicionario = transmissor.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 2)  # 1 bit por símbolo => 2 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                transmissor.frequencia_de_simbolo * 2,  # *2 devido ao clock
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(
                f"Forma de onda do símbolo {simbolo} na codificação NRZ Manchester"
            )
            plt.ylim(-4, 4)
            plt.plot(forma_de_onda.flatten())
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_banda_base_manchester_1bit_forma_de_onda_simbolo.png"
        )
        plt.close()

    def test_banda_base_dicionario_de_formas_de_onda_bipolar(self):
        transmissor = TransmissorBandaBase(
            codificacao="bipolar", bits_por_simbolo=4, debug=True
        )

        dicionario = transmissor.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                transmissor.frequencia_de_simbolo * 2,  # *2 devido ao clock
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na codificação Bipolar")
            plt.ylim(-4, 4)
            plt.plot(forma_de_onda.flatten())
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_banda_base_bipolar_forma_de_onda_simbolo.png"
        )
        plt.close()

    def test_modulador_dicionario_de_formas_de_onda_qpsk(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=2,
            modulacao="qpsk",
            debug=True,
        )

        dicionario = modulador.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 4)  # 2 bits por símbolo => 4 símbolos

        plt.figure(figsize=(10, 8))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                modulador.portadora.taxa_amostragem,
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(2, 2, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na modulação QPSK")
            plt.plot(forma_de_onda)
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_forma_de_onda_simbolo_qpsk.png"
        )
        plt.close()

    def test_modulador_dicionario_de_formas_de_onda_16qam(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=4,
            modulacao="16-qam",
            debug=True,
        )

        dicionario = modulador.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                modulador.portadora.taxa_amostragem,
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na modulação 16-QAM")
            plt.plot(forma_de_onda)
            plt.ylim(-4, 4)
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_forma_de_onda_simbolo_16qam.png"
        )
        plt.close()

    def test_modulador_dicionario_de_formas_de_onda_ask(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=4,
            modulacao="ask",
            debug=True,
        )

        dicionario = modulador.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                modulador.portadora.taxa_amostragem,
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na modulação ASK")
            plt.plot(forma_de_onda)
            plt.ylim(-4, 4)
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_forma_de_onda_simbolo_ask.png"
        )
        plt.close()

    def test_modulador_dicionario_de_formas_de_onda_fsk(self):
        modulador = Modulador(
            tensao_pico=3.3,
            frequencia_portadora=1.0,
            bits_por_simbolo=4,
            modulacao="fsk",
            debug=True,
        )

        dicionario = modulador.gerar_dicionario_de_formas_de_onda()

        self.assertEqual(len(dicionario), 16)  # 4 bits por símbolo => 16 símbolos

        plt.figure(figsize=(20, 12))
        for simbolo, forma_de_onda in dicionario.items():
            self.assertEqual(
                forma_de_onda.shape[0],
                modulador.portadora.taxa_amostragem,
            )  # Cada forma de onda deve ter duração de 1 símbolo
            plt.subplot(4, 4, simbolo + 1)
            plt.title(f"Forma de onda do símbolo {simbolo} na modulação FSK")
            plt.plot(forma_de_onda)
            plt.xlabel("Amostras")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.tight_layout()
        plt.savefig(
            "images/tests/camada_fisica/transmissor_forma_de_onda_simbolo_fsk.png"
        )
        plt.close()


if __name__ == "__main__":
    unittest.main()
