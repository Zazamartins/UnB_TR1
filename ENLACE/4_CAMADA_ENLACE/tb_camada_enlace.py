from CamadaEnlace import Transmissor, Receptor
import random
import time

# ==============================================================================
# CONFIGURAÇÕES VISUAIS E UTILITÁRIOS
# ==============================================================================
class Cores:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

def print_header(texto):
    print(f"\n{Cores.CYAN}{'='*70}")
    print(f" {texto}")
    print(f"{'='*70}{Cores.RESET}")

def simular_canal_fisico(bits, forcar_erro_pos=None, chance_erro=0.0):
    """
    Simula o meio físico. Pode injetar erro aleatório ou em posição fixa.
    """
    lista_bits = list(bits)
    erro_ocorreu = False
    posicao = -1

    # Modo 1: Erro forçado (para testes determinísticos)
    if forcar_erro_pos is not None:
        if 0 <= forcar_erro_pos < len(lista_bits):
            lista_bits[forcar_erro_pos] = '0' if lista_bits[forcar_erro_pos] == '1' else '1'
            erro_ocorreu = True
            posicao = forcar_erro_pos

    # Modo 2: Erro aleatório (simulação real)
    elif chance_erro > 0:
        if random.random() < chance_erro:
            posicao = random.randint(0, len(lista_bits) - 1)
            lista_bits[posicao] = '0' if lista_bits[posicao] == '1' else '1'
            erro_ocorreu = True

    print(f"\n   {Cores.GRAY}[CANAL FÍSICO] Trafegando {len(bits)} bits...{Cores.RESET}")
    if erro_ocorreu:
        print(f"   {Cores.RED}⚡ RUÍDO DETECTADO! O bit na posição {posicao} foi invertido.{Cores.RESET}")
        print(f"   {Cores.RED}   Original: ...{bits[max(0, posicao-3):min(len(bits), posicao+4)]}...{Cores.RESET}")
        bits_mod = "".join(lista_bits)
        print(f"   {Cores.RED}   Alterado: ...{bits_mod[max(0, posicao-3):min(len(lista_bits), posicao+4)]}...{Cores.RESET}")
    else:
        print(f"   {Cores.GREEN}✔ Sinal chegou intacto ao receptor.{Cores.RESET}")
        
    return "".join(lista_bits)

def exibir_resultado_rx(res_rx, dado_original):
    print(f"\n   {Cores.BLUE}➔ RECEPTOR (RX):{Cores.RESET}")
    print(f"     1. Desenquadramento: {res_rx['info_enquadramento']}")
    print(f"     2. Verificação Erro: {res_rx['info_erro']}")
    
    status = res_rx['status']
    cor_status = Cores.GREEN
    if status == "ERRO": cor_status = Cores.RED
    elif status == "CORRIGIDO": cor_status = Cores.YELLOW
    
    print(f"     3. Status Final:     {cor_status}[{status}] {res_rx['detalhes']}{Cores.RESET}")
    print(f"     4. Dados Entregues:  {Cores.BOLD}{res_rx['dados_finais']}{Cores.RESET}")
    
    if res_rx['dados_finais'] == dado_original:
        print(f"   {Cores.GREEN}✅ SUCESSO: A mensagem recebida é IDÊNTICA à enviada.{Cores.RESET}")
    else:
        if status == "ERRO":
             print(f"   {Cores.GREEN}🛡️ SEGURANÇA: O sistema rejeitou corretamente o pacote corrompido.{Cores.RESET}")
        else:
             print(f"   {Cores.RED}❌ FALHA CRÍTICA: Dados diferentes foram aceitos!{Cores.RESET}")


# ==============================================================================
# INSTANCIANDO O SISTEMA
# ==============================================================================
tx = Transmissor()
rx = Receptor()

# ==============================================================================
# CENÁRIO 1: BYTE STUFFING + CRC-32 (O Clássico Robusto)
# ==============================================================================
print_header("CENÁRIO 1: Byte Stuffing + CRC-32 (Sucesso)")

# Dados contendo a FLAG (01111110) no meio para testar o Stuffing
# 01000001 (A) + 01111110 (FLAG) + 01000010 (B)
dado_original = "010000010111111001000010" 
print(f"   Dados Originais: {dado_original}")
print(f"   {Cores.YELLOW}Nota: O dado contém a sequência da FLAG no meio! O Byte Stuffing deve tratar.{Cores.RESET}")

# 1. Transmissão (Enquadramento=1 [Byte], Erro=2 [CRC])
print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
res_tx = tx.processar(dado_original, tipo_enquadramento=1, tipo_erro=2)
print(f"     1. Payload Protegido (CRC add): {res_tx['payload_protegido']}")
print(f"     2. Quadro (Com Stuffing):       {res_tx['quadro_final']}")
print(f"        {Cores.GRAY}(Veja que a string cresceu para escapar a flag interna){Cores.RESET}")

# 2. Canal (Sem erro)
no_fio = simular_canal_fisico(res_tx['quadro_final'], chance_erro=0.0)

# 3. Recepção
res_rx = rx.processar(no_fio, tipo_enquadramento=1, tipo_erro=2)
exibir_resultado_rx(res_rx, dado_original)


# ==============================================================================
# CENÁRIO 2: BIT STUFFING + CHECKSUM (Detecção de Erro)
# ==============================================================================
print_header("CENÁRIO 2: Bit Stuffing + Checksum (Detecção de Erro)")

# Sequência com muitos 1s para testar Bit Stuffing
dado_original = "1111111111111111" # 16 uns
print(f"   Dados Originais: {dado_original}")

# 1. Transmissão (Enquadramento=2 [Bit], Erro=1 [Checksum])
print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
res_tx = tx.processar(dado_original, tipo_enquadramento=2, tipo_erro=1)
print(f"     1. Payload Protegido: {res_tx['payload_protegido']}")
print(f"     2. Quadro Final:      {res_tx['quadro_final']}")

# 2. Canal (COM ERRO FORÇADO)
# Vamos inverter um bit no meio do payload
posicao_erro = 10 
no_fio = simular_canal_fisico(res_tx['quadro_final'], forcar_erro_pos=posicao_erro)

# 3. Recepção
res_rx = rx.processar(no_fio, tipo_enquadramento=2, tipo_erro=1)
exibir_resultado_rx(res_rx, dado_original)


# ==============================================================================
# CENÁRIO 3: CONTAGEM CARACTERES + HAMMING (Correção Mágica)
# ==============================================================================
print_header("CENÁRIO 3: Contagem + Hamming (Correção de Erro)")

# ASCII 'K' (75) -> 01001011
dado_original = "01001011" 
print(f"   Dados Originais: {dado_original}")

# 1. Transmissão (Enquadramento=0 [Contagem], Erro=3 [Hamming])
print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
res_tx = tx.processar(dado_original, tipo_enquadramento=0, tipo_erro=3)
print(f"     1. Payload (Hamming): {res_tx['payload_protegido']}")
print(f"     2. Quadro Final:      {res_tx['quadro_final']}")

# 2. Canal (COM ERRO FORÇADO NO DADO)
# O Hamming deve ser capaz de corrigir 1 bit errado.
# Vamos contar onde começa o dado real dentro do quadro (pula cabeçalho de contagem 8 bits)
# O payload Hamming expande os bits. Vamos chutar um bit no meio.
no_fio = simular_canal_fisico(res_tx['quadro_final'], forcar_erro_pos=12)

# 3. Recepção
res_rx = rx.processar(no_fio, tipo_enquadramento=0, tipo_erro=3)
exibir_resultado_rx(res_rx, dado_original)

print(f"\n{Cores.CYAN}{'='*70}")
print(f" FIM DA SIMULAÇÃO")
print(f"{'='*70}{Cores.RESET}")