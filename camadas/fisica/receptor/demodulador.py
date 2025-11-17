from camadas.fisica.receptor.base import ReceptorBase
from camadas.fisica.transmissor.modulador import Modulador, MODULACOES

import numpy as np
import matplotlib.pyplot as plt

from util.sinal import Sinal


class Demodulador(ReceptorBase):
    def __init__(
        self,
        modulacao: str,
        frequencia_portadora: float,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        taxa_amostragem: int = 1000,
    ):
        super().__init__()
        if modulacao.lower() not in MODULACOES:
            raise ValueError(f"Modulação '{modulacao}' não implementada.")
        self.modulacao = modulacao.lower()
        self.frequencia_portadora = frequencia_portadora
        self.bits_por_simbolo = bits_por_simbolo
        self.tensao_pico = tensao_pico
        self.taxa_amostragem = taxa_amostragem
        self.dicionario_de_formas_de_onda = Modulador(
            modulacao=self.modulacao,
            frequencia_portadora=self.frequencia_portadora,
            bits_por_simbolo=self.bits_por_simbolo,
            tensao_pico=self.tensao_pico,
            taxa_amostragem=self.taxa_amostragem,
            debug=True,
        ).gerar_dicionario_de_formas_de_onda()

    def processar_sinal(self, bits: np.ndarray) -> np.ndarray:
        sinal = Sinal(self.bits_por_simbolo, self.taxa_amostragem)
        tempo_de_simbolo = 1 / self.frequencia_portadora
        amostras_por_simbolo = int(self.taxa_amostragem * tempo_de_simbolo)
        numero_de_simbolos = len(bits) // amostras_por_simbolo

        simbolos_demodulados = []

        for i in range(numero_de_simbolos):
            inicio = i * amostras_por_simbolo
            fim = inicio + amostras_por_simbolo
            segmento = bits[inicio:fim]

            menor_distancia = -np.inf
            simbolo_deteccao = None

            for simbolo, forma_onda in self.dicionario_de_formas_de_onda.items():
                distancia = np.abs(
                    np.sum((segmento - forma_onda) ** 2)
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
