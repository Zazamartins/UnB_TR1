import numpy as np

from camadas.fisica.transmissor.modulacoes import ASK, FSK, PSK, QAM16, QPSK
from util.portadora import Portadora
from util.ruido import Ruido
from util.sinal import Sinal

from .base import TransmissorBase

MODULADOCOES = {
    "ask": ASK,
    "fsk": FSK,
    "psk": PSK,
    "qpsk": QPSK,
    "16-qam": QAM16,
}


class Modulador(TransmissorBase):
    """Modula a onda portadora conforme sinal que se deseja transmitir."""

    def __init__(
        self,
        modulacao: str,
        largura_de_banda: float,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        debug=False,
    ):
        super().__init__()
        if modulacao.lower() not in MODULADOCOES:
            raise ValueError(f"Modulação '{modulacao}' não implementada.")
        self.modulador = MODULADOCOES[modulacao]
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

        amplitudes = np.ones_like(simbolos_decimais)
        frequencias = np.ones_like(simbolos_decimais)
        fases = np.zeros_like(simbolos_decimais)

        if self.modulacao == "ask":
            ask = self.modulador()
            amplitudes = ask.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "fsk":
            fsk = self.modulador()
            frequencias = fsk.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "psk":
            psk = self.modulador(self.bits_por_simbolo)
            fases = psk.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "qpsk":
            qpsk = self.modulador()
            fases = qpsk.gerar_parametros(simbolos_decimais)
        elif self.modulacao == "16-qam":
            qam16 = self.modulador()
            amplitudes, fases = qam16.gerar_parametros(simbolos_decimais)

        sinal_modulado = self.portadora.modular(amplitudes, frequencias, fases)

        if not self.debug:
            sinal_modulado += ruido.gerar_ruido(sinal_modulado)

        return sinal_modulado
