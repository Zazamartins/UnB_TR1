import unittest

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

import util.portadora as portadora


class PortadoraTest(unittest.TestCase):
    def test_plot_diferentes_frequencias(self):
        p1 = portadora.Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)
        p2 = portadora.Portadora(amplitude=1.0, frequencia=5.0, fase=0.0)
        p3 = portadora.Portadora(amplitude=1.0, frequencia=10.0, fase=0.0)

        tempo = np.linspace(0, 1, 1000)

        sinal1 = p1.gerar_portadora(tempo)
        sinal2 = p2.gerar_portadora(tempo)
        sinal3 = p3.gerar_portadora(tempo)

        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.title("Portadora - 1 Hz")
        plt.plot(tempo, sinal1)
        plt.grid()
        plt.subplot(3, 1, 2)
        plt.title("Portadora - 5 Hz")
        plt.plot(tempo, sinal2)
        plt.grid()
        plt.subplot(3, 1, 3)
        plt.title("Portadora - 10 Hz")
        plt.plot(tempo, sinal3)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/portadora_diferentes_frequencias.png")
        plt.close()

        picos_p1, _ = find_peaks(sinal1)
        picos_p2, _ = find_peaks(sinal2)
        picos_p3, _ = find_peaks(sinal3)

        self.assertEqual(len(picos_p1), 1)
        self.assertEqual(len(picos_p2), 5)
        self.assertEqual(len(picos_p3), 10)

    def test_gerar_sinal_mensagem(self):
        p = portadora.Portadora(amplitude=1.0, frequencia=2.0, fase=0.0)
        mensagem_1bit = np.array([0, 1, 0, 1, 0, 1, 0, 0])
        sinal_1 = p.gerar_portadora_para_mensagem(mensagem_1bit)

        mensagem_8bit = np.array([[0, 1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 0, 1, 1]])
        sinal_8 = p.gerar_portadora_para_mensagem(mensagem_8bit)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("1 bit por símbolo com 8 bits na mensagem")
        plt.plot(sinal_1)
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.title("8 bits por símbolo com 2 símbolos na mensagem")
        plt.plot(sinal_8)
        plt.grid()
        plt.tight_layout()
        plt.savefig("images/tests/camada_fisica/portadora_sinais_mensagem.png")
        plt.close()

        picos_sinal_1, _ = find_peaks(sinal_1)
        picos_sinal_8, _ = find_peaks(sinal_8)

        self.assertEqual(len(picos_sinal_1), 8)
        self.assertEqual(len(picos_sinal_8), 2)

    def test_modular_por_amplitude(self):
        p = portadora.Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

        amplitudes = np.array([0.0, 1.0, 0.0, 1.0, 0.0])
        frequencias = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        fases = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        sinal_modulado = p.modular(amplitudes, frequencias, fases)

        plt.figure(figsize=(10, 4))
        plt.title("Modulação por Amplitude")
        plt.plot(sinal_modulado, label="[01010]")
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/portadora_modulacao_amplitude.png")
        plt.close()

        picos_sinal, _ = find_peaks(sinal_modulado)
        self.assertEqual(len(picos_sinal), 2)

    def test_modular_por_frequencia(self):
        p = portadora.Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

        amplitudes = np.array([1.0, 1.0, 1.0, 1.0])
        frequencias = np.array(
            [1.0, 1.0 + 1.0 / (4 - 1), 1.0 + 1.0 / (4 - 2), 1.0 + 1.0 / (4 - 3)]
        )
        fases = np.array([0.0, 0.0, 0.0, 0.0])

        sinal_modulado = p.modular(amplitudes, frequencias, fases)

        plt.figure(figsize=(10, 4))
        plt.title("Modulação por Frequência")
        plt.plot(
            sinal_modulado, label="$1f_c$, $\\frac{4}{3}f_c$, $\\frac{5}{3}f_c$, $2f_c$"
        )
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/portadora_modulacao_frequencia.png")
        plt.close()

        picos_sinal, _ = find_peaks(sinal_modulado)
        self.assertEqual(
            len(picos_sinal), 7
        )  # 1 pico quando f=fc + 2 picos quando f>0.3fc

    def test_modular_por_fase(self):
        p = portadora.Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

        amplitudes = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        frequencias = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        fases = np.array([0.0, 45.0, 90.0, 135.0, 180.0])

        sinal_modulado = p.modular(amplitudes, frequencias, fases)

        plt.figure(figsize=(10, 4))
        plt.title("Modulação por Fase")
        plt.plot(sinal_modulado, label="[0°, 45°, 90°, 135°, 180°]")
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/portadora_modulacao_fase.png")
        plt.close()

        picos_sinal, _ = find_peaks(sinal_modulado)
        self.assertEqual(len(picos_sinal), 6)

    def test_modular_por_amplitude_frequencia_alta(self):
        p = portadora.Portadora(amplitude=1.0, frequencia=1000.0, fase=0.0, taxa_amostragem=5000)

        amplitudes = np.array([0.0, 1.0, 0.0, 1.0, 0.0])
        frequencias = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        fases = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        
        sinal_modulado = p.modular(amplitudes, frequencias, fases)
        picos_sinal, _ = find_peaks(sinal_modulado)
        self.assertEqual(len(picos_sinal), 2000) # 1000 para cada amplitude 1 com frequencia 1000 Hz
        self.assertEqual(len(sinal_modulado), 25000) # 5 simbolos de 1/1000s com taxa de amostragem 5000 Hz
        
        plt.figure(figsize=(10, 4))
        plt.title("Modulação por Amplitude - Alta Frequência")
        plt.plot(sinal_modulado, label="[01010] - 1kHz")
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig("images/tests/camada_fisica/portadora_modulacao_amplitude_alta_frequencia.png")
        plt.close()