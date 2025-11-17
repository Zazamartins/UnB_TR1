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
        frequencia_de_simbolo: float = 1.0,
        tensao_pico: float = 3.3,
        taxa_amostragem: int = 1000,
        debug: bool = False,
    ):
        super().__init__()
        if codificacao.lower() not in CODIFICACOES:
            raise ValueError(f"Codificação '{codificacao}' não implementada.")
        self.codificador = CODIFICACOES[codificacao]()
        self.bits_por_simbolo = bits_por_simbolo
        self.frequencia_de_simbolo = frequencia_de_simbolo
        self.tensao_pico = tensao_pico
        self.taxa_amostragem = taxa_amostragem
        self.debug = (
            debug  # Flag para printar sinal intermediário e pular adição de ruído
        )

    def processar_sinal(self, bits: np.ndarray) -> np.ndarray:
        # Converte a mensagem em uma sequência de bits
        sinal = Sinal(self.bits_por_simbolo, taxa_amostragem=self.taxa_amostragem)
        ruido = Ruido()
        bits = sinal.sequencia_de_bits_para_simbolos(bits)

        # Codifica os bits usando o esquema de codificação selecionado
        sinal_codificado = self.codificador.codificar(bits)

        if self.debug:
            print("DEBUG: ", sinal_codificado)

        # Aplica valor decimal de cada símbolo
        sinal_codificado = sinal.binario_para_decimal(sinal_codificado)

        sinal_codificado *= (
            self.tensao_pico
        )  # Ajusta o nível de tensão do sinal codificado

        if not self.debug:
            sinal_codificado = sinal.gerar_pulso_tensao(
                sinal_codificado,
                tempo_de_simbolo=1/self.frequencia_de_simbolo
            )
        else:
            sinal_codificado = sinal.gerar_pulso_tensao_ideal(
                sinal_codificado,
                tempo_de_simbolo=1/self.frequencia_de_simbolo
            )

        if not self.debug:
            sinal_codificado += ruido.gerar_ruido(
                sinal_codificado
            )  # Adiciona ruído ao sinal codificado

        return sinal_codificado
