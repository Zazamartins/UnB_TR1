import hamming

print("##########################################################")
print("###          TESTBENCH: CÓDIGO DE HAMMING              ###")
print("##########################################################\n")

# --------------------------CENÁRIO 1: CODIFICAÇÃO E ENVIO---------------------------------------
print("=== ETAPA 1: CODIFICAÇÃO ===")
# Vamos enviar a letra 'D' em ASCII (1000100)
dado_original = "1000100"
print(f"1. Dado Original (7 bits): {dado_original}")

quadro_protegido = hamming.codificar_hamming(dado_original)

print(f"2. Quadro Hamming Gerado:  {quadro_protegido}")
print(f"   -> Tamanho aumentou para {len(quadro_protegido)} bits (4 de paridade adicionados).")
print(f"   -> Os bits extras estão nas posições 1, 2, 4 e 8.")


# -------------------------CENÁRIO 2: RECEPÇÃO PERFEITA------------------------------------------
print("\n=== ETAPA 2: RECEPÇÃO SEM ERROS ===")
dado_recuperado = hamming.decodificar_hamming(quadro_protegido)
print(f"1. Dado decodificado:      {dado_recuperado}")
print(f"   -> Status: {'SUCESSO' if dado_recuperado == dado_original else 'FALHA'}")


# -----------------------CENÁRIO 3: CORREÇÃO DE ERRO (A MÁGICA)-------------------------------------
print("\n=== ETAPA 3: SIMULAÇÃO DE ERRO E CORREÇÃO ===")

# Vamos introduzir um erro proposital na posição 6
posicao_ruido = 6 # Posição baseada em 1 (humana)
lista = list(quadro_protegido)
idx_array = posicao_ruido - 1 # Índice array (Python)

# Inverte o bit
lista[idx_array] = '0' if lista[idx_array] == '1' else '1'
quadro_corrompido = "".join(lista)

print(f"1. Introduzindo erro na posição {posicao_ruido}...")
print(f"   Original:   {quadro_protegido}")
print(f"   Corrompido: {quadro_corrompido}")

# Agora o receptor vai tentar ler. Ele deve ser capaz de consertar sozinho.
print("2. Receptor processando...")
dado_corrigido = hamming.decodificar_hamming(quadro_corrompido)

print(f"3. Resultado Final: {dado_corrigido}")

if dado_corrigido == dado_original:
    print("   >>> STATUS: SUCESSO TOTAL! O bit foi consertado magicamente. <<<")
else:
    print("   >>> STATUS: FALHA NA CORREÇÃO. <<<")