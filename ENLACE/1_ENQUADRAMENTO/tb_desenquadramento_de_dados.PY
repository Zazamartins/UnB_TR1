import desenquadramento_de_dados

print("### INICIANDO TESTES DE DESENQUADRAMENTO (RECEPÇÃO) ###\n")

# ------------------TESTE 1: DES(CONTAGEM DE CARACTERES)--------------------------------------------
print("--- Teste 1: Recuperação por Contagem ---")
# Simulação: Chegou um quadro com cabeçalho '3' (00000011) seguido de 3 bytes de dados
quadro_cheio = "00000011" + "11110000" + "10101010" + "00001111"
print(f"Recebido da rede: {quadro_cheio}")

resultado_1 = desenquadramento_de_dados.desenquadramento_contagem_de_caracteres(quadro_cheio)

print(f"Dados extraídos:  {resultado_1}")
print("Explicação: O cabeçalho (primeiros 8 bits) foi removido com sucesso.\n")


#-------------------- TESTE 2: DES(BYTE STUFFING)----------------------------------------------
print("--- Teste 2: Recuperação Byte Stuffing ---")
# Simulação: Dados onde houve stuffing.
# FLAG + DADO + ESC + FLAG(dado) + DADO + FLAG
# Note: O 'ESC + FLAG' deve virar apenas 'FLAG' na saída.
FLAG = "01111110"
ESC  = "01111101"
DADO = "11111111"

quadro_stuffing = FLAG + DADO + ESC + FLAG + DADO + FLAG
print(f"Recebido (Raw):   {quadro_stuffing}")
print("Estrutura: [FLAG] [DADO] [ESC][FLAG] [DADO] [FLAG]")

resultado_2 = desenquadramento_de_dados.desenquadramento_byte_stuffing(quadro_stuffing)

print(f"Dados extraídos:  {resultado_2}")
print(f"Esperado:         {DADO + FLAG + DADO}")
print("Explicação: O ESC foi removido e a FLAG seguinte foi mantida como dado.\n")


# -------------------------TESTE 3: DES(BIT STUFFING)-----------------------------------------
print("--- Teste 3: Recuperação Bit Stuffing ---")
# Simulação: Recebemos '1111101'.
# Sabemos que após cinco 1s, o 0 é lixo (stuffing) e o 1 seguinte é dado real.
# O dado original era '111111'.
miolo_com_stuffing = "1111101" 
quadro_bits = "01111110" + miolo_com_stuffing + "01111110"

print(f"Recebido (Raw):   {quadro_bits}")
print(f"Miolo (stuffed):  {miolo_com_stuffing} (Note o '0' após cinco 1s)")

resultado_3 = desenquadramento_de_dados.desenquadramento_bit_stuffing(quadro_bits)

print(f"Dados extraídos:  {resultado_3}")
print("Explicação: O '0' intruso foi removido, restaurando a sequência '111111'.")