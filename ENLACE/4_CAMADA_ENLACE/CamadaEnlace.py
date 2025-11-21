"""
ENLACE SEPARADO EM RX E TX PARA FACILITAR GUI COM GTK
"""

class Utilitarios:
    """Ferramentas matemáticas estáticas para auxiliar TX e RX."""
    POLINOMIO_CRC32 = 0x104C11DB7
    GRAU_CRC = 32

    @staticmethod
    def is_power_2(n):
        return n > 0 and (n & (n - 1)) == 0

    @staticmethod
    def divisao_crc(numero_alvo):
        divisor = Utilitarios.POLINOMIO_CRC32
        dividendo = numero_alvo
        num_bits = dividendo.bit_length()
        while num_bits >= (Utilitarios.GRAU_CRC + 1):
            shift = num_bits - (Utilitarios.GRAU_CRC + 1)
            dividendo ^= (divisor << shift)
            num_bits = dividendo.bit_length()
        return dividendo

    @staticmethod
    def checksum_math(dados, n_bits):
        mascara = (1 << n_bits) - 1
        # Padding
        resto = len(dados) % n_bits
        if resto != 0:
            dados = ('0' * (n_bits - resto)) + dados
        soma = 0
        for i in range(0, len(dados), n_bits):
            val = int(dados[i:i+n_bits], 2)
            soma += val
            while soma > mascara:
                soma = (soma & mascara) + (soma >> n_bits)
        return soma
    
    @staticmethod
    def get_nome_erro(i):
        return ["Paridade", "Checksum", "CRC-32", "Hamming"][i]
        
    @staticmethod
    def get_nome_enq(i):
        return ["Contagem Caracteres", "Byte Stuffing", "Bit Stuffing"][i]


class Transmissor:
    """Classe responsável por transformar DADOS em QUADROS."""
    
    def processar(self, dados_bits: str, tipo_enquadramento: int, tipo_erro: int) -> dict:
        # 1. Adiciona Controle de Erro
        payload = self._aplicar_controle_erro(dados_bits, tipo_erro)
        # 2. Aplica Enquadramento
        quadro = self._aplicar_enquadramento(payload, tipo_enquadramento)
        
        return {
            "tipo": "TX",
            # AQUI ESTAVA O ERRO: Padronizado para 'payload_protegido'
            "payload_protegido": payload, 
            "quadro_final": quadro,
            "info_erro": Utilitarios.get_nome_erro(tipo_erro),
            "info_enquadramento": Utilitarios.get_nome_enq(tipo_enquadramento)
        }

    def _aplicar_controle_erro(self, bits, tipo):
        # 0:Paridade, 1:Checksum, 2:CRC, 3:Hamming
        if tipo == 0:
            acc = 0
            for b in bits: acc ^= int(b)
            return bits + str(acc)
        elif tipo == 1:
            n = 16
            s = Utilitarios.checksum_math(bits, n)
            c = (~s) & ((1 << n) - 1)
            return bits + format(c, f'0{n}b')
        elif tipo == 2:
            d = int(bits, 2)
            d_padded = d << 32
            r = Utilitarios.divisao_crc(d_padded)
            return bits + format(r, '032b')
        elif tipo == 3:
            m, r = len(bits), 0
            while (2**r) < (m + r + 1): r += 1
            total = m + r
            arr = ['0'] * (total + 1)
            idx = 0
            for i in range(1, total + 1):
                if not Utilitarios.is_power_2(i):
                    arr[i] = bits[idx]
                    idx += 1
            for i in range(r):
                pos = 2**i
                xor = 0
                for j in range(1, total + 1):
                    if j & pos: xor ^= int(arr[j])
                arr[pos] = str(xor)
            return "".join(arr[1:])
        return bits

    def _aplicar_enquadramento(self, bits, tipo):
        # 0:Contagem, 1:Byte, 2:Bit
        if tipo == 0:
            qtd = len(bits) // 8
            if len(bits) % 8 != 0: qtd += 1
            return format(qtd, '08b') + bits
        elif tipo == 1:
            flag, esc = '01111110', '01111101'
            out = ''
            for i in range(0, len(bits), 8):
                byte = bits[i:i+8]
                if byte == flag or byte == esc: out += esc + byte
                else: out += byte
            return flag + out + flag
        elif tipo == 2:
            out, cnt = '', 0
            for b in bits:
                if b == '1':
                    cnt += 1
                    out += '1'
                    if cnt == 5:
                        out += '0'
                        cnt = 0
                else:
                    cnt = 0
                    out += '0'
            return '01111110' + out + '01111110'
        return bits


class Receptor:
    """Classe responsável por validar e limpar o quadro."""
    
    def processar(self, quadro: str, tipo_enquadramento: int, tipo_erro: int) -> dict:
        # 1. Desenquadra
        payload = self._remover_enquadramento(quadro, tipo_enquadramento)
        
        # 2. Verifica Erro
        res = self._verificar_controle_erro(payload, tipo_erro)
        
        return {
            "tipo": "RX",
            "quadro_bruto": quadro,
            "payload_extraido": payload,
            "dados_finais": res['dados'],
            "status": res['status'],
            "detalhes": res['msg'],
            "info_erro": Utilitarios.get_nome_erro(tipo_erro),
            "info_enquadramento": Utilitarios.get_nome_enq(tipo_enquadramento)
        }

    def _remover_enquadramento(self, quadro, tipo):
        if tipo == 0:
            return quadro[8:]
        elif tipo == 1:
            esc = '01111101'
            miolo = quadro[8:-8]
            out, i = '', 0
            while i < len(miolo):
                byte = miolo[i:i+8]
                if byte == esc:
                    i += 8
                    out += miolo[i:i+8]
                else:
                    out += byte
                i += 8
            return out
        elif tipo == 2:
            miolo = quadro[8:-8]
            out, cnt, i = '', 0, 0
            while i < len(miolo):
                b = miolo[i]
                if b == '1':
                    cnt += 1
                    out += '1'
                    if cnt == 5:
                        if (i+1) < len(miolo): i += 1
                        cnt = 0
                else:
                    cnt = 0
                    out += '0'
                i += 1
            return out
        return quadro

    def _verificar_controle_erro(self, bits, tipo):
        if tipo == 0: # Paridade
            dados = bits[:-1]
            acc = 0
            for b in bits: acc ^= int(b)
            if acc == 0: return {'dados': dados, 'status': 'SUCESSO', 'msg': 'Paridade OK'}
            return {'dados': dados, 'status': 'ERRO', 'msg': 'Paridade Inválida'}
        
        elif tipo == 1: # Checksum
            dados = bits[:-16]
            s = Utilitarios.checksum_math(bits, 16)
            c = (~s) & ((1 << 16) - 1)
            if c == 0: return {'dados': dados, 'status': 'SUCESSO', 'msg': 'Checksum OK'}
            return {'dados': dados, 'status': 'ERRO', 'msg': 'Soma Incorreta'}
            
        elif tipo == 2: # CRC
            dados = bits[:-32]
            if len(bits) < 32: return {'dados': "", 'status': 'ERRO', 'msg': 'Curto demais'}
            d = int(bits, 2)
            if Utilitarios.divisao_crc(d) == 0:
                return {'dados': dados, 'status': 'SUCESSO', 'msg': 'CRC OK'}
            return {'dados': dados, 'status': 'ERRO', 'msg': 'CRC Falhou'}
            
        elif tipo == 3: # Hamming
            n = len(bits)
            arr = ['X'] + list(bits)
            erro_pos, r = 0, 0
            while (2**r) <= n:
                pos = 2**r
                xor = 0
                for j in range(1, n+1):
                    if j & pos: xor ^= int(arr[j])
                if xor != 0: erro_pos += pos
                r += 1
            
            if erro_pos > 0:
                if erro_pos <= n:
                    arr[erro_pos] = '0' if arr[erro_pos] == '1' else '1'
                    # Reconstrói dados
                    dados = ""
                    for i in range(1, n+1):
                        if not Utilitarios.is_power_2(i): dados += arr[i]
                    return {'dados': dados, 'status': 'CORRIGIDO', 'msg': f'Erro no bit {erro_pos} corrigido.'}
                else:
                    return {'dados': "", 'status': 'ERRO', 'msg': 'Erro fora do alcance'}
            
            dados = ""
            for i in range(1, n+1):
                if not Utilitarios.is_power_2(i): dados += arr[i]
            return {'dados': dados, 'status': 'SUCESSO', 'msg': 'Hamming OK'}
            
        return {'dados': bits, 'status': 'UNK', 'msg': '?'}