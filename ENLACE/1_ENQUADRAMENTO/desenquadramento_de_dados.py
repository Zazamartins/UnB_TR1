"""
1/3 DESENQUADRAMENTO DE DADOS? ONDE COMEÇA ONDE TERMINA?
1. DES(Contagem de Caracteres)
2. DES(Byte Stuffing)
3. DES(Bit Stuffing)
"""

# -----------------------1. REMOVENDO CONTAGEM DE BYTES----------------------------------------------------
def desenquadramento_contagem_de_caracteres(quadro_recebido):
    """
    Lê o primeiro byte para saber o tamanho
    depois remover esse cabeçalho.
    """
    # Os primeiros 8 bits são o cabeçalho de tamanho
    cabecalho = quadro_recebido[0:8]
    
    # O resto é o dado
    dados = quadro_recebido[8:]
    
    return dados

# -----------------------2. DES(BYTE STUFFING)----------------------------------------------------
def desenquadramento_byte_stuffing(quadro_recebido):
    """
    2. Remove Byte Stuffing:
    Remove as flags das pontas. Percorre os dados: se achar um ESC,
    ignora ele e lê o próximo byte como dado puro.
    """
    FLAG = '01111110'
    ESC  = '01111101'
    
    # 1. Remove as Flags do início e do fim (8 bits cada)
    # Fatiamento: do caractere 8 até o último menos 8
    miolo = quadro_recebido[8 : -8]
    
    dados_limpos = ''
    
    i = 0
    while i < len(miolo):
        byte_atual = miolo[i : i+8]
        
        if byte_atual == ESC:
            # Um ESCAPE!
            # Significa que o PRÓXIMO byte é um dado real (mesmo que pareça flag/esc)
            # Então pulamos este ESC (i += 8) e pegamos o próximo
            i += 8
            proximo_byte = miolo[i : i+8]
            dados_limpos += proximo_byte
        else:
            # Byte normal, só guarda
            dados_limpos += byte_atual
            
        # Avança para o próximo bloco
        i += 8
        
    return dados_limpos

# -----------------------3. DES(BIT STUFFING)----------------------------------------------------
def desenquadramento_bit_stuffing(quadro_recebido):
    """
    Remove flags das pontas. Percorre bit a bit.
    Se achar 5 '1's seguidos, PULA o próximo bit (que deve ser '0').
    """
    FLAG = '01111110'
    
    # Remove as flags das pontas
    miolo = quadro_recebido[8 : -8]
    
    dados_limpos = ''
    contador_um = 0
    
    i = 0
    while i < len(miolo):
        bit = miolo[i]
        
        if bit == '1':
            contador_um += 1
            dados_limpos += '1'
            
            if contador_um == 5:
                # Se achamos 5 uns, o transmissor inseriu um '0' aqui.
                # Temos que PULAR esse '0' (não adicionar na saída).
                # Verificamos se o próximo é zero mesmo e pulamos o índice.
                if (i + 1) < len(miolo):
                    # Avança o índice extra para pular o '0' de stuffing
                    i += 1 
                
                contador_um = 0 # Reseta contagem
        else:
            contador_um = 0
            dados_limpos += '0'
            
        i += 1
        
    return dados_limpos