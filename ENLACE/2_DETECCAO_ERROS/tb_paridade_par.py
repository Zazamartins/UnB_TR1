import paridade_par

def explicar_conta_xor(bits_str):
    """
    Função auxiliar apenas para MOSTRAR a conta na tela.
    """
    numeros = [int(b) for b in bits_str]
    resultado = 0
    conta_texto = ""
    
    for i, num in enumerate(numeros):
        resultado ^= num
        if i == 0:
            conta_texto += f"{num}"
        else:
            conta_texto += f" ^ {num}"
            
    return f"{conta_texto} = {resultado}"

print("##########################################################")
print("###      TESTBENCH DETALHADO - PARIDADE PAR (XOR)      ###")
print("##########################################################\n")

# ----------------------CENÁRIO 1: TRANSMISSÃO PERFEITA------------------------------------
print("=== ETAPA 1: TRANSMISSÃO NORMAL (SEM ERROS) ===")

# 1. Escolha dos dados
dado_original = "1101" # 3 uns (ímpar)
print(f"1. [ANTES] Dado Original: '{dado_original}'")
print(f"   -> Análise: Temos três '1's. Isso é ÍMPAR.")
print(f"   -> Esperado: O bit de paridade deve ser '1' para tornar o total PAR.")

# 2. Codificação
quadro_codificado = paridade_par.calcular_paridade(dado_original)
bit_adicionado = quadro_codificado[-1]

print(f"\n2. [DURANTE] Processo de Codificação:")
print(f"   -> Cálculo XOR dos dados: {explicar_conta_xor(dado_original)}")
print(f"   -> Bit de paridade calculado: {bit_adicionado}")
print(f"   -> Quadro Final para envio:   '{quadro_codificado}'")

# 3. Verificação
print(f"\n3. [DEPOIS] Verificação no Receptor:")
print(f"   -> O receptor faz o XOR de tudo ({quadro_codificado}).")
print(f"   -> Conta: {explicar_conta_xor(quadro_codificado)}")

is_valido = paridade_par.verificar_erro(quadro_codificado)

if is_valido:
    print(f"   -> RESULTADO: O resultado foi 0. O pacote foi ACEITO.")
else:
    print(f"   -> RESULTADO: O resultado foi 1. O pacote foi REJEITADO.")

# 4. Limpeza
print(f"\n4. [FINAL] Recuperando a mensagem:")
msg_final = paridade_par.limpar_dados(quadro_codificado)
print(f"   -> Mensagem entregue: '{msg_final}'\n")


print("-" * 60 + "\n")


# ------------------------CENÁRIO 2: SIMULAÇÃO DE ERRO-------------------------------------------
print("=== ETAPA 2: SIMULAÇÃO DE RUÍDO (ERRO FORÇADO) ===")


# Vamos pegar o quadro perfeito do teste anterior: '11011'
pacote_integro = quadro_codificado
print(f"1. [ANTES] Pacote saindo do transmissor: '{pacote_integro}'")
print(f"   -> Sabemos que este pacote está correto (XOR = 0).")

# 2. Introduzindo Erro
# Vamos inverter o PRIMEIRO bit (de 1 para 0)
# '11011' vira '01011'
pacote_com_erro = "0" + pacote_integro[1:]

print(f"\n2. [DURANTE] Ocorreu um erro na rede!")
print(f"   -> Bit na posição 0 foi invertido.")
print(f"   -> Pacote que chegou no receptor: '{pacote_com_erro}'")

# 3. Tentativa de Verificação
print(f"\n3. [DEPOIS] O receptor tenta validar:")
print(f"   -> Ele não sabe que houve erro. Ele confia na matemática.")
print(f"   -> Conta do XOR: {explicar_conta_xor(pacote_com_erro)}")

check_erro = paridade_par.verificar_erro(pacote_com_erro)

print(f"\n   -> ANÁLISE DO RESULTADO:")
if check_erro == False: # False significa que detectou erro
    print(f"      O cálculo XOR resultou em 1.")
    print(f"      Isso significa que a quantidade total de 1s é ÍMPAR.")
    print(f"      Como o protocolo é PARIDADE PAR, isso prova que houve corrupção.")
    print(f"      STATUS: SUCESSO! O ERRO FOI DETECTADO CORRETAMENTE.")
else:
    print(f"      FALHA CRÍTICA: O sistema achou que estava tudo bem.")