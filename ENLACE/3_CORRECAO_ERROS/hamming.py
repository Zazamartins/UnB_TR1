"""
Código de Hamming (7,4) e genéricos.
Capacidade: Detecta e CORRIGE erro de 1 bit.
"""

def _eh_potencia_de_2(n):
    """
    Verifica se um número é potência de 2 (1, 2, 4, 8...)
    Usamos bitwise: (n & n-1) == 0 TRUQUE DE HARWARE
    Ex: 4 (100) e 3 (011) -> 100 & 011 = 000.
    """
    return n > 0 and (n & (n - 1)) == 0

def codificar_hamming(dados_bits: str) -> str:
    """
    Recebe bits de dados (ex: '1001') e retorna o quadro Hamming completo.
    """
    # 1. Descobrir quantos bits de paridade (r) precisamos
    m = len(dados_bits)
    r = 0
    # Fórmula de Hamming: 2^r >= m + r + 1
    while (2**r) < (m + r + 1):
        r += 1
        
    tamanho_total = m + r
    lista_quadro = ['?'] * (tamanho_total + 1) # +1 pois Hamming usa índice 1-based
    
    # 2. Preencher os DADOS nas posições que NÃO são potência de 2
    idx_dados = 0
    for i in range(1, tamanho_total + 1):
        if not _eh_potencia_de_2(i):
            lista_quadro[i] = dados_bits[idx_dados]
            idx_dados += 1
        else:
            lista_quadro[i] = '0' # Placeholder para paridade
            
    # 3. Calcular os bits de Paridade
    # Para cada bit de paridade (posições 1, 2, 4...)
    for i in range(r):
        posicao_paridade = 2**i
        xor_acumulado = 0
        
        # Percorre o quadro verificando quem esse bit de paridade cobre
        # Regra: Se o bit J tem o bit da posição_paridade "ligado", ele entra na conta.
        for j in range(1, tamanho_total + 1):
            # Ex: Se estamos calculando P4 (100), olhamos para 4, 5, 6, 7...
            # Isso é feito com o E bit a bit (&)
            if j & posicao_paridade:
                xor_acumulado ^= int(lista_quadro[j])
                
        # Salva o resultado (0 ou 1) na posição da paridade
        lista_quadro[posicao_paridade] = str(xor_acumulado)
        
    # Retorna string (ignorando o índice 0 que usamos só pra facilitar a matemática)
    return "".join(lista_quadro[1:])

def decodificar_hamming(quadro_recebido: str) -> str:
    """
    Recebe o quadro, verifica paridades, CORRIGE se necessário
    e retorna APENAS os dados originais.
    """
    # Trabalhamos com lista para poder alterar (corrigir) o bit errado
    # Adicionamos um dummy no índice 0 para alinhar com a matemática (1..N)
    lista_bits = ['X'] + list(quadro_recebido)
    n = len(quadro_recebido)
    
    # Vamos calcular a "Síndrome" do erro
    posicao_erro = 0
    
    # Quantos bits de paridade existem? Vamos checar as potências de 2.
    r = 0
    while (2**r) <= n:
        posicao_paridade = 2**r
        xor_verificacao = 0
        
        # Recalcula o XOR para essa posição (incluindo o próprio bit de paridade recebido)
        for j in range(1, n + 1):
            if j & posicao_paridade:
                xor_verificacao ^= int(lista_bits[j])
        
        # Se o xor der 1, significa que a paridade não bateu (erro detectado!)
        if xor_verificacao != 0:
            # A mágica: somamos o valor da paridade à posição do erro
            posicao_erro += posicao_paridade
            
        r += 1
        
    # Se a posição do erro for > 0, temos que corrigir!
    if posicao_erro > 0:
        print(f"   [HAMMING] Correção Automática: Erro detectado e corrigido no bit {posicao_erro}.")
        if posicao_erro <= n:
            # Inverte o bit (0->1 ou 1->0)
            bit_atual = lista_bits[posicao_erro]
            lista_bits[posicao_erro] = '0' if bit_atual == '1' else '1'
            
    # Extrair apenas os dados (removendo as potências de 2)
    dados_limpos = ""
    for i in range(1, n + 1):
        if not _eh_potencia_de_2(i):
            dados_limpos += lista_bits[i]
            
    return dados_limpos