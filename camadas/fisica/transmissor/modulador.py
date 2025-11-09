import numpy as np

from util.portadora import Portadora
from util.ruido import Ruido
from util.sinal import Sinal

from .base import TransmissorBase

MODULADOCOES = {
    # "ask": ASK,
    # "fsk": FSK,
    # "psk": PSK,
    # "qpsk": QPSK,
    # "16-qam": QAM16,
}


class Modulador(TransmissorBase):
    """Modula a onda portadora conforme sinal que se deseja transmitir."""

    def __init__(
        self,
        modulacao: str,
        largura_de_banda: float,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
    ):
        super().__init__()
        if modulacao.lower() not in MODULADOCOES:
            raise ValueError(f"Modulação '{modulacao}' não implementada.")
        self.modulador = MODULADOCOES[modulacao](bits_por_simbolo)
        self.bits_por_simbolo = bits_por_simbolo
        self.modulacao = modulacao
        self.portadora = Portadora(
            amplitude=tensao_pico, frequencia=largura_de_banda, fase=0
        )

    def transmitir(self, mensagem: str) -> np.ndarray:
        sinal = Sinal(self.bits_por_simbolo)
        ruido = Ruido()
        bits = sinal.gerar_sinal_binario(mensagem)

        simbolos_decimais = sinal.binario_para_decimal(bits)

        amplitudes = np.zeros_like(simbolos_decimais)
        frequencias = np.zeros_like(simbolos_decimais)
        fases = np.zeros_like(simbolos_decimais)

        if self.modulacao == "ask":
            amplitudes = self.modulador.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "fsk":
            frequencias = self.modulador.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "psk":
            fases = self.modulador.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "qpsk":
            fases = self.modulador.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "16-qam":
            amplitudes, fases = self.modulador.gerar_parametros(simbolos_decimais)

        sinal_modulado = self.portadora.modular(amplitudes, frequencias, fases)

        sinal_modulado += ruido.gerar_ruido(sinal_modulado)

        return sinal_modulado
