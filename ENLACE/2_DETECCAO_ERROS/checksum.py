"""
Checksum parametrizado (padrão 16 bits).
"""

def _calcular_soma(bits_dados, n_bits):
    """
    Realiza a soma de complemento de 1 com blocos de tamanho 'n_bits'.
    """
    # Máscara dinâmica: se n=16, máscara é 0xFFFF. Se n=8, máscara é 0xFF.
    # (1 << n) - 1 cria uma sequência de n '1's.
    MASCARA = (1 << n_bits) - 1
    
    # Padding: Garante que a mensagem seja múltipla de n_bits
    resto = len(bits_dados) % n_bits
    if resto != 0:
        zeros_faltantes = n_bits - resto
        bits_dados = ('0' * zeros_faltantes) + bits_dados
        
    soma = 0
    
    # Loop com passo parametrizado
    for i in range(0, len(bits_dados), n_bits):
        # Pega bloco de tamanho n_bits
        bloco = bits_dados[i : i + n_bits]
        valor = int(bloco, 2)
        
        soma += valor
        
        # Lógica de Wraparound (Estouro) para qualquer tamanho de bits
        # Enquanto a soma for maior que o máximo permitido pela máscara...
        while soma > MASCARA:
            carry = soma >> n_bits  # Pega o bit que sobrou lá em cima
            resto = soma & MASCARA  # Pega a parte que cabe
            soma = resto + carry    # Soma o carry de volta
            
    return soma

def transmissor_checksum(mensagem_bits: str, n_bits: int = 16) -> str:
    """
    [TRANSMISSOR]
    1. Calcula a soma dos blocos da mensagem.
    2. Faz o complemento (inverte).
    3. Retorna: Mensagem Original + Checksum calculado.
    """
    # Calcula a soma bruta
    soma_total = _calcular_soma(mensagem_bits, n_bits)
    
    # Máscara para garantir o tamanho correto na inversão
    MASCARA = (1 << n_bits) - 1
    
    # Inverte os bits (Complemento de 1)
    checksum_val = (~soma_total) & MASCARA
    
    # Formata para string binária com o tamanho solicitado
    # f'0{n_bits}b' cria uma string de formatação dinâmica, ex: '016b'
    checksum_str = format(checksum_val, f'0{n_bits}b')
    
    return mensagem_bits + checksum_str

def receptor_checksum(pacote_recebido: str, n_bits: int = 16) -> bool:
    """
    [RECEPTOR]
    1. Recebe o pacote (Dados + Checksum).
    2. Soma tudo (incluindo o checksum).
    3. Se a soma invertida der 0, está válido.
    """
    # Verificação básica de tamanho
    if len(pacote_recebido) < n_bits:
        return False
        
    soma_final = _calcular_soma(pacote_recebido, n_bits)
    MASCARA = (1 << n_bits) - 1
    
    # Verifica se o inverso é zero (ou seja, se a soma deu tudo 1)
    validacao = (~soma_final) & MASCARA
    
    return validacao == 0

def limpar_dados(pacote_recebido: str, n_bits: int = 16) -> str:
    """
    Remove os últimos 'n_bits' (que são o checksum) para ler a mensagem.
    """
    if len(pacote_recebido) <= n_bits:
        return ""
    return pacote_recebido[:-n_bits]