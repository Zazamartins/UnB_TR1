import unittest

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

from CamadaFisica import Portadora


class PortadoraTest(unittest.TestCase):
    def test_modular_por_amplitude(self):
        p = Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

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
        p = Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

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
        p = Portadora(amplitude=1.0, frequencia=1.0, fase=0.0)

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
        p = Portadora(amplitude=1.0, frequencia=1000.0, fase=0.0, taxa_amostragem=5000)

        amplitudes = np.array([0.0, 1.0, 0.0, 1.0, 0.0])
        frequencias = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        fases = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        sinal_modulado = p.modular(amplitudes, frequencias, fases)
        picos_sinal, _ = find_peaks(sinal_modulado)
        self.assertEqual(
            len(picos_sinal), 2000
        )  # 1000 para cada amplitude 1 com frequencia 1000 Hz
        self.assertEqual(
            len(sinal_modulado), 25000
        )  # 5 simbolos de 1/1000s com taxa de amostragem 5000 Hz

        plt.figure(figsize=(10, 4))
        plt.title("Modulação por Amplitude - Alta Frequência")
        plt.plot(sinal_modulado, label="[01010] - 1kHz")
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig(
            "images/tests/camada_fisica/portadora_modulacao_amplitude_alta_frequencia.png"
        )
        plt.close()
