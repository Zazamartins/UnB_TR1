import numpy as np

from util.ruido import Ruido
from util.sinal import Sinal

from .base import TransmissorBase
from .codificacoes.bipolar import Bipolar
from .codificacoes.manchester import Manchester
from .codificacoes.nrz_polar import NRZPolar

CODIFICACOES = {
    "manchester": Manchester,
    "nrz_polar": NRZPolar,
    "bipolar": Bipolar,
}


class TransmissorBandaBase(TransmissorBase):
    def __init__(
        self,
        codificacao: str,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        debug=False,
    ):
        super().__init__()
        if codificacao.lower() not in CODIFICACOES:
            raise ValueError(f"Codificação '{codificacao}' não implementada.")
        self.codificador = CODIFICACOES[codificacao]()
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.debug = (
            debug  # Flag para printar sinal intermediário e pular adição de ruído
        )

    def processar_sinal(self, mensagem: str) -> np.ndarray:
        # Converte a mensagem em uma sequência de bits
        sinal = Sinal(self.bits_por_simbolo)
        ruido = Ruido()
        bits = sinal.gerar_sinal_binario(mensagem)

        # Codifica os bits usando o esquema de codificação selecionado
        sinal_codificado = self.codificador.codificar(bits)

        if self.debug:
            print("DEBUG: ", sinal_codificado)

        # Aplica valor decimal de cada símbolo
        sinal_codificado = sinal.binario_para_decimal(sinal_codificado)

        if not self.debug:
            sinal_codificado = sinal.gerar_pulso_tensao(sinal_codificado)

        sinal_codificado *= (
            self.tensao_pico
        )  # Ajusta o nível de tensão do sinal codificado

        if not self.debug:
            sinal_codificado += ruido.gerar_ruido(
                sinal_codificado
            )  # Adiciona ruído ao sinal codificado

        return sinal_codificado
