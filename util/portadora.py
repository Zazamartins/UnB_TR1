import numpy as np


class Portadora:
    def __init__(
        self,
        amplitude: float,
        frequencia: float,
        fase: float,
        tempo_de_simbolo: float = 1.0,
        taxa_amostragem: int = 1000,
    ):
        self.amplitude = amplitude
        self.frequencia = frequencia
        self.fase = fase
        self.tempo_de_simbolo = tempo_de_simbolo
        self.taxa_amostragem = taxa_amostragem

    def modular(
        self, amplitudes: np.ndarray, frequencias: np.ndarray, fases: np.ndarray
    ) -> np.ndarray:
        """Modula a portadora conforme os parâmetros fornecidos.
        Amplitudes - array com as amplitudes de 0 a 1 para cada símbolo.
        Frequencias - array com as frequências de 1 a 2 para cada símbolo.
        Fases - array com as fases de 0 a 180 graus para cada símbolo.
        Retorna o sinal modulado.
        """
        numero_de_simbolos = len(amplitudes)
        tempo_por_simbolo = np.linspace(
            0,
            self.tempo_de_simbolo,
            int(self.tempo_de_simbolo * self.taxa_amostragem),
            endpoint=False,
        )

        sinal_modulado = np.array([])
        for i in range(numero_de_simbolos):
            amp = amplitudes[i]
            freq = frequencias[i]
            fase = fases[i]

            # Amplitude varia entre 0 e a amplitude da portadora
            amplitude = amp * self.amplitude

            # Frequência varia entre f e 2fG
            frequencia = freq * self.frequencia

            # Fase varia entre 0 e 180 graus
            fase = np.deg2rad(fase + self.fase)

            ciclo = amplitude * np.sin(2 * np.pi * frequencia * tempo_por_simbolo + fase)

            sinal_modulado = np.concatenate((sinal_modulado, ciclo))

        return sinal_modulado

    def gerar_portadora(self, tempo: np.ndarray) -> np.ndarray:
        """Gera o sinal da portadora no tempo informado."""
        return self.amplitude * np.sin(2 * np.pi * self.frequencia * tempo + self.fase)

    def gerar_portadora_para_mensagem(self, mensagem: np.ndarray) -> np.ndarray:
        """Gera um ciclo de onda por símbolo da mensagem."""
        duracao_simbolo = 1 / self.frequencia

        if mensagem.ndim > 1:
            numero_de_simbolos = mensagem.shape[0]
        else:
            numero_de_simbolos = len(mensagem)

        tempo_total = duracao_simbolo * numero_de_simbolos
        tempo = np.linspace(0, tempo_total, int(tempo_total * self.taxa_amostragem))

        sinal_portadora = self.gerar_portadora(tempo)

        return sinal_portadora
