import crc

def visualizador_binario(titulo, bits):
    """Ajuda a visualizar strings longas quebrando linhas se precisar"""
    print(f"{titulo}: {bits} (Len: {len(bits)})")

print("##########################################################")
print("###          TESTBENCH: CRC-32 (IEEE 802)              ###")
print("##########################################################\n")

# ------------------CENÁRIO 1: CÁLCULO E ENVIO----------------------------
print("=== ETAPA 1: GERAÇÃO DO CRC ===")

# Vamos usar uma mensagem curta para caber na tela, letra 'U' (01010101)
mensagem_original = "01010101" 
print(f"1. Mensagem Original:  {mensagem_original}")

# Calcula
pacote_final = crc.calcular_crc(mensagem_original)

# Separa visualmente para o usuário entender
dados = pacote_final[:-32]
codigo_crc = pacote_final[-32:]

print(f"2. Cálculo do CRC (32 bits):")
print(f"   -> Checksum Gerado: {codigo_crc}")
print(f"   -> Pacote Completo: {pacote_final}")


# -------------------------CENÁRIO 2: VERIFICAÇÃO CORRETA-----------------------------------
print("\n=== ETAPA 2: VERIFICAÇÃO NO RECEPTOR ===")

print("1. O Receptor recebe o pacote completo e faz a divisão.")
print("   -> Se o RESTO da divisão for 0, o pacote é aceito.")

valido = crc.verificar_crc(pacote_final)

print(f"2. Resultado da Verificação: {'[APROVADO]' if valido else '[REPROVADO]'}")

if valido:
    msg_limpa = crc.remover_crc(pacote_final)
    print(f"3. Mensagem Extraída: {msg_limpa}")


# ---------------------CENÁRIO 3: SIMULAÇÃO DE ERRO FATAL--------------------------------------------
print("\n=== ETAPA 3: INJEÇÃO DE ERRO (TESTE DE ROBUSTEZ) ===")

# Vamos pegar o pacote perfeito e inverter um bit no meio
# Vamos mudar o último bit da mensagem (antes do CRC começar)
lista_bits = list(pacote_final)
indice_alvo = 7 # O último bit da mensagem original "01010101"

# Inversão Bitwise manual
if lista_bits[indice_alvo] == '0':
    lista_bits[indice_alvo] = '1'
else:
    lista_bits[indice_alvo] = '0'

pacote_corrompido = "".join(lista_bits)

print(f"1. Pacote Corrompido: {pacote_corrompido}")
print(f"   -> Alteramos o bit no índice {indice_alvo}.")
print(f"   -> Original: {pacote_final[indice_alvo]}")
print(f"   -> Novo:     {pacote_corrompido[indice_alvo]}")

# Tenta verificar
print("2. Rodando Verificação...")
check_fail = crc.verificar_crc(pacote_corrompido)

print(f"3. Veredito do Algoritmo: {'[PASSOU - ERRO!]' if check_fail else '[REJEITADO - SUCESSO!]'}")

if check_fail == False:
    print("   -> O CRC funcionou! A divisão retornou um resto diferente de zero.")
    print("   -> O sistema sabe que o dado recebido é lixo.")