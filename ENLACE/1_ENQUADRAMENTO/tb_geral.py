import enquadramento_de_dados as transmissor
import desenquadramento_de_dados as receptor

# FUNÇÕES AUXILIARES DE VISUALIZAÇÃO (Para depurar melhor o códigoo)
def texto_para_bits(texto):
    """Converte string 'ABC' para string de bits '01000001...'"""
    bits = ''
    for char in texto:
        # Pega o código ASCII, vira binário de 8 digitos
        bits += format(ord(char), '08b') 
    return bits

def bits_para_texto(bits_string):
    """Converte string de bits de volta para texto legível"""
    chars = []
    # Anda de 8 em 8
    for i in range(0, len(bits_string), 8):
        byte = bits_string[i:i+8]
        if len(byte) == 8:
            codigo_ascii = int(byte, 2)
            chars.append(chr(codigo_ascii))
    return "".join(chars)

def imprimir_relatorio(titulo, msg_original, bits_transmitidos, bits_recebidos):
    print(f"\n{'='*70}")
    print(f" PROTOCOLO: {titulo}")
    print(f"{'='*70}")
    
    # 1. O que queríamos enviar
    print(f"1. [ORIGEM] Mensagem Texto:  '{msg_original}'")
    bits_originais = texto_para_bits(msg_original)
    print(f"   [ORIGEM] Em Bits:         {bits_originais}")

    # 2. O que passou pelo fio (com flags e stuffing)
    print(f"\n2. [REDE]   Pacote Trafegado: {bits_transmitidos}")
    print(f"   -> Note o aumento de tamanho devido ao cabeçalho/stuffing")

    # 3. O que chegou e foi limpo
    print(f"\n3. [DESTINO] Bits Limpos:    {bits_recebidos}")
    
    try:
        texto_final = bits_para_texto(bits_recebidos)
        print(f"   [DESTINO] Mensagem Final: '{texto_final}'")
        
        # Veredito
        if texto_final == msg_original:
            print("\n   >>> STATUS: SUCESSO TOTAL (Mensagem idêntica) <<<")
        else:
            print("\n   >>> STATUS: FALHA (Mensagens diferentes) <<<")
    except:
        print("\n   >>> STATUS: ERRO DE CONVERSÃO (Bits corrompidos?) <<<")


# -------------------------------TESTES------------------------------------------------------------------------

print("### INICIANDO SIMULAÇÃO COMPLETA DE ENLACE ###")

# -----------CENÁRIO 1: CONTAGEM DE CARACTERES----------------------
mensagem_1 = "Redes"
bits_input_1 = texto_para_bits(mensagem_1)

# Transmite
pacote_1 = transmissor.contagem_de_caracteres(bits_input_1)
# Recebe
limpo_1 = receptor.desenquadramento_contagem_de_caracteres(pacote_1)

imprimir_relatorio("Contagem de Caracteres", mensagem_1, pacote_1, limpo_1)


# -------------------CENÁRIO 2: BYTE STUFFING----------------------------------------
# '~' (til) é o caractere 126, que é EXATAMENTE a FLAG (01111110)
# A mensagem será: "1~2". O '~' no meio deve ser escapado.
mensagem_2 = "1~2" 
bits_input_2 = texto_para_bits(mensagem_2)

# Transmite
pacote_2 = transmissor.byte_stuffing(bits_input_2)
# Recebe
limpo_2 = receptor.desenquadramento_byte_stuffing(pacote_2)

imprimir_relatorio("Byte Stuffing (Inserção de Bytes)", mensagem_2, pacote_2, limpo_2)
print("   Obs: Veja no passo 2 (REDE) que a string de bits ficou bem maior")
print("        para acomodar o caractere de escape antes do '~'.")


# ----------------------CENÁRIO 3: BIT STUFFING--------------------------------
# Para testar isso visualmente, precisamos de uma sequencia de bits com muitos 1s.
# O caractere '?' em ASCII é 00111111. Dois '?' seguidos dão muitos 1s.
# Ou vamos forçar uma string binária manual para garantir 6 uns seguidos.
# Vamos simular envio de bits brutos (não texto) para ver o bit stuffing agir claramente.

print(f"\n{'='*70}")
print(f" PROTOCOLO: Bit Stuffing (Inserção de Bits)")
print(f"{'='*70}")

# Entrada manual: 111111 (6 uns). O sistema deve quebrar isso.
bits_manual = "111111" 
print(f"1. [ORIGEM] Bits Crus:       {bits_manual} (6 uns seguidos)")

# Transmite
pacote_3 = transmissor.bit_stuffing(bits_manual)
print(f"\n2. [REDE]   Pacote Trafegado: {pacote_3}")

# Vamos destacar onde o zero entrou.
# Pacote padrão: FLAG(01111110) + DADO(1111101) + FLAG(01111110)
miolo = pacote_3[8:-8]
print(f"   -> Análise do miolo:      {miolo}")
print("   -> Note o '0' inserido após o quinto '1'.")

# Recebe
limpo_3 = receptor.desenquadramento_bit_stuffing(pacote_3)
print(f"\n3. [DESTINO] Bits Limpos:    {limpo_3}")

if limpo_3 == bits_manual:
    print("\n   >>> STATUS: SUCESSO TOTAL (Bits restaurados) <<<")
else:
    print("\n   >>> STATUS: FALHA <<<")