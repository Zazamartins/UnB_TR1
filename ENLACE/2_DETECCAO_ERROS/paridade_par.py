"""
Lógica: Utiliza o operador XOR (^) para calcular se a quantidade de 1s é par ou ímpar.
Regra do XOR: Ele funciona como um acumulador. Se o resultado final for 1, temos número ímpar de 1s.
"""

def calcular_paridade(bits_entrada: str) -> str:
    """
    Percorre a string fazendo XOR de cada bit.
    Adiciona o resultado (0 ou 1) ao final da string.
    """
    acumulador_xor = 0
    
    for bit in bits_entrada:
        # Converte o caractere '0' ou '1' para inteiro e faz o XOR
        valor_bit = int(bit)
        acumulador_xor = acumulador_xor ^ valor_bit
        
    # Converte o resultado (0 ou 1) para string e anexa ao final
    return bits_entrada + str(acumulador_xor)

def verificar_erro(quadro_recebido: str) -> bool:
    """
    Refaz o XOR de TODOS os bits (dados + bit de paridade).
    Matemática: Se a paridade estiver correta, o XOR de tudo DEVE ser 0.
    """
    calculo = 0
    
    for bit in quadro_recebido:
        calculo = calculo ^ int(bit)
        
    # Se calculo for 0, é True (Sem erro). Se for 1, é False (Tem erro).
    return calculo == 0

def limpar_dados(quadro_recebido: str) -> str:
    """
    Remove o último bit (bit de redundância) para recuperar o dado original.
    """
    return quadro_recebido[:-1]