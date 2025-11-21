"""
1/3 ENQUADRAMENTO DE DADOS? ONDE COMEÇA ONDE TERMINA?
1. Contagem de Caracteres
2. Byte Stuffing
3. Bit Stuffing
"""

# -----------------------1. CONTAGEM DE CARACTERES/BYTES----------------------------------------------------
def contagem_de_caracteres(quadro):
    """
    1. Contagem de Caracteres:
    Conta quantos bytes (grupos de 8 bits) existem e coloca esse número
    em binário no começo.
    """
    # Calcula quantos bytes tem no quadro (tamanho total dividido por 8)
    quantidade_bytes = len(quadro) // 8
    
    # Transforma esse número em uma string de 8 bits (ex: 4 vira '00000100')
    cabecalho = format(quantidade_bytes, '08b')
    
    # Retorna o cabeçalho colado com o quadro original
    return cabecalho + quadro


# -----------------------2. BYTE STUFFING----------------------------------------------------
def byte_stuffing(quadro):
    """
    Verifica byte a byte. Se encontrar a FLAG ou o ESCAPE no meio dos dados,
    insere um ESCAPE antes para avisar. 
    Lembre do caractere especial no LATEX '\' 
    """
    # FLAG e SCAPE
    FLAG = '01111110'  # Representa o começo/fim
    ESC  = '01111101'  # Representa o caractere de escape
    
    quadro_saida = ''
    
    # Percorre o quadro original de 8 em 8 bits (um byte por vez)
    i = 0
    while i < len(quadro):
        # Pega um pedaço de 8 bits/1 Byte
        byte_atual = quadro[i : i+8]
        
        # Verifica se esse pedaço é igual a FLAG ou ESC
        if byte_atual == FLAG or byte_atual == ESC:
            # Se for igual, adicionamos o ESC antes de adicionar o dado
            quadro_saida += ESC
            quadro_saida += byte_atual
        else:
            # Se for um byte normal, só adiciona
            quadro_saida += byte_atual
            
        # Avança para o próximo grupo de 8 bits/byte
        i += 8
        
    # Retorna: FLAG + QUADRO_STUFFING + FLAG
    return FLAG + quadro_saida + FLAG


# -----------------------3. BIT STUFFING----------------------------------------------------
def bit_stuffing(quadro):
    """
    Percorre bit a bit. Se contar 5 '1's seguidos, insere um '0' à força.
    """
    FLAG = '01111110'
    
    quadro_saida = ''
    contador_um = 0
    
    # Analisa cada bit individualmente (0 ou 1)
    for bit in quadro:
        if bit == '1':
            contador_um += 1
            quadro_saida += '1'
            
            # REGRA DO BIT STUFFING: Se tiver 5 uns seguidos, insere um 0
            if contador_um == 5:
                quadro_saida += '0'
                contador_um = 0 # Zera contagem pois quebramos a sequência
        else:
            # Se é zero, zera a contagem de uns
            contador_um = 0
            quadro_saida += '0'
            
    # Retorna o quadro cercado pelas flags
    return FLAG + quadro_saida + FLAG