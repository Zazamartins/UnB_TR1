"""
CRC-32 (IEEE 802).
Método: Divisão Polinomial usando Bitwise Shift e XOR.
"""

# Polinômio padrão IEEE 802: x^32 + x^26 + ... + 1
# Em Hex: 0x104C11DB7 (Representação binária de 33 bits)
POLINOMIO_HEX = 0x104C11DB7
GRAU_CRC = 32

def __executar_divisao_binaria(numero_alvo: int) -> int:
    """
    Realiza a 'divisão longa' binária usando XOR.
    Retorna apenas o RESTO da divisão (que é o CRC).
    """
    # Transforma nosso polinômio hex em inteiro manipulável
    divisor = POLINOMIO_HEX
    
    # O número alvo é a mensagem completa (já com os zeros ou crc anexado)
    dividendo = numero_alvo
    
    # Precisamos saber quantos bits tem o dividendo para alinhar o divisor
    # .bit_length() retorna a quantidade de bits necessários para representar o número
    num_bits = dividendo.bit_length()
    
    # Enquanto o dividendo for maior ou igual ao grau do polinômio (32)
    # continuamos a divisão.
    while num_bits >= (GRAU_CRC + 1):
        
        # Calculamos a diferença de tamanho para alinhar o divisor com o dividendo
        # Ex: Se dividendo tem 40 bits e divisor 33, shiftamos 7 vezes.
        shift_amount = num_bits - (GRAU_CRC + 1)
        
        # Alinha o divisor à esquerda
        divisor_alinhado = divisor << shift_amount
        
        # Aplica XOR (que equivale a subtração sem "empresta um" em GF(2))
        dividendo = dividendo ^ divisor_alinhado
        
        # Recalcula o tamanho do bit para a próxima iteração
        num_bits = dividendo.bit_length()
        
    # O que sobrar no 'dividendo' quando o loop acabar é o RESTO.
    return dividendo

def calcular_crc(bits_str: str) -> str:
    """
    1. Adiciona 32 zeros ao final da mensagem.
    2. Calcula o resto da divisão pelo polinômio.
    3. Retorna Mensagem Original + Resto (CRC).
    """
    # Converte string de bits para inteiro
    dados_int = int(bits_str, 2)
    
    # Passo 1: Shift Left de 32 posições (equivale a adicionar 32 zeros)
    dados_com_padding = dados_int << GRAU_CRC
    
    # Passo 2: Calcula o resto
    resto = __executar_divisao_binaria(dados_com_padding)
    
    # Formata o resto para garantir que tenha 32 caracteres (com zeros a esquerda)
    crc_formatado = format(resto, '032b')
    
    return bits_str + crc_formatado

def verificar_crc(quadro_completo: str) -> bool:
    """
    Recebe a mensagem já com o CRC no final.
    Realiza a divisão de tudo. Se o resto for 0, está íntegro.
    """
    # Verifica segurança básica
    if len(quadro_completo) < 32:
        return False
        
    dados_int = int(quadro_completo, 2)
    
    # Na matemática do CRC, se dividirmos (Mensagem + CRC) pelo Polinômio,
    # o resto OBRIGATORIAMENTE deve ser zero.
    resto_final = __executar_divisao_binaria(dados_int)
    
    # Verifica se o resto é zero
    return resto_final == 0

def remover_crc(quadro_completo: str) -> str:
    """
    Remove os últimos 32 bits para ler a mensagem original.
    """
    if len(quadro_completo) <= 32:
        return "" # Ou levantar erro, mas vamos retornar vazio por segurança
    
    # Fatia a string até os últimos 32 caracteres
    return quadro_completo[:-32]

"""
------------------EXEMPLO CRC-4 (polinômio de 4 bits) para MELHOR VISUALIZAR---------------------------
Dado: 110101
Polinômio: 1011

i = 1:

  110101  (Dado)
^ 101100  (Polinômio empurrado com << para alinhar)
--------
  011001  (Resultado do XOR)
  
Veja que o primeiro 1 virou 0 (1^1=0). O dado diminuiu! Agora é 11001.

i = 2:
  011001
^ 010110 (Polinômio empurrado)
--------
  001111 (Resultado)

O dado diminuiu de novo. Agora é 1111.

i = 3:

  001111
^ 001011
--------
  000100
  
Fim: O valor 100 (4 em binário) é menor que o polinômio 1011. O loop para. O CRC é 100.
"""