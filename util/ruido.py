import numpy as np

class Ruido:
    def __init__(self, sigma: float = 0.1):
        self.sigma = sigma

    def gerar_ruido(self, sinal: np.ndarray) -> np.ndarray:
        """Gera ruído gaussiano com média 0 e desvio padrão sigma na forma de um array numpy com o mesmo formato do sinal de entrada."""
        ruido = np.random.normal(0, self.sigma, sinal.shape)
        return ruido