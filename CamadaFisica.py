from abc import ABC, abstractmethod

from scipy.integrate import quad
import numpy as np

# ===================================================
# =-=-=-=-=-=-=-=-=-= UTILITÁRIAS =-=-=-=-=-=-=-=-=-=
# ===================================================

class Ruido:
    def __init__(self, sigma: float = 0.1):
        self.sigma = sigma

    def gerar_ruido(self, sinal: np.ndarray) -> np.ndarray:
        """Gera ruído gaussiano com média 0 e desvio padrão sigma na forma de um array numpy com o mesmo formato do sinal de entrada."""
        ruido = np.random.normal(0, self.sigma, sinal.shape)
        return ruido

class Sinal:
    """Classe que converte uma mensagem de texto em um sinal digital."""

    def __init__(self, bits_por_simbolo: int = 1, taxa_amostragem: int = 1000):
        self._bits_por_simbolo = bits_por_simbolo
        self._taxa_amostragem = taxa_amostragem

    @property
    def bits_por_simbolo(self) -> int:
        return self._bits_por_simbolo

    @property
    def taxa_amostragem(self) -> int:
        return self._taxa_amostragem

    @bits_por_simbolo.setter
    def bits_por_simbolo(self, valor: int):
        self._bits_por_simbolo = valor

    @staticmethod
    def gerar_sinal_binario(mensagem: str) -> np.ndarray:
        """Converte a mensagem em uma sequência de bits."""
        bits = "".join(format(ord(c), "08b") for c in mensagem)
        bits = np.array([int(b) for b in bits])
        return bits

    def gerar_pulso_tensao_ideal(
        self, simbolos_decimais: np.ndarray, tempo_de_simbolo: float = 1.0
    ) -> np.ndarray:
        """
        Gera uma curva de tensão ideal simulando um pulso elétrico.
        """
        sinal = []
        for simbolo in simbolos_decimais:
            sinal.append(np.full(int(tempo_de_simbolo * self.taxa_amostragem), simbolo))

        return np.array(sinal)

    def gerar_pulso_tensao(
        self,
        simbolos_decimais: np.ndarray,
        tempo_de_simbolo: float = 1.0,
        simbolos_por_periodo: int = 4,
    ) -> np.ndarray:
        """
        Gera uma curva de tensão simulando um pulso elétrico utilizando série de Fourier
        simbolos_decimais é um array com os símbolos em decimal -> [simbolo1, simbolo2, simbolo3, ...].
        Devolve um array numpy com a forma de onda de cada símbolo -> [[forma_de_onda1], [forma_de_onda2], [forma_de_onda3], ...].
        """

        if self.bits_por_simbolo == 1:
            simbolos_decimais = np.reshape(
                simbolos_decimais, (-1, 1)
            )  # trata cada bit como um símbolo

        # Dado que a série de fourier considera a função aproximada como sendo periódica,
        # faz sentido definir quantos símbolos serão representados até que seja considerado
        # que um período foi percorrido. Isso melhora o resultado para sequências muito extensas
        # de símbolos.
        segmentos = np.array_split(
            simbolos_decimais, max(1, len(simbolos_decimais) // simbolos_por_periodo)
        )
        forma_de_onda = np.concatenate(
            [
                self.__serie_de_fourier(
                    segmento, tempo_de_simbolo=tempo_de_simbolo, harmonicas=8
                )
                for segmento in segmentos
            ]
        )

        return forma_de_onda

    def sequencia_de_bits_para_simbolos(
        self, bits: np.ndarray
    ) -> np.ndarray:  # TODO testar
        """Agrupa a sequência de bits em símbolos de acordo com bits_por_simbolo."""
        if self.bits_por_simbolo == 1:
            return bits

        num_simbolos = len(bits) // self.bits_por_simbolo
        bits = bits[: num_simbolos * self.bits_por_simbolo]
        simbolos = bits.reshape((num_simbolos, self.bits_por_simbolo))

        return simbolos

    def binario_para_decimal(self, bits: np.ndarray) -> np.ndarray:
        """Converte uma sequência de símbolos em uma sequência de seus respectivos decimais, normalizados (de 0 a 1)."""
        sinal = []
        passo_de_tensao = 1 / (2**self.bits_por_simbolo - 1)

        if self.bits_por_simbolo > 1:
            bits = bits.reshape((-1, self.bits_por_simbolo))
            for simbolo in bits:
                valor_simbolo = 0
                for i, bit in enumerate(simbolo):
                    valor_simbolo += bit * (2 ** (self.bits_por_simbolo - i - 1))
                nivel_tensao = valor_simbolo * passo_de_tensao
                sinal.append(nivel_tensao)
        else:
            for bit in bits:
                nivel_tensao = bit * passo_de_tensao
                sinal.append(nivel_tensao)

        return np.array(sinal)

    def decimal_para_binario(self, decimal: int) -> np.ndarray:
        """Converte um número decimal em sua representação binária com bits_por_simbolo bits."""
        formato = "{0:0" + str(self.bits_por_simbolo) + "b}"
        binario_str = formato.format(decimal)
        binario = np.array([int(bit) for bit in binario_str])
        return binario

    def __serie_de_fourier(
        self, simbolos: np.ndarray, tempo_de_simbolo: float, harmonicas: int
    ) -> np.ndarray:
        """Gera uma série de Fourier."""
        periodo = len(simbolos) * tempo_de_simbolo
        t = np.linspace(0, periodo, int(periodo * self.taxa_amostragem), endpoint=False)
        c = 2 / periodo * np.sum(simbolos)

        resultado = np.zeros_like(t) + c / 2

        for n in range(1, harmonicas + 1):
            y_an = lambda t: simbolos[int(t // tempo_de_simbolo)] * np.sin(
                2 * np.pi * n * t / periodo
            )
            y_bn = lambda t: simbolos[int(t // tempo_de_simbolo)] * np.cos(
                2 * np.pi * n * t / periodo
            )

            an = (
                np.sin(2 * np.pi * n * t / periodo)
                * (2.0 / periodo)
                * np.array(quad(y_an, 0, periodo))[0]  # descarta o valor do erro
            )
            bn = (
                np.cos(2 * np.pi * n * t / periodo)
                * (2.0 / periodo)
                * np.array(quad(y_bn, 0, periodo))[0]  # descarta o valor do erro
            )

            resultado += an + bn

        return np.reshape(resultado, (len(simbolos), -1))

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
   
class Gray:

    def __init__(
        self,
        bits_por_simbolo: int,
        normalizado: bool = False,
        flag_binario: bool = False,
    ):
        self.bits_por_simbolo = bits_por_simbolo
        self.normalizado = normalizado
        self.flag_binario = flag_binario
        self._tabela_gray = self._gerar_tabela_gray()

    @property
    def tabela_gray(self) -> np.ndarray:
        return self._tabela_gray

    def _gerar_tabela_gray(self) -> np.ndarray:
        """
        Gera a tabela de códigos Gray para o número de bits por símbolo.
        Referência: https://stackoverflow.com/questions/38738835/generating-gray-codes-recursively-without-initialising-the-base-case-outside-of
        """
        num_simbolos = 2**self.bits_por_simbolo
        tabela = []

        for i in range(num_simbolos):
            gray_code = i ^ (i >> 1)
            if self.flag_binario:
                binario = format(gray_code, f"0{self.bits_por_simbolo}b")
                gray_code = [int(bit) for bit in binario]
            tabela.append(gray_code)

        tabela = np.array(tabela)

        if self.normalizado:
            tabela = tabela / (num_simbolos - 1)

        return tabela

# ====================================================
# =-=-=-=-=-=-=-=-=-= CODIFICAÇÕES =-=-=-=-=-=-=-=-=-=
# ====================================================

class CodificacaoBase(ABC):
    @abstractmethod
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        """Retorna as palavras de bits codificadas."""
        pass

class Bipolar(CodificacaoBase):
    """Codificação Bipolar ou AMI:
    Se clock é baixo, transmite 0. Do contrário:
    - Se bits 1, transmite pulsos positivos e negativos alternados. Se bit 0, transmite 0.
    """

    def __init__(self):
        self._ultimo_sinal = 1.0  # alterna +1/-1 para bits 1

    def codificar(self, bits: np.ndarray) -> np.ndarray:
        # Diferente de 0 somente quando clock é alto
        self._ultimo_sinal = 1.0
        clock = self.__clock(bits)
        saida = []

        for i, clk in enumerate(clock):
            # Cada símbolo dura um ciclo de clock (rising + falling edges)
            i_mensagem = i // 2
            simbolo = bits[i_mensagem]
            mais_de_um_bit_por_simbolo = (
                simbolo.ndim > 0 if i_mensagem < len(bits) else False
            )

            # Quando clock é alto, transmite 1 ou -1 de forma alternada
            if clk == 1.0:
                if mais_de_um_bit_por_simbolo and simbolo.any():
                    simbolo_saida = simbolo * self._ultimo_sinal
                    self._ultimo_sinal *= -1.0

                    saida.append(simbolo_saida)
                elif mais_de_um_bit_por_simbolo:
                    saida.append([0.0] * len(simbolo))
                else:
                    if simbolo == 1:
                        saida.append(self._ultimo_sinal)
                        self._ultimo_sinal *= -1.0
                    else:
                        saida.append(0.0)
            # Quando clock é baixo, transmite 0
            else:
                if mais_de_um_bit_por_simbolo:
                    saida.append([0.0] * len(simbolo))
                else:
                    saida.append(0.0)

        return np.array(saida)

    def __clock(self, bits: np.ndarray) -> np.ndarray:
        clock = np.zeros(len(bits) * 2)

        for i in range(len(clock)):
            if i % 2 == 0:
                clock[i] = 1.0
            else:
                clock[i] = 0.0

        return clock

class Manchester(CodificacaoBase):
    """ Codificação Manchester: 
        Faz uma operação XOR entre os bits da mensagem e o clock.
    """
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        clock = self.__clock(bits)
        saida = []
        for i, clk in enumerate(clock):
            i_mensagem = i // 2 

            mais_de_um_bit_por_simbolo = (
                bits[i_mensagem].ndim > 0 if i_mensagem < len(bits) else False
            )

            if clk == 1.0: # XOR com 1 === inverte bits
                if mais_de_um_bit_por_simbolo:
                    simbolo_saida = []
                    for b in bits[i_mensagem]:
                        if b == 1:
                            simbolo_saida.append(0.0)
                        else:
                            simbolo_saida.append(1.0)
                    saida.append(simbolo_saida)
                else:
                    if bits[i_mensagem] == 1:
                        saida.append(0.0)
                    else:
                        saida.append(1.0)
            else: # XOR com 0 === mantém bits
                if mais_de_um_bit_por_simbolo:
                    simbolo_saida = []
                    for b in bits[i_mensagem]:
                        if b == 1:
                            simbolo_saida.append(1.0)
                        else:
                            simbolo_saida.append(0.0)
                    saida.append(simbolo_saida)
                else:
                    if bits[i_mensagem] == 1:
                        saida.append(1.0)
                    else:
                        saida.append(0.0)
                

        return np.array(saida)
    
    def __clock(self, bits: np.ndarray) -> np.ndarray:
        clock = np.zeros(len(bits) * 2)

        for i in range(len(clock)):
            if i % 2 == 0:
                clock[i] = 1.0
            else:
                clock[i] = 0.0
        return clock
            
class NRZPolar(CodificacaoBase):
    """ Codificação NRZ Polar: 
        Bits 1 são representados por +1 e bits 0 por -1.
    """
    def codificar(self, bits: np.ndarray) -> np.ndarray:
        saida = []
        for simbolo in bits:
            if simbolo.ndim > 0:
                simbolo_saida = []
                for b in simbolo:
                    if b == 1:
                        simbolo_saida.append(1.0)
                    else:
                        simbolo_saida.append(-1.0)

                saida.append(simbolo_saida)
            else:
                if simbolo == 1:
                    saida.append(1.0)
                else:
                    saida.append(-1.0)
            
        return np.array(saida)    

CODIFICACOES = {
    "manchester": Manchester,
    "nrz_polar": NRZPolar,
    "bipolar": Bipolar,
}

# ==================================================
# =-=-=-=-=-=-=-=-=-= MODULAÇÕES =-=-=-=-=-=-=-=-=-=
# ==================================================

class ModulacaoBase(ABC):
    @abstractmethod
    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Retorna, para cada símbolo, o valor do parâmetro utilizado na modulação da portadora."""
        pass

class ASK(ModulacaoBase):
    def __init__(self):
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação ASK (Amplitude Shift Keying).
        A amplitude da portadora pode variar entre 0 e 1
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as amplitudes correspondentes a cada símbolo.
        """
        parametros = []

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            amplitude = simbolo
            parametros.append(amplitude)

        return np.array(parametros)

class FSK(ModulacaoBase):
    def __init__(self):
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação FSK (Frequency Shift Keying).
        A frequência da portadora pode variar entre a frequencia da portadora e 2 vezes essa frequência,
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com o multiplicador de frequência correspondentes a cada símbolo.
        """
        parametros = []

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            parametros.append(1 + simbolo)

        return np.array(parametros)
     
class PSK(ModulacaoBase):
    def __init__(self, bits_por_simbolo: int = 1):
        self.bits_por_simbolo = bits_por_simbolo
        super().__init__()

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação PSK (Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 graus a 360 graus
        em intervalos atrelados ao número de bits por símbolo.
        Retorna um array com as fases (em graus) correspondentes a cada símbolo.
        """
        gray = Gray(
            bits_por_simbolo=self.bits_por_simbolo, normalizado=True
        )  # Codigo Gray com valores de 0 a 1
        tabela_gray = gray.tabela_gray
        parametros = []
        num_fases = 2**self.bits_por_simbolo

        # Nota: simbolos_decimais já apresenta valores de 0 a 1
        for simbolo in simbolos_decimais:
            indice = np.where(tabela_gray == simbolo)[0][0]
            fase = indice * (360 / num_fases)
            parametros.append(fase)

        return np.array(parametros)
     
class QPSK(ModulacaoBase):
    def __init__(self):
        super().__init__()
        self.psk = PSK(bits_por_simbolo=2)  # QPSK usa 2 bits por símbolo

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação QPSK (Quadrature Phase Shift Keying).
        A fase da portadora pode ser defasada de 0 a 360 graus
        em intervalos atrelados ao número de bits por símbolo (2 bits por símbolo para QPSK).
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        return self.psk.gerar_parametros(simbolos_decimais)
     
class QAM16(ModulacaoBase):
    def __init__(self):
        super().__init__()

        self._gray_16qam_decimal = np.array(
            [
                [7, 5, 13, 15],  # [0, 1, 1, 1], [0, 1, 0, 1], [1,1,0,1], [1,1,1,1]
                [6, 4, 12, 14],  # [0, 1, 1, 0], [0, 1, 0, 0], [1,1,0,0], [1,1,1,0]
                [2, 0, 8, 10],  # [0, 0, 1, 0], [0, 0, 0, 0], [1,0,0,0], [1,0,1,0]
                [3, 1, 9, 11],  # [0, 0, 1, 1], [0, 0, 0, 1], [1,0,0,1], [1,0,1,1]
            ]
        ) / (2**4 - 1)  # Normalizado entre 0 e 1

    @property
    def tabela_gray(self) -> np.ndarray:
        """Retorna a tabela Gray utilizada na modulação 16QAM."""
        return self._gray_16qam_decimal

    def gerar_parametros(self, simbolos_decimais: np.ndarray) -> np.ndarray:
        """Modulação 16QAM (Quadrature Amplitude Modulation).
        A fase da portadora pode ser defasada de 0 a 360 graus
        em intervalos atrelados ao número de bits por símbolo (2 bits por símbolo para QPSK).
        Retorna um array com as fases correspondentes a cada símbolo.
        """
        amplitudes = np.zeros_like(simbolos_decimais, dtype=float)
        fases = np.zeros_like(simbolos_decimais, dtype=float)

        # Q > 0 === X1XX
        # Q < 0 === X0XX
        # I > 0 === 1XXX
        # I < 0 === 0XXX
        # I = 1/(3*sqrt(2)) === XX0X
        # I = 1/sqrt(2) === XX1X
        # Q = 1/(3*sqrt(2)) === XXX0
        # Q = 1/sqrt(2) === XXX1
        # 45deg === XX00 e XX11
        # 75deg === XX01
        # 15deg === XX10
        for i, simbolo in enumerate(simbolos_decimais):
            linha, coluna = np.where(self._gray_16qam_decimal == simbolo)
            linha = linha[0]
            coluna = coluna[0]

            # Determina componente I
            if coluna in [0, 1]:  # I < 0 (Quadrantes 2 e 3)
                componente_i = -1 / (3 * np.sqrt(2))
            else:  # I > 0
                componente_i = 1 / (3 * np.sqrt(2))

            if coluna in [1, 2]:  # I = 1/3sqrt(2)
                componente_i *= 1
            else:  # I = 1/sqrt(2)
                componente_i *= 3

            # Determina componente Q
            if linha in [0, 1]:  # Q > 0 (Quadrantes 1 e 2)
                componente_q = 1 / (3 * np.sqrt(2))
            else:  # Q < 0
                componente_q = -1 / (3 * np.sqrt(2))
            if linha in [1, 2]:  # Q = 1/3sqrt(2)
                componente_q *= 1
            else:  # Q = 1/sqrt(2)
                componente_q *= 3

            amplitude = np.sqrt(componente_i**2 + componente_q**2)
            fase = np.degrees(np.arctan2(componente_q, componente_i)) % 360
            amplitudes[i] = amplitude
            fases[i] = fase

        return amplitudes, fases

MODULACOES = {
    "ask": ASK,
    "fsk": FSK,
    "psk": PSK,
    "qpsk": QPSK,
    "16-qam": QAM16,
}

# ===================================================
# =-=-=-=-=-=-=-=-=-= TRANSMISSOR =-=-=-=-=-=-=-=-=-=
# ===================================================

class TransmissorBase(ABC):
    @abstractmethod
    def processar_sinal(self, mensagem: str) -> np.ndarray:
        """Processa a mensagem de entrada e retorna o sinal modulado"""
        pass

    def gerar_dicionario_de_formas_de_onda(self) -> dict[int, np.ndarray]:
        """Gera um dicionário com as formas de onda de cada símbolo possível."""
        debug_backup = self.debug
        self.debug = True  # Ativa o modo debug para evitar ruído
        sinal = Sinal(self.bits_por_simbolo, self.taxa_amostragem)
        num_simbolos = 2**self.bits_por_simbolo
        simbolos = np.arange(num_simbolos)
        dicionario: dict[int, np.ndarray] = {}

        for simbolo in simbolos:
            bits = sinal.decimal_para_binario(simbolo)
            sinal_eletrico = self.processar_sinal(bits)
            dicionario[simbolo] = sinal_eletrico

        self.debug = debug_backup  # Restaura o modo debug anterior

        return dicionario

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
        bits = bits.flatten()
        # Converte a mensagem em uma sequência de bits
        sinal = Sinal(self.bits_por_simbolo, taxa_amostragem=self.taxa_amostragem)
        ruido = Ruido()
        bits = sinal.sequencia_de_bits_para_simbolos(bits)

        # Codifica os bits usando o esquema de codificação selecionado
        sinal_codificado = self.codificador.codificar(bits)

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

class Modulador(TransmissorBase):
    """Modula a onda portadora conforme sinal que se deseja transmitir."""

    def __init__(
        self,
        modulacao: str,
        frequencia_portadora: float,
        bits_por_simbolo: int = 1,
        tensao_pico: float = 3.3,
        taxa_amostragem: int = 1000,
        debug: bool = False,
    ):
        super().__init__()
        if modulacao.lower() not in MODULACOES:
            raise ValueError(f"Modulação '{modulacao}' não implementada.")
        self.modulador = MODULACOES[modulacao]
        self.bits_por_simbolo = bits_por_simbolo
        self.modulacao = modulacao
        self.portadora = Portadora(
            amplitude=tensao_pico,
            frequencia=frequencia_portadora,
            fase=0,
            tempo_de_simbolo=1 / frequencia_portadora,
            taxa_amostragem=taxa_amostragem,
        )
        self.debug = (
            debug  # Flag para printar sinal intermediário e pular adição de ruído
        )

    @property
    def taxa_amostragem(self) -> int:
        return self.portadora.taxa_amostragem

    def processar_sinal(self, bits: np.ndarray) -> np.ndarray:
        sinal = Sinal(self.bits_por_simbolo, self.taxa_amostragem)
        ruido = Ruido()
        bits = sinal.sequencia_de_bits_para_simbolos(bits)

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

# ====================================================
# =-=-=-=-=-=-=-=-=-=-= RECEPTOR =-=-=-=-=-=-=-=-=-=-=
# ====================================================

class ReceptorBase(ABC):
    @abstractmethod
    def processar_sinal(self, sinal: np.ndarray) -> str:
        """Processa o sinal recebido e retorna a mensagem decodificada"""
        pass

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
