import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import numpy as np
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

# importa as camadas (fisica e enlace)
from CamadaFisica import Modulador, Sinal
from CamadaEnlace import TransmissorEnlace, ReceptorEnlace


# -------------------------
# Funções auxiliares simples
# -------------------------

def converter_texto_para_bits(texto: str) -> str:
    """Converte texto pra bits..."""
    return "".join(format(ord(c), "08b") for c in texto)


def converter_bits_para_texto(bits: str) -> str:
    """Transforma string de bits pra texto"""
    if not bits:
        return ""
    if len(bits) % 8 != 0:
        # corta o que sobrou, pq senão vira lixo
        bits = bits[: (len(bits) // 8) * 8]
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(byte, 2)))
    return "".join(chars)


def converter_int_seguro(texto, padrao=0):
    """Tenta converter pra int, se der merda retorna padrao."""
    try:
        return int(texto)
    except:
        return padrao


def converter_float_seguro(texto, padrao=0.0):
    """Tenta converter pra float, se falhar retorna padrao."""
    try:
        return float(texto)
    except:
        return padrao


# -------------------------
# Janela principal
# -------------------------
class JanelaPrincipal(Gtk.Window):
    def __init__(self):
        # título da janela
        super().__init__(title="O SIMULADORZINHO")
        self.set_default_size(1000, 700)
        self.set_border_width(8)

        # instâncias das classes de enlace (TX/RX)
        self.modulo_tx_enlace = TransmissorEnlace()
        self.modulo_rx_enlace = ReceptorEnlace()

        # container principal vertical
        caixa_vertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(caixa_vertical)

        # -----------------------------------------------------
        # CONFIGURAÇÕES GERAIS
        # -----------------------------------------------------
        quadro_cfg = Gtk.Frame(label="Configurações")
        caixa_vertical.pack_start(quadro_cfg, False, False, 6)
        grade_cfg = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_cfg.add(grade_cfg)

        # tamanho maximo do quadro (apenas campo, não usado diretamente)
        grade_cfg.attach(Gtk.Label("Tamanho máximo do quadro (bytes):"), 0, 0, 1, 1)
        self.campo_tamanho_max_quadro = Gtk.Entry()
        self.campo_tamanho_max_quadro.set_text("1024")
        grade_cfg.attach(self.campo_tamanho_max_quadro, 1, 0, 1, 1)

        # tamanho do EDC (bits)
        grade_cfg.attach(Gtk.Label("Tamanho do EDC (bits):"), 2, 0, 1, 1)
        self.campo_tamanho_edc = Gtk.Entry()
        self.campo_tamanho_edc.set_text("16")
        grade_cfg.attach(self.campo_tamanho_edc, 3, 0, 1, 1)

        # tipo de enquadramento
        grade_cfg.attach(Gtk.Label("Tipo de Enquadramento:"), 0, 1, 1, 1)
        self.combo_enquadramento = Gtk.ComboBoxText()
        for t in ["Contagem Caracteres", "Byte Stuffing", "Bit Stuffing"]:
            self.combo_enquadramento.append_text(t)
        self.combo_enquadramento.set_active(0)
        grade_cfg.attach(self.combo_enquadramento, 1, 1, 1, 1)

        # tipo de detecção/correção
        grade_cfg.attach(Gtk.Label("Detecção / Correção:"), 2, 1, 1, 1)
        self.combo_deteccao = Gtk.ComboBoxText()
        for t in ["Paridade", "Checksum", "CRC-32", "Hamming"]:
            self.combo_deteccao.append_text(t)
        self.combo_deteccao.set_active(0)
        grade_cfg.attach(self.combo_deteccao, 3, 1, 1, 1)

        # modulação analógica (apenas info, a escolha depois é por seção TX)
        grade_cfg.attach(Gtk.Label("Modulação analógica:"), 0, 2, 1, 1)
        self.combo_mod_analogico = Gtk.ComboBoxText()
        for t in ["ask", "fsk", "psk", "qpsk", "16-qam"]:
            self.combo_mod_analogico.append_text(t)
        self.combo_mod_analogico.set_active(0)
        grade_cfg.attach(self.combo_mod_analogico, 1, 2, 1, 1)

        # opção de ruído
        self.checkbox_ruido = Gtk.CheckButton(label="Ativar ruído (Gaussiano)")
        grade_cfg.attach(self.checkbox_ruido, 2, 2, 1, 1)

        grade_cfg.attach(Gtk.Label("σ (sigma):"), 0, 3, 1, 1)
        self.campo_sigma = Gtk.Entry()
        self.campo_sigma.set_text("0.1")
        grade_cfg.attach(self.campo_sigma, 1, 3, 1, 1)

        # -----------------------------------------------------
        # NOTEBOOK COM AS ABAS TX / RX / FÍSICA
        # -----------------------------------------------------
        bloco_abas = Gtk.Notebook()
        caixa_vertical.pack_start(bloco_abas, True, True, 6)

        # =====================================================
        # TX
        # =====================================================
        pagina_tx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=6)
        bloco_abas.append_page(pagina_tx, Gtk.Label(label="TransmissorEnlace (Enlace)"))

        # entrada de aplicação
        quadro_app = Gtk.Frame(label="Aplicação (TX)")
        pagina_tx.pack_start(quadro_app, False, False, 0)
        grade_app = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_app.add(grade_app)

        grade_app.attach(Gtk.Label("Mensagem:"), 0, 0, 1, 1)
        self.campo_mensagem_texto = Gtk.Entry()
        grade_app.attach(self.campo_mensagem_texto, 1, 0, 3, 1)

        botao_converter = Gtk.Button(label="Converter em bits")
        botao_converter.connect("clicked", self.quando_clicar_converter_texto_para_bits)
        grade_app.attach(botao_converter, 4, 0, 1, 1)

        grade_app.attach(Gtk.Label("Bits originais:"), 0, 1, 1, 1)
        self.visao_bits_originais = Gtk.TextView(width_request=600, height_request=60)
        self.visao_bits_originais.set_editable(False)
        grade_app.attach(self.visao_bits_originais, 1, 1, 4, 1)

        # -------------------------------------------------
        # Camada de Enlace (TX)
        # -------------------------------------------------
        quadro_enlace_tx = Gtk.Frame(label="Camada de Enlace (TX)")
        pagina_tx.pack_start(quadro_enlace_tx, False, False, 0)
        grade_enlace_tx = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_enlace_tx.add(grade_enlace_tx)

        grade_enlace_tx.attach(Gtk.Label("Enquadramento:"), 0, 0, 1, 1)
        self.combo_enq_tx = Gtk.ComboBoxText()
        for t in ["Contagem", "Byte Stuffing", "Bit Stuffing"]:
            self.combo_enq_tx.append_text(t)
        self.combo_enq_tx.set_active(0)
        grade_enlace_tx.attach(self.combo_enq_tx, 1, 0, 1, 1)

        grade_enlace_tx.attach(Gtk.Label("Controle de erro:"), 2, 0, 1, 1)
        self.combo_err_tx = Gtk.ComboBoxText()
        for t in ["Paridade", "Checksum", "CRC", "Hamming"]:
            self.combo_err_tx.append_text(t)
        self.combo_err_tx.set_active(0)
        grade_enlace_tx.attach(self.combo_err_tx, 3, 0, 1, 1)

        botao_aplicar_enlace = Gtk.Button(label="Aplicar Enlace (Gerar Quadro)")
        botao_aplicar_enlace.connect("clicked", self.quando_clicar_aplicar_enlace_transmissao)
        grade_enlace_tx.attach(botao_aplicar_enlace, 0, 1, 2, 1)

        grade_enlace_tx.attach(Gtk.Label("Payload protegido:"), 0, 2, 1, 1)
        self.visao_payload_protegido = Gtk.TextView(width_request=600, height_request=80)
        self.visao_payload_protegido.set_editable(False)
        grade_enlace_tx.attach(self.visao_payload_protegido, 1, 2, 4, 1)

        grade_enlace_tx.attach(Gtk.Label("Quadro final:"), 0, 3, 1, 1)
        self.visao_quadro_final = Gtk.TextView(width_request=600, height_request=80)
        self.visao_quadro_final.set_editable(False)
        grade_enlace_tx.attach(self.visao_quadro_final, 1, 3, 4, 1)

        # -------------------------------------------------
        # Camada Física (TX)
        # -------------------------------------------------
        quadro_fis_tx = Gtk.Frame(label="Camada Física (TX)")
        pagina_tx.pack_start(quadro_fis_tx, True, True, 0)
        grade_fis_tx = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_fis_tx.add(grade_fis_tx)

        grade_fis_tx.attach(Gtk.Label("Modulação analógica:"), 0, 0, 1, 1)
        self.combo_mod_tx = Gtk.ComboBoxText()
        for t in ["ask", "fsk", "psk", "qpsk", "16-qam"]:
            self.combo_mod_tx.append_text(t)
        self.combo_mod_tx.set_active(0)
        grade_fis_tx.attach(self.combo_mod_tx, 1, 0, 1, 1)

        grade_fis_tx.attach(Gtk.Label("Frequência (Hz):"), 2, 0, 1, 1)
        self.campo_frequencia_tx = Gtk.Entry()
        self.campo_frequencia_tx.set_text("1000")
        grade_fis_tx.attach(self.campo_frequencia_tx, 3, 0, 1, 1)

        grade_fis_tx.attach(Gtk.Label("Bits por símbolo:"), 0, 1, 1, 1)
        self.campo_bps_tx = Gtk.Entry()
        self.campo_bps_tx.set_text("1")
        grade_fis_tx.attach(self.campo_bps_tx, 1, 1, 1, 1)

        botao_transmitir = Gtk.Button(label="Transmitir (TX -> sinal modulado)")
        botao_transmitir.connect("clicked", self.quando_clicar_transmitir_sinal_fisico)
        grade_fis_tx.attach(botao_transmitir, 0, 2, 2, 1)

        botao_tx_para_rx = Gtk.Button(label="Enviar TX -> RX (simulado)")
        botao_tx_para_rx.connect("clicked", self.quando_clicar_enviar_tx_para_rx)
        grade_fis_tx.attach(botao_tx_para_rx, 2, 2, 2, 1)

        grade_fis_tx.attach(Gtk.Label("Amostras geradas:"), 0, 3, 1, 1)
        self.rotulo_amostras = Gtk.Label(label="")
        grade_fis_tx.attach(self.rotulo_amostras, 1, 3, 1, 1)

        # =====================================================
        # RX
        # =====================================================
        pagina_rx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=6)
        bloco_abas.append_page(pagina_rx, Gtk.Label(label="ReceptorEnlace (Enlace)"))

        quadro_rx_entrada = Gtk.Frame(label="Entrada (quadros)")
        pagina_rx.pack_start(quadro_rx_entrada, False, False, 0)
        grade_rx_entrada = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_rx_entrada.add(grade_rx_entrada)

        grade_rx_entrada.attach(Gtk.Label("Quadro recebido (bits):"), 0, 0, 1, 1)
        self.visao_entrada_quadro_rx = Gtk.TextView(width_request=700, height_request=120)
        grade_rx_entrada.attach(self.visao_entrada_quadro_rx, 1, 0, 3, 1)

        grade_rx_entrada.attach(Gtk.Label("Enquadramento usado:"), 0, 1, 1, 1)
        self.combo_enq_rx = Gtk.ComboBoxText()
        for t in ["Contagem", "Byte Stuffing", "Bit Stuffing"]:
            self.combo_enq_rx.append_text(t)
        self.combo_enq_rx.set_active(0)
        grade_rx_entrada.attach(self.combo_enq_rx, 1, 1, 1, 1)

        grade_rx_entrada.attach(Gtk.Label("Controle de erro usado:"), 2, 1, 1, 1)
        self.combo_err_rx = Gtk.ComboBoxText()
        for t in ["Paridade", "Checksum", "CRC", "Hamming"]:
            self.combo_err_rx.append_text(t)
        self.combo_err_rx.set_active(0)
        grade_rx_entrada.attach(self.combo_err_rx, 3, 1, 1, 1)

        botao_processar_rx = Gtk.Button(label="Processar RX")
        botao_processar_rx.connect("clicked", self.quando_clicar_processar_recepcao)
        grade_rx_entrada.attach(botao_processar_rx, 0, 2, 1, 1)

        # saída RX
        quadro_rx_saida = Gtk.Frame(label="Resultados (RX)")
        pagina_rx.pack_start(quadro_rx_saida, True, True, 0)
        grade_rx_saida = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_rx_saida.add(grade_rx_saida)

        grade_rx_saida.attach(Gtk.Label("Quadro bruto:"), 0, 0, 1, 1)
        self.visao_quadro_bruto = Gtk.TextView(width_request=700, height_request=80)
        grade_rx_saida.attach(self.visao_quadro_bruto, 1, 0, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Payload extraído:"), 0, 1, 1, 1)
        self.visao_payload_extraido = Gtk.TextView(width_request=700, height_request=80)
        grade_rx_saida.attach(self.visao_payload_extraido, 1, 1, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Dados finais (bits):"), 0, 2, 1, 1)
        self.visao_dados_finais_bits = Gtk.TextView(width_request=700, height_request=80)
        grade_rx_saida.attach(self.visao_dados_finais_bits, 1, 2, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Dados finais (texto):"), 0, 3, 1, 1)
        self.rotulo_texto_rx = Gtk.Label(label="")
        grade_rx_saida.attach(self.rotulo_texto_rx, 1, 3, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Status:"), 0, 4, 1, 1)
        self.rotulo_status_rx = Gtk.Label(label="")
        grade_rx_saida.attach(self.rotulo_status_rx, 1, 4, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Detalhes:"), 0, 5, 1, 1)
        self.rotulo_detalhes_rx = Gtk.Label(label="")
        grade_rx_saida.attach(self.rotulo_detalhes_rx, 1, 5, 3, 1)

        # =====================================================
        # Aba Física visualizações simples
        # =====================================================
        pagina_fis = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=6)
        bloco_abas.append_page(pagina_fis, Gtk.Label(label="Camada Física"))

        quadro_vis_fis = Gtk.Frame(label="Visualização Física")
        pagina_fis.pack_start(quadro_vis_fis, True, True, 0)
        grade_vis_fis = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_vis_fis.add(grade_vis_fis)

        botao_mostrar_codificado = Gtk.Button(label="Mostrar sinal codificado")
        botao_mostrar_codificado.connect("clicked", self.quando_clicar_mostrar_sinal_codificado)
        grade_vis_fis.attach(botao_mostrar_codificado, 0, 0, 1, 1)

        botao_mostrar_modulado = Gtk.Button(label="Mostrar sinal modulado")
        botao_mostrar_modulado.connect("clicked", self.quando_clicar_mostrar_sinal_modulado)
        grade_vis_fis.attach(botao_mostrar_modulado, 1, 0, 1, 1)

        # logs gerais
        quadro_logs = Gtk.Frame(label="resulatdo da budega")
        caixa_vertical.pack_start(quadro_logs, False, False, 0)
        self.caixa_logs = Gtk.TextView(height_request=100)
        self.caixa_logs.set_editable(False)
        quadro_logs.add(self.caixa_logs)

        # variáveis 
        self.ultimos_bits = ""
        self.ultimo_payload = ""
        self.ultimo_quadro = ""
        self.ultimo_sinal = None
        self.ultima_taxa = 1000

        # mostra a janela
        self.show_all()

    # =======================
    # Funções do TX 
    # =======================
    def quando_clicar_converter_texto_para_bits(self, widget):
        """Quando o cara clica no botão converter bits."""
        texto = self.campo_mensagem_texto.get_text()
        bits = converter_texto_para_bits(texto)
        self.ultimos_bits = bits
        # atualiza a caixa de texto com os bits
        self.visao_bits_originais.get_buffer().set_text(bits)
        self._registrar_log("Mensagem convertida em bits")

    def quando_clicar_aplicar_enlace_transmissao(self, widget):
        """Aplica enquadramento + controle de erro (usa o modulo de enlace)."""
        if not self.ultimos_bits:
            self._registrar_log("Nenhuma mensagem convertida em bits.")
            return

        tipo_enq = self.combo_enq_tx.get_active()
        tipo_err = self.combo_err_tx.get_active()

        resultado = self.modulo_tx_enlace.processar(self.ultimos_bits, tipo_enq, tipo_err)

        self.ultimo_payload = resultado.get("payload_protegido", "")
        self.ultimo_quadro = resultado.get("quadro_final", "")

        self._definir_texto_na_caixa(self.visao_payload_protegido, self.ultimo_payload)
        self._definir_texto_na_caixa(self.visao_quadro_final, self.ultimo_quadro)

        info = f"Enlace aplicado: {resultado.get('info_enquadramento')} / {resultado.get('info_erro')}"
        self._registrar_log(info)

    def quando_clicar_transmitir_sinal_fisico(self, widget):
        """Pega o payload (ou bits originais) e manda pra camada física (modulação)."""
        if not self.ultimo_payload and not self.ultimos_bits:
            self._registrar_log("Sem payload para modular.")
            return

        bits_para_mod = self.ultimo_payload or self.ultimos_bits
        arr_bits = np.array([int(b) for b in bits_para_mod])

        mod_tipo = self.combo_mod_tx.get_active_text()
        freq = converter_float_seguro(self.campo_frequencia_tx.get_text(), 1000.0)
        bps = converter_int_seguro(self.campo_bps_tx.get_text(), 1)

        taxa = int(freq * 1000) if freq > 0 else 1000

        modulador = Modulador(
            modulacao=mod_tipo,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=taxa,
            debug=False
        )

        sinal = modulador.processar_sinal(arr_bits)

        self.ultimo_sinal = sinal
        self.ultima_taxa = modulador.taxa_amostragem

        self.rotulo_amostras.set_text(str(len(sinal)))
        self._registrar_log("Sinal modulado gerado.")

        # abre janela com gráfico
        tela_plot = JanelaGrafico(sinal, modulador.taxa_amostragem, titulo="Sinal modulado (TX)")
        tela_plot.show_all()

    def quando_clicar_enviar_tx_para_rx(self, widget):
        """Copia o quadro gerado na aba TX para a aba RX (simulação)."""
        if not self.ultimo_quadro:
            self._registrar_log("Nenhum quadro gerado.")
            return

        self.visao_entrada_quadro_rx.get_buffer().set_text(self.ultimo_quadro)
        self.combo_enq_rx.set_active(self.combo_enq_tx.get_active())
        self.combo_err_rx.set_active(self.combo_err_tx.get_active())

        self._registrar_log("Quadro enviado TX -> RX (simulado)")

    # =======================
    # Funções do RX (callbacks)
    # =======================
    def quando_clicar_processar_recepcao(self, widget):
        """Processa o quadro recebido: desenquadrar, verificar erro, retornar dados."""
        buf = self.visao_entrada_quadro_rx.get_buffer()
        quadro = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()

        if not quadro:
            self._registrar_log("Quadro vazio.")
            return

        tipo_enq = self.combo_enq_rx.get_active()
        tipo_err = self.combo_err_rx.get_active()

        resultado = self.modulo_rx_enlace.processar(quadro, tipo_enq, tipo_err)

        self._definir_texto_na_caixa(self.visao_quadro_bruto, resultado.get("quadro_bruto", ""))
        self._definir_texto_na_caixa(self.visao_payload_extraido, resultado.get("payload_extraido", ""))
        self._definir_texto_na_caixa(self.visao_dados_finais_bits, resultado.get("dados_finais", ""))

        texto_final = converter_bits_para_texto(resultado.get("dados_finais", "")) if resultado.get("dados_finais") else ""
        self.rotulo_texto_rx.set_text(texto_final)

        self.rotulo_status_rx.set_text(resultado.get("status", ""))
        self.rotulo_detalhes_rx.set_text(resultado.get("detalhes", ""))

        self._registrar_log(f"RX processado: {resultado.get('status')}")

    # =======================
    # Funções da parte física (visualizações)
    # =======================
    def quando_clicar_mostrar_sinal_codificado(self, widget):
        """Mostra o sinal codificado (antes da modulação)."""
        if not self.ultimos_bits:
            self._registrar_log("Nenhum bit convertido.")
            return

        bps = converter_int_seguro(self.campo_bps_tx.get_text(), 1)
        obj_sinal = Sinal(bits_por_simbolo=bps, taxa_amostragem=1000)

        arr_bits = np.array([int(b) for b in self.ultimos_bits])
        simbolos = obj_sinal.sequencia_de_bits_para_simbolos(arr_bits)
        dec = obj_sinal.binario_para_decimal(simbolos)

        onda = obj_sinal.gerar_pulso_tensao(dec, tempo_de_simbolo=1.0, simbolos_por_periodo=4).flatten()

        tela_plot = JanelaGrafico(onda, obj_sinal.taxa_amostragem, titulo="Sinal Codificado")
        tela_plot.show_all()

    def quando_clicar_mostrar_sinal_modulado(self, widget):
        """Mostra o último sinal modulado gerado."""
        if self.ultimo_sinal is None:
            self._registrar_log("Nenhum sinal modulado ainda.")
            return

        tela_plot = JanelaGrafico(self.ultimo_sinal, self.ultima_taxa, titulo="Sinal Modulado (último)")
        tela_plot.show_all()

    # -------------------------
    # métodos auxiliares privados
    # -------------------------
    def _definir_texto_na_caixa(self, caixa: Gtk.TextView, texto: str):
        caixa.get_buffer().set_text(texto)

    def _registrar_log(self, mensagem: str):
        buf = self.caixa_logs.get_buffer()
        anterior = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        buf.set_text(anterior + mensagem + "\n")


# -------------------------
# Janela de plot 
# -------------------------
class JanelaGrafico(Gtk.Window):
    """Janela simples que plota o sinal usando matplotlib."""

    def __init__(self, sinal: np.ndarray, taxa_amostragem: int, titulo="Sinal"):
        super().__init__(title=titulo)
        self.set_default_size(900, 650)

        caixa = Gtk.Box()
        self.add(caixa)

        figura = Figure(figsize=(9, 6))
        canvas = FigureCanvas(figura)
        caixa.pack_start(canvas, True, True, 0)

        ax = figura.add_subplot(1, 1, 1)
        tempo = np.arange(0, len(sinal)) / taxa_amostragem

        ax.plot(tempo, sinal)
        ax.set_title(titulo)
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Amplitude")
        ax.grid()

        canvas.draw()


# -------------------------
# executa o programa
# -------------------------
def main():
    janela = JanelaPrincipal()
    janela.connect("destroy", Gtk.main_quit)
    janela.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()