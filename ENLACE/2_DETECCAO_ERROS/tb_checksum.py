import checksum

print("##########################################################")
print("###     TESTBENCH: CHECKSUM (TRANSMISSOR/RECEPTOR)     ###")
print("##########################################################\n")

# -------------------CENÁRIO 1: Padrão Internet (16 Bits)-------------------------------
print("=== TESTE 1: Padrão TCP/IP (Passo = 16 bits) ===")

# Simulando 2 blocos de 16 bits: Valor 1 e Valor 2
# Soma esperada: 3. Checksum esperado: Inverso de 3 (...111100)
msg_16 = "0000000000000001" + "0000000000000010" 

# 1. Transmissor gera o pacote
pacote_16 = checksum.transmissor_checksum(msg_16, n_bits=16)

print(f"1. Mensagem Original: {msg_16}")
print(f"2. Pacote Transmitido: {pacote_16}")
print(f"   -> Checksum anexado (ultimos 16): {pacote_16[-16:]}")

# 2. Receptor valida
sucesso_16 = checksum.receptor_checksum(pacote_16, n_bits=16)
print(f"3. Receptor Validou? {'[SIM - SUCESSO]' if sucesso_16 else '[NÃO - ERRO]'}")


# ---------------------CENÁRIO 2: Testando a Parametrização (Passo = 8 Bits)----------------------------------
print("\n=== TESTE 2: Parametrizado (Passo = 8 bits) ===")
print("Demonstrando que a função aceita outros tamanhos de bloco.")

# Mensagem: dois bytes simples
msg_8 = "00000011" + "00000001" # 3 + 1 = 4
# Checksum de 8 bits deve ser o inverso de 4 (00000100) -> 11111011

# 1. Transmissor (passando n_bits=8)
pacote_8 = checksum.transmissor_checksum(msg_8, n_bits=8)

print(f"1. Pacote Transmitido: {pacote_8}")
print(f"   -> Checksum (8 bits): {pacote_8[-8:]}")

# 2. Receptor (passando n_bits=8)
sucesso_8 = checksum.receptor_checksum(pacote_8, n_bits=8)
print(f"2. Receptor Validou? {'[SIM]' if sucesso_8 else '[NÃO]'}")


# -------------------------CENÁRIO 3: Simulação de Erro (No Receptor)-------------------------------
print("\n=== TESTE 3: Detecção de Erro (Passo = 16 bits) ===")

# Vamos pegar o pacote válido do Teste 1 e estragar um bit
lista_bits = list(pacote_16)
lista_bits[0] = '1' if lista_bits[0] == '0' else '0' # Inverte o primeiro bit
pacote_ruim = "".join(lista_bits)

print(f"1. Pacote Corrompido: {pacote_ruim}")

# Receptor tenta validar
validacao = checksum.receptor_checksum(pacote_ruim, n_bits=16)

if validacao == False:
    print("2. Receptor: [ERRO DETECTADO] O pacote foi rejeitado corretamente.")
else:
    print("2. Receptor: [FALHA] O erro passou despercebido.")