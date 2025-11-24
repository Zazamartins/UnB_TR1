from CamadaEnlace import Transmissor, Receptor
import random
import time

# ---------------------------CONFIGURAÇÕES VISUAIS E UTILITÁRIOS---------------------
class Cores:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    MAGENTA = "\033[95m"

def print_header(texto):
    print(f"\n{Cores.CYAN}{'='*80}")
    print(f" {texto}")
    print(f"{'='*80}{Cores.RESET}")

def simular_canal_fisico(bits, forcar_erro_pos=None, chance_erro=0.0):
    """Simula o meio físico com injeção de ruído."""
    lista_bits = list(bits)
    erro_ocorreu = False
    posicao = -1

    # Modo 1: Erro forçado
    if forcar_erro_pos is not None:
        if 0 <= forcar_erro_pos < len(lista_bits):
            lista_bits[forcar_erro_pos] = '0' if lista_bits[forcar_erro_pos] == '1' else '1'
            erro_ocorreu = True
            posicao = forcar_erro_pos

    # Modo 2: Erro aleatório
    elif chance_erro > 0:
        if random.random() < chance_erro:
            posicao = random.randint(0, len(lista_bits) - 1)
            lista_bits[posicao] = '0' if lista_bits[posicao] == '1' else '1'
            erro_ocorreu = True

    print(f"\n   {Cores.GRAY}[CANAL FÍSICO] Trafegando {len(bits)} bits...{Cores.RESET}")
    if erro_ocorreu:
        print(f"   {Cores.RED}⚡ RUÍDO DETECTADO! O bit na posição {posicao} foi invertido.{Cores.RESET}")
        # Mostra contexto visual do erro
        inicio = max(0, posicao-3)
        fim = min(len(bits), posicao+4)
        print(f"   {Cores.RED}   Antes: ...{bits[inicio:fim]}...{Cores.RESET}")
        print(f"   {Cores.RED}   Depois:...{''.join(lista_bits)[inicio:fim]}...{Cores.RESET}")
    else:
        print(f"   {Cores.GREEN}✔ Sinal chegou intacto ao receptor.{Cores.RESET}")
        
    return "".join(lista_bits)

def exibir_resultado_rx(res_rx, dado_original):
    print(f"\n   {Cores.BLUE}➔ RECEPTOR (RX):{Cores.RESET}")
    
    # Mostra alertas de tamanho se houver (Feature da GUI)
    detalhes = res_rx['detalhes']
    if "(Aviso:" in detalhes:
        detalhes = detalhes.replace("(Aviso:", f"{Cores.YELLOW}(Aviso:")
    
    print(f"     1. Desenquadramento: {res_rx['info_enquadramento']}")
    print(f"     2. Verificação Erro: {res_rx['info_erro']}")
    
    status = res_rx['status']
    cor_status = Cores.GREEN
    if status == "ERRO": cor_status = Cores.RED
    elif status == "CORRIGIDO": cor_status = Cores.YELLOW
    
    print(f"     3. Status Final:     {cor_status}[{status}]{Cores.RESET} {detalhes}")
    print(f"     4. Dados Entregues:  {Cores.BOLD}{res_rx['dados_finais']}{Cores.RESET}")
    
    if res_rx['dados_finais'] == dado_original:
        print(f"   {Cores.GREEN}✅ SUCESSO: A integridade dos dados foi mantida.{Cores.RESET}")
    else:
        if status == "ERRO":
             print(f"   {Cores.GREEN}🛡️ SEGURANÇA: O sistema rejeitou corretamente o pacote.{Cores.RESET}")
        else:
             print(f"   {Cores.RED}❌ FALHA CRÍTICA: Dados corrompidos foram aceitos!{Cores.RESET}")

# --------------------------------INSTANCIANDO O SISTEMA----------------------------------
tx = Transmissor()
rx = Receptor()

# ---------------------------CENÁRIO 1: (Uso Padrão)----------------------------------------------
print_header("CENÁRIO 1: Byte Stuffing + CRC-32 (Uso Padrão)")
dado_original = "010000010111111001000010" 
print(f"   Dados: {dado_original}")
print(f"   {Cores.GRAY}Teste sem passar parametros extras (usa defaults 1500/32){Cores.RESET}")

# TX Padrão
res_tx = tx.processar(dado_original, tipo_enquadramento=1, tipo_erro=2)
print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
print(f"     Payload: {res_tx['payload_protegido']}")
print(f"     Quadro:  {res_tx['quadro_final']}")

no_fio = simular_canal_fisico(res_tx['quadro_final'])
res_rx = rx.processar(no_fio, tipo_enquadramento=1, tipo_erro=2)
exibir_resultado_rx(res_rx, dado_original)


# -----------------------------CENÁRIO 2: GUI FEATURE - CHECKSUM VARIÁVEL (8 BITS)----------------------------------
print_header("CENÁRIO 2: GUI Feature - Checksum Reduzido (8 bits)")
dado_original = "11111111" # 8 bits de 1s
# Soma = 255 (0xFF). Inverso = 0. Checksum deve ser 00000000.
# Mas como checksum soma blocos, vamos ver o comportamento com tam_edc=8.

print(f"   Dados: {dado_original}")
print(f"   {Cores.MAGENTA}Configuração GUI: Tamanho EDC = 8 bits (padrão era 16){Cores.RESET}")

# TX com Checksum (tipo 1) e tam_edc=8
res_tx = tx.processar(dado_original, 1, 1, tam_edc=8)

print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
print(f"     Payload Protegido: {res_tx['payload_protegido']}")
# Verifica visualmente se adicionou apenas 8 bits
tam_extra = len(res_tx['payload_protegido']) - len(dado_original)
print(f"     {Cores.YELLOW}Check:{Cores.RESET} Adicionados {tam_extra} bits de EDC (Esperado: 8)")

no_fio = simular_canal_fisico(res_tx['quadro_final'])

# RX deve receber o mesmo parametro de tamanho
res_rx = rx.processar(no_fio, 1, 1, tam_edc=8)
exibir_resultado_rx(res_rx, dado_original)


# --------------------------CENÁRIO 3: GUI FEATURE - ESTOURO DE TAMANHO DE QUADRO-------------------------------------
print_header("CENÁRIO 3: GUI Feature - Limite de MTU (Tamanho Máx)")
# Cria um dado grande (80 bits = 10 bytes)
dado_original = "1" * 80 
print(f"   Dados: {len(dado_original)} bits (10 bytes)")
print(f"   {Cores.MAGENTA}Configuração GUI: Tamanho Máx Quadro = 5 bytes (Vai estourar!){Cores.RESET}")

# TX com limite apertado (5 bytes)
res_tx = tx.processar(dado_original, 0, 0, tam_max_quadro=5)

print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
print(f"     Quadro Final: {res_tx['quadro_final']}")
# Verifica se o aviso foi gerado
if res_tx['aviso']:
    print(f"     {Cores.RED}ALERTA GUI:{Cores.RESET}{res_tx['aviso']}")
else:
    print(f"     {Cores.GREEN}Tamanho OK.{Cores.RESET}")

no_fio = simular_canal_fisico(res_tx['quadro_final'])

# RX também verifica
res_rx = rx.processar(no_fio, 0, 0, tam_max_quadro=5)
exibir_resultado_rx(res_rx, dado_original)


# ------------------------------------CENÁRIO 4: HAMMING (Correção)---------------------------------------
print_header("CENÁRIO 4: Hamming (Correção de Erro)")
dado_original = "1001100" # ASCII 'L'
print(f"   Dados: {dado_original}")

# TX Hamming (tipo 3)
res_tx = tx.processar(dado_original, 0, 3)
print(f"\n   {Cores.BLUE}➔ TRANSMISSOR (TX):{Cores.RESET}")
print(f"     Payload: {res_tx['payload_protegido']}")

# Força erro no bit 5
no_fio = simular_canal_fisico(res_tx['quadro_final'], forcar_erro_pos=5)

res_rx = rx.processar(no_fio, 0, 3)
exibir_resultado_rx(res_rx, dado_original)

print(f"\n{Cores.CYAN}{'='*80}")
print(f" FIM DA SIMULAÇÃO")
print(f"{'='*80}{Cores.RESET}")