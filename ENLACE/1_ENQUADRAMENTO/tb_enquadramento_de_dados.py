import enquadramento_de_dados

print("### INICIANDO TESTES DE ENQUADRAMENTO ###\n")

# ----------------------TESTE 1: CONTAGEM DE CARACTERES-------------------------------------
print("--- Teste 1: Contagem de Caracteres ---")
# Exemplo: 3 bytes quaisquer (24 bits)
entrada_1 = "00000001" + "00000010" + "00000011" 
print(f"Entrada original ({len(entrada_1)//8} bytes): {entrada_1}")

saida_1 = enquadramento_de_dados.contagem_de_caracteres(entrada_1)
print(f"Saída enquadrada:  {saida_1}")
print(f"Explicação: Os primeiros 8 bits ({saida_1[:8]}) representam o número 3 em binário.\n")


# -------------------------TESTE 2: BYTE STUFFING------------------------------------------
print("--- Teste 2: Byte Stuffing ---")
# Cenário crítico: O dado contém exatamente o código da FLAG no meio!
# FLAG usada no código: 01111110
dado_perigoso = "01111110" 
entrada_2 = "11111111" + dado_perigoso + "00000000"

print(f"Entrada com perigo: {entrada_2}")
print("Note que o byte do meio é idêntico à FLAG.")

saida_2 = enquadramento_de_dados.byte_stuffing(entrada_2)
print(f"Saída enquadrada:   {saida_2}")
print("Explicação: O código deve ter inserido um ESC (01111101) antes do byte do meio.\n")


# -------------------------------TESTE 3: BIT STUFFING-------------------------------------------
print("--- Teste 3: Bit Stuffing ---")
# Cenário crítico: Sequência de 6 uns (111111). 
# O protocolo não permite 6 uns, então deve inserir um 0 após o quinto 1.
entrada_3 = "111111" 

print(f"Entrada (6 uns):    {entrada_3}")

saida_3 = enquadramento_de_dados.bit_stuffing(entrada_3)
print(f"Saída enquadrada:   {saida_3}")

# Vamos pegar só o miolo para conferir (tirando as flags de 8 bits das pontas)
miolo = saida_3[8:-8]
print(f"Miolo processado:   {miolo}")
print("Explicação: Veja que virou '1111101'. Um zero foi inserido após o quinto 1.")