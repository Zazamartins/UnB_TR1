from camadas.fisica.receptor.base import ReceptorBase
import numpy as np

from camadas.fisica.transmissor.banda_base import CODIFICACOES, TransmissorBandaBase
from util.sinal import Sinal
import matplotlib.pyplot as plt


class Decodificador(ReceptorBase):
    def __init__(
        self,
        codificacao: str,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        taxa_amostragem: int = 1000,
    ):
        super().__init__()
        if codificacao.lower() not in CODIFICACOES:
            raise ValueError(f"Codificação '{codificacao}' não implementada.")
        self.codificacao = codificacao.lower()
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.taxa_amostragem = taxa_amostragem
        self.dicionario_de_formas_de_onda = TransmissorBandaBase(
            codificacao=self.codificacao,
            bits_por_simbolo=self.bits_por_simbolo,
            tensao_pico=self.tensao_pico,
            taxa_amostragem=self.taxa_amostragem,
            debug=True,
        ).gerar_dicionario_de_formas_de_onda()

    def processar_sinal(self, bits: np.ndarray) -> np.ndarray:
        bits = bits.flatten()
        
        sinal = Sinal(self.bits_por_simbolo, self.taxa_amostragem)
        tempo_de_simbolo = 1
        amostras_por_simbolo = int(self.taxa_amostragem * tempo_de_simbolo)
        numero_de_simbolos = len(bits) // amostras_por_simbolo
        tem_clock = self.codificacao == "manchester" or self.codificacao == "bipolar"

        simbolos_demodulados = []

        if self.codificacao == "bipolar":
            bits = np.abs(bits)

        for i in range(numero_de_simbolos):
            inicio = i * amostras_por_simbolo
            fim = inicio + amostras_por_simbolo
            if tem_clock:
                if i % 2 == 1:
                    continue
                    
                fim = inicio + amostras_por_simbolo * 2
                
            print(inicio, fim)


            segmento = bits[inicio:fim]

            menor_distancia = -np.inf
            simbolo_deteccao = None

            for simbolo, forma_onda in self.dicionario_de_formas_de_onda.items():              
                distancia = np.abs(
                    np.sum((segmento - forma_onda.flatten()) ** 2)
                )  # Distância Euclidiana
                if menor_distancia == -np.inf or distancia < menor_distancia:
                    menor_distancia = distancia
                    simbolo_deteccao = simbolo

            simbolos_demodulados.append(sinal.decimal_para_binario(simbolo_deteccao))

        if self.bits_por_simbolo > 1:
            simbolos_demodulados = np.array(simbolos_demodulados)
        else:
            simbolos_demodulados = np.array(simbolos_demodulados).flatten()

        return simbolos_demodulados
