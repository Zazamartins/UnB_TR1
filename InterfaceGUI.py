import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import numpy as np
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

# importa as camadas (fisica e enlace)
from CamadaFisica import (
    CODIFICACOES,
    MODULACOES,
    Modulador,
    Demodulador,
    Decodificador,
    Sinal,
    TransmissorBandaBase,
)
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
        byte = bits[i : i + 8]
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

        grade_cfg.attach(Gtk.Label("σ (sigma):"), 0, 2, 1, 1)
        self.campo_sigma = Gtk.Entry()
        self.campo_sigma.set_text("0.1")
        grade_cfg.attach(self.campo_sigma, 1, 2, 1, 1)

        # opção de ruído
        self.checkbox_debug = Gtk.CheckButton(label="Ativar flag de debug")
        grade_cfg.attach(self.checkbox_debug, 2, 2, 1, 1)

        # -----------------------------------------------------
        # NOTEBOOK COM AS ABAS TX / RX / FÍSICA
        # -----------------------------------------------------
        bloco_abas = Gtk.Notebook()
        caixa_vertical.pack_start(bloco_abas, True, True, 6)

        # =====================================================
        # TX
        # =====================================================
        self.scrolledwindow_tx = Gtk.ScrolledWindow()
        self.scrolledwindow_tx.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.pagina_tx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=6)
        self.scrolledwindow_tx.add(self.pagina_tx)
        bloco_abas.append_page(self.scrolledwindow_tx, Gtk.Label(label="Transmissor (Tx)"))

        # entrada de aplicação
        quadro_app = Gtk.Frame(label="Aplicação (Tx)")
        self.pagina_tx.pack_start(quadro_app, False, False, 0)
        grade_app = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_app.add(grade_app)

        grade_app.attach(Gtk.Label("Mensagem:"), 0, 0, 1, 1)
        self.campo_mensagem_texto = Gtk.Entry()
        grade_app.attach(self.campo_mensagem_texto, 1, 0, 3, 1)

        botao_converter = Gtk.Button(label="Converter em bits")
        botao_converter.connect("clicked", self.quando_clicar_converter_texto_para_bits)
        grade_app.attach(botao_converter, 4, 0, 1, 1)

        grade_app.attach(Gtk.Label("Bits:"), 0, 1, 1, 1)
        self.visao_bits_originais = Gtk.TextView(width_request=700, height_request=20)
        self.visao_bits_originais.set_editable(False)
        Gtk.TextView.set_pixels_above_lines(self.visao_bits_originais, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_bits_originais, Gtk.WrapMode.CHAR)
        grade_app.attach(self.visao_bits_originais, 1, 1, 1, 1)

        # -------------------------------------------------
        # Camada de Enlace (Tx)
        # -------------------------------------------------
        quadro_enlace_tx = Gtk.Frame(label="Camada de Enlace (Tx)")
        self.pagina_tx.pack_start(quadro_enlace_tx, False, False, 0)
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
        botao_aplicar_enlace.connect(
            "clicked", self.quando_clicar_aplicar_enlace_transmissao
        )
        grade_enlace_tx.attach(botao_aplicar_enlace, 0, 1, 2, 1)

        grade_enlace_tx.attach(Gtk.Label("Payload protegido:"), 0, 2, 1, 1)
        self.visao_payload_protegido = Gtk.TextView(
            width_request=700, height_request=20
        )
        self.visao_payload_protegido.set_editable(False)
        Gtk.TextView.set_pixels_above_lines(self.visao_payload_protegido, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_payload_protegido, Gtk.WrapMode.CHAR)
        grade_enlace_tx.attach(self.visao_payload_protegido, 1, 2, 1, 1)

        grade_enlace_tx.attach(Gtk.Label("Quadro final:"), 0, 3, 1, 1)
        self.visao_quadro_final = Gtk.TextView(width_request=700, height_request=20)
        self.visao_quadro_final.set_editable(False)
        Gtk.TextView.set_pixels_above_lines(self.visao_quadro_final, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_quadro_final, Gtk.WrapMode.CHAR)
        grade_enlace_tx.attach(self.visao_quadro_final, 1, 3, 1, 1)

        # -------------------------------------------------
        # Camada Física (Tx)
        # -------------------------------------------------
        quadro_fis_tx = Gtk.Frame(label="Camada Física (Tx)")
        self.pagina_tx.pack_start(quadro_fis_tx, True, True, 0)
        grade_fis_tx = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_fis_tx.add(grade_fis_tx)

        grade_fis_tx.attach(Gtk.Label("Modulação analógica:"), 0, 0, 1, 1)
        self.combo_mod_tx = Gtk.ComboBoxText()
        for t in MODULACOES:
            self.combo_mod_tx.append_text(t)
        self.combo_mod_tx.set_active(0)
        grade_fis_tx.attach(self.combo_mod_tx, 1, 0, 1, 1)

        grade_fis_tx.attach(Gtk.Label("Frequência (Hz):"), 2, 0, 1, 1)
        self.campo_frequencia_tx = Gtk.Entry()
        self.campo_frequencia_tx.set_text("1000")
        grade_fis_tx.attach(self.campo_frequencia_tx, 3, 0, 1, 1)

        grade_fis_tx.attach(Gtk.Label("Modulação digital:"), 0, 1, 1, 1)
        self.combo_mod_digital_tx = Gtk.ComboBoxText()
        for t in CODIFICACOES:
            self.combo_mod_digital_tx.append_text(t)
        self.combo_mod_digital_tx.set_active(0)
        grade_fis_tx.attach(self.combo_mod_digital_tx, 1, 1, 1, 1)

        grade_fis_tx.attach(Gtk.Label("Bits por símbolo:"), 2, 1, 1, 1)
        self.campo_bps_tx = Gtk.Entry()
        self.campo_bps_tx.set_text("1")
        grade_fis_tx.attach(self.campo_bps_tx, 3, 1, 1, 1)

        botao_transmitir_modulado = Gtk.Button(
            label="Transmitir sinal modulado (Tx -> Rx)"
        )
        botao_transmitir_modulado.connect(
            "clicked", self.quando_clicar_transmitir_sinal_fisico_modulado
        )
        grade_fis_tx.attach(botao_transmitir_modulado, 0, 2, 2, 1)

        botao_transmitir_codificado = Gtk.Button(
            label="Transmitir sinal codificado (Tx -> Rx)"
        )
        botao_transmitir_codificado.connect(
            "clicked", self.quando_clicar_transmitir_sinal_fisico_codificado
        )
        grade_fis_tx.attach(botao_transmitir_codificado, 2, 2, 2, 1)

        grade_fis_tx.attach(Gtk.Label("Amostras geradas:"), 0, 3, 1, 1)
        self.rotulo_amostras = Gtk.Label(label="")
        grade_fis_tx.attach(self.rotulo_amostras, 1, 3, 1, 1)
        
        quadro_plots = Gtk.Frame(label="Visualização do Sinal (Tx)")
        self.pagina_tx.pack_start(quadro_plots, True, True, 0)
        fig_tx = Figure(figsize=(12, 10))
        fig_tx.tight_layout()
        self.canvas_tx = FigureCanvas(fig_tx)
        quadro_plots.add(self.canvas_tx)
        self.canvas_tx.set_size_request(900, 700)
        self.canvas_tx.draw()

        # =====================================================
        # RX
        # =====================================================
        scrollable_rx = Gtk.ScrolledWindow()
        scrollable_rx.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        pagina_rx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=6)
        scrollable_rx.add(pagina_rx)
        bloco_abas.append_page(scrollable_rx, Gtk.Label(label="Receptor (Rx)"))

        # =====================================================
        # Camada Física
        # =====================================================
        
        quadro_fis_rx = Gtk.Frame(label="Camada Física (Rx)")
        pagina_rx.pack_start(quadro_fis_rx, False, False, 0)
        grade_fis_rx = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_fis_rx.add(grade_fis_rx)
        grade_fis_rx.attach(Gtk.Label("Bits decodificados:"), 0, 3, 1, 1)
        self.visao_bits_decodificados = Gtk.TextView(width_request=700, height_request=20)
        self.visao_bits_decodificados.set_editable(False)
        Gtk.TextView.set_pixels_above_lines(self.visao_bits_decodificados, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_bits_decodificados, Gtk.WrapMode.CHAR)
        grade_fis_rx.attach(self.visao_bits_decodificados, 1, 3, 1, 1)
        
        # =====================================================
        # Camada Enlace
        # =====================================================
        quadro_rx_entrada = Gtk.Frame(label="Enlace (Rx)")
        pagina_rx.pack_start(quadro_rx_entrada, False, False, 0)
        grade_enlace_rx = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_rx_entrada.add(grade_enlace_rx)

        grade_enlace_rx.attach(Gtk.Label("Enquadramento usado:"), 0, 1, 1, 1)
        self.combo_enq_rx = Gtk.ComboBoxText()
        for t in ["Contagem", "Byte Stuffing", "Bit Stuffing"]:
            self.combo_enq_rx.append_text(t)
        self.combo_enq_rx.set_active(self.combo_enq_tx.get_active())
        grade_enlace_rx.attach(self.combo_enq_rx, 1, 1, 1, 1)

        grade_enlace_rx.attach(Gtk.Label("Controle de erro usado:"), 2, 1, 1, 1)
        self.combo_err_rx = Gtk.ComboBoxText()
        for t in ["Paridade", "Checksum", "CRC", "Hamming"]:
            self.combo_err_rx.append_text(t)
        self.combo_err_rx.set_active(self.combo_err_tx.get_active())
        grade_enlace_rx.attach(self.combo_err_rx, 3, 1, 1, 1)

        botao_processar_rx = Gtk.Button(label="Processar RX")
        botao_processar_rx.connect("clicked", self.quando_clicar_processar_recepcao)
        grade_enlace_rx.attach(botao_processar_rx, 0, 2, 1, 1)

        # saída RX
        quadro_rx_saida = Gtk.Frame(label="Resultado (Rx)")
        pagina_rx.pack_start(quadro_rx_saida, True, True, 0)
        grade_rx_saida = Gtk.Grid(column_spacing=8, row_spacing=6, margin=6)
        quadro_rx_saida.add(grade_rx_saida)

        grade_rx_saida.attach(Gtk.Label("Quadro bruto:"), 0, 0, 1, 1)
        self.visao_quadro_bruto = Gtk.TextView(width_request=700, height_request=20)
        Gtk.TextView.set_pixels_above_lines(self.visao_quadro_bruto, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_quadro_bruto, Gtk.WrapMode.CHAR)
        grade_rx_saida.attach(self.visao_quadro_bruto, 1, 0, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Payload extraído:"), 0, 1, 1, 1)
        self.visao_payload_extraido = Gtk.TextView(width_request=700, height_request=20)
        Gtk.TextView.set_pixels_above_lines(self.visao_payload_extraido, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_payload_extraido, Gtk.WrapMode.CHAR)
        grade_rx_saida.attach(self.visao_payload_extraido, 1, 1, 3, 1)

        grade_rx_saida.attach(Gtk.Label("Dados finais (bits):"), 0, 2, 1, 1)
        self.visao_dados_finais_bits = Gtk.TextView(
            width_request=700, height_request=20
        )
        Gtk.TextView.set_pixels_above_lines(self.visao_dados_finais_bits, 20 / 2 - 8)
        Gtk.TextView.set_wrap_mode(self.visao_dados_finais_bits, Gtk.WrapMode.CHAR)
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

        # logs gerais
        quadro_logs = Gtk.Frame(label="Logs")
        caixa_vertical.pack_start(quadro_logs, False, False, 0)
        self.caixa_logs = Gtk.TextView(height_request=100)
        self.caixa_logs.set_editable(False)
        quadro_logs.add(self.caixa_logs)

        # variáveis
        self.ultimos_bits = ""
        self.payload_tx = ""
        self.quadro_tx = ""
        self.sinal_tx = None
        self.taxa_amostragem_tx = 1000

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

        resultado = self.modulo_tx_enlace.processar(
            self.ultimos_bits, tipo_enq, tipo_err
        )

        self.payload_tx = resultado.get("payload_protegido", "")
        self.quadro_tx = resultado.get("quadro_final", "")

        self._definir_texto_na_caixa(self.visao_payload_protegido, self.payload_tx)
        self._definir_texto_na_caixa(self.visao_quadro_final, self.quadro_tx)

        info = f"Enlace aplicado: {resultado.get('info_enquadramento')} / {resultado.get('info_erro')}"
        self._registrar_log(info)

    def quando_clicar_transmitir_sinal_fisico_modulado(self, widget):
        """Pega o payload (ou bits originais) e manda pra camada física (modulação)."""
        if not self.quadro_tx:
            self._registrar_log("Sem payload para modular.")
            return

        arr_bits = np.array([int(b) for b in self.quadro_tx])

        mod_tipo = self.combo_mod_tx.get_active_text()
        freq = converter_float_seguro(self.campo_frequencia_tx.get_text(), 1000.0)
        sigma = converter_float_seguro(self.campo_sigma.get_text(), 0.1)
        bps = converter_int_seguro(self.campo_bps_tx.get_text(), 1)
        debug = self.checkbox_debug.get_active()

        taxa = int(freq * 1000) if freq > 0 else 1000

        modulador = Modulador(
            modulacao=mod_tipo,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=taxa,
            sigma=sigma,
            debug=debug,
        )

        demodulador = Demodulador(
            modulacao=mod_tipo,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=taxa,
        )

        sinal = modulador.processar_sinal(arr_bits)

        self.sinal_tx = sinal
        self.taxa_amostragem_tx = modulador.taxa_amostragem
        self._definir_texto_na_caixa(self.visao_bits_decodificados,
            "".join(str(n) for n in list(demodulador.processar_sinal(sinal).flatten()))
        )

        self._plotar_transmissor()

        self.rotulo_amostras.set_text(str(len(sinal)))
        self._registrar_log("Sinal modulado gerado.")

    def quando_clicar_transmitir_sinal_fisico_codificado(self, widget):
        if not self.quadro_tx:
            self._registrar_log("Sem payload para codificar.")
            return

        arr_bits = np.array([int(b) for b in self.quadro_tx])

        cod_tipo = self.combo_mod_digital_tx.get_active_text()
        freq = converter_float_seguro(self.campo_frequencia_tx.get_text(), 1000.0)
        sigma = converter_float_seguro(self.campo_sigma.get_text(), 0.1)
        bps = converter_int_seguro(self.campo_bps_tx.get_text(), 1)
        debug = self.checkbox_debug.get_active()

        taxa = int(freq * 1000) if freq > 0 else 1000

        codificador = TransmissorBandaBase(
            codificacao=cod_tipo,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=taxa,
            sigma=sigma,
            debug=debug,
        )

        decodificador = Decodificador(
            codificacao=cod_tipo,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=taxa,
        )

        sinal = codificador.processar_sinal(arr_bits).flatten()

        self.sinal_tx = sinal
        self.taxa_amostragem_tx = codificador.taxa_amostragem
        self._definir_texto_na_caixa(self.visao_bits_decodificados,
            "".join(str(n) for n in list(decodificador.processar_sinal(sinal).flatten()))
        )

        self._plotar_transmissor()

        self.rotulo_amostras.set_text(str(len(sinal)))
        self._registrar_log("Sinal codificado gerado.")

    # =======================
    # Funções do RX (callbacks)
    # =======================
    def quando_clicar_processar_recepcao(self, widget):
        """Processa o quadro recebido: desenquadrar, verificar erro, retornar dados."""
        quadro = self.visao_bits_decodificados.get_buffer().get_text(
            self.visao_bits_decodificados.get_buffer().get_start_iter(),
            self.visao_bits_decodificados.get_buffer().get_end_iter(),
            True,
        ).strip()

        if not quadro:
            self._registrar_log("Quadro vazio.")
            return

        tipo_enq = self.combo_enq_rx.get_active()
        tipo_err = self.combo_err_rx.get_active()

        resultado = self.modulo_rx_enlace.processar(quadro, tipo_enq, tipo_err)

        self._definir_texto_na_caixa(
            self.visao_quadro_bruto, resultado.get("quadro_bruto", "")
        )
        self._definir_texto_na_caixa(
            self.visao_payload_extraido, resultado.get("payload_extraido", "")
        )
        self._definir_texto_na_caixa(
            self.visao_dados_finais_bits, resultado.get("dados_finais", "")
        )

        texto_final = (
            converter_bits_para_texto(resultado.get("dados_finais", ""))
            if resultado.get("dados_finais")
            else ""
        )
        self.rotulo_texto_rx.set_text(texto_final)

        self.rotulo_status_rx.set_text(resultado.get("status", ""))
        self.rotulo_detalhes_rx.set_text(resultado.get("detalhes", ""))

        self._registrar_log(f"RX processado: {resultado.get('status')}")
    # -------------------------
    # métodos auxiliares privados
    # -------------------------
    def _plotar_transmissor(self):
        bits_transmitidos = np.array(
            list(self.quadro_tx),
            dtype=int,
        )
        fig_tx = self.canvas_tx.figure
        fig_tx.clear()

        ax_enlace_tx = fig_tx.add_subplot(2, 1, 1)
        ax_enlace_tx.plot(
            np.append(bits_transmitidos, bits_transmitidos[-1]),
            drawstyle="steps-post",
        )
        ax_enlace_tx.set_title("Sinal na Camada de Enlace - Transmissor")
        ax_enlace_tx.set_xlabel("Bits")
        ax_enlace_tx.set_ylabel("Amplitude")
        ax_enlace_tx.grid()

        ax = fig_tx.add_subplot(2, 1, 2)
        tempo = np.arange(0, len(self.sinal_tx)) / self.taxa_amostragem_tx
        ax.plot(tempo, self.sinal_tx)
        ax.set_title("Sinal Modulado")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylim(-4.0, 4.0)
        ax.set_ylabel("Amplitude")
        ax.grid()
        fig_tx.tight_layout()
        self.canvas_tx.draw()
        

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
