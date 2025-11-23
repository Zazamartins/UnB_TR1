import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import numpy as np
from CamadaFisica import (
    Modulador,
    Demodulador,
    TransmissorBandaBase,
    Decodificador,
    CODIFICACOES,
    MODULACOES,
)
from CamadaEnlace import TransmissorEnlace, ReceptorEnlace

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class JanelaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__(title=" Transmissor ")
        self.set_default_size(500, 400)

        layout = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.add(layout)

        # Entrada da mensagem
        self.entry_msg = Gtk.Entry()
        self.entry_msg.set_placeholder_text("Digite a mensagem")
        layout.pack_start(self.entry_msg, False, False, 0)

        # Caixa de modulação
        self.combo_mod = Gtk.ComboBoxText()
        for m in MODULACOES:
            self.combo_mod.append_text(m)
        self.combo_mod.set_active(0)
        layout.pack_start(self.combo_mod, False, False, 0)

        # Caixa de codificacao
        self.combo_cod = Gtk.ComboBoxText()
        for c in CODIFICACOES:
            self.combo_cod.append_text(c)
        self.combo_cod.set_active(0)
        layout.pack_start(self.combo_cod, False, False, 0)

        # Caixa de tipo de enquadramento
        # 0:Contagem, 1:Byte, 2:Bit
        self.combo_enq = Gtk.ComboBoxText()
        self.combo_enq.append_text("Contagem")
        self.combo_enq.append_text("Byte")
        self.combo_enq.append_text("Bit")
        self.combo_enq.set_active(0)
        layout.pack_start(self.combo_enq, False, False, 0)

        # Caixa tipo de detecção/correção de erro
        # 0:Paridade, 1:Checksum, 2:CRC, 3:Hamming
        self.combo_erro = Gtk.ComboBoxText()
        self.combo_erro.append_text("Paridade")
        self.combo_erro.append_text("Checksum")
        self.combo_erro.append_text("CRC")
        self.combo_erro.append_text("Hamming")
        self.combo_erro.set_active(0)
        layout.pack_start(self.combo_erro, False, False, 0)
        
        # Caixa tamanho do EDC
        self.combo_edc = Gtk.ComboBoxText()
        self.combo_edc.append_text("8 bits")
        self.combo_edc.append_text("16 bits")
        self.combo_edc.append_text("32 bits")
        self.combo_edc.set_active(0)
        layout.pack_start(self.combo_edc, False, False, 0)
        
        # Caixa tamanho maximo do quadro
        self.combo_tam_quadro = Gtk.ComboBoxText()
        self.combo_tam_quadro.append_text("128 bytes")
        self.combo_tam_quadro.append_text("256 bytes")
        self.combo_tam_quadro.append_text("512 bytes")
        self.combo_tam_quadro.append_text("1024 bytes")
        self.combo_tam_quadro.set_active(0)

        # Frequência
        self.entry_freq = Gtk.Entry()
        self.entry_freq.set_placeholder_text("Frequência da portadora (ex: 1000)")
        self.entry_freq.set_text("1000")
        layout.pack_start(self.entry_freq, False, False, 0)

        # Bits por símbolo
        self.entry_bps = Gtk.Entry()
        self.entry_bps.set_placeholder_text("Bits por símbolo (ex: 1,2,4)")
        self.entry_bps.set_text("4")
        layout.pack_start(self.entry_bps, False, False, 0)

        # Botão Transmitir
        self.btn = Gtk.Button(label="Transmitir")
        self.btn.connect("clicked", self.on_transmitir)
        layout.pack_start(self.btn, False, False, 0)

        # Resultado
        self.output = Gtk.Label(label="")
        layout.pack_start(self.output, False, False, 0)

        self.sinal_modulado = None
        self.sinal_codificado = None

        self.connect("delete-event", Gtk.main_quit)
        self.connect("destroy", Gtk.main_quit)

    def on_transmitir(self, widget):
        mensagem = self.entry_msg.get_text()
        tipo_mod = self.combo_mod.get_active_text()
        tipo_cod = self.combo_cod.get_active_text()
        freq = float(self.entry_freq.get_text())
        bps = int(self.entry_bps.get_text())

        # CONVERTE MENSAGEM PARA BITS
        bits = np.array(
            [int(b) for b in "".join(format(ord(c), "08b") for c in mensagem)]
        )

        self.mod = Modulador(
            modulacao=tipo_mod,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=1000 * freq,
            debug=False,
        )

        self.demod = Demodulador(
            modulacao=tipo_mod,
            frequencia_portadora=freq,
            bits_por_simbolo=bps,
            taxa_amostragem=1000 * freq,
        )

        self.cod = TransmissorBandaBase(
            codificacao=tipo_cod,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=1000 * freq,
            debug=False,
        )

        self.decod = Decodificador(
            codificacao=tipo_cod,
            bits_por_simbolo=bps,
            frequencia_de_simbolo=freq,
            taxa_amostragem=1000 * freq,
        )

        self.enlace_tx = TransmissorEnlace()
        self.enlace_rx = ReceptorEnlace()

        bits_transmitidos = np.array(
            list(
                self.enlace_tx.processar(
                    "".join(str(x) for x in bits.flatten()),
                    tipo_enquadramento=self.combo_enq.get_active(),
                    tipo_erro=self.combo_erro.get_active(),
                    # tamanho_edc=self.combo_edc.get_active(),
                    # tamanho_maximo_quadro=self.combo_tam_quadro.get_active(),
                )["quadro_final"]
            ),
            dtype=int,
        )
        bits_codificados = self.cod.processar_sinal(bits_transmitidos).flatten()
        bits_modulados = self.mod.processar_sinal(bits_transmitidos).flatten()
        bits_decodificados = self.decod.processar_sinal(bits_codificados).flatten()
        bits_demodulados = self.demod.processar_sinal(bits_modulados).flatten()
        bits_recebidos = np.array(
            list(
                self.enlace_rx.processar(
                    "".join(str(x) for x in bits_demodulados),
                    tipo_enquadramento=self.combo_enq.get_active(),
                    tipo_erro=self.combo_erro.get_active(),
                    # tamanho_edc=self.combo_edc.get_active(),
                    # tamanho_maximo_quadro=self.combo_tam_quadro.get_active(),
                )["dados_finais"]
            ),
            dtype=int,
        )

        self.output.set_text(f"Sinal transmitido com {len(bits_modulados)} amostras!")

        fig_tx = Figure(figsize=(12, 12), dpi=100)
        fig_tx.tight_layout(pad=3.0)

        ax_enlace_tx = fig_tx.add_subplot(3, 1, 1)
        ax_enlace_tx.plot(
            np.append(bits_transmitidos, bits_transmitidos[-1]),
            drawstyle="steps-post",
        )
        ax_enlace_tx.set_title("Sinal na Camada de Enlace - Transmissor")
        ax_enlace_tx.set_xlabel("Bits")
        ax_enlace_tx.set_ylabel("Amplitude")
        ax_enlace_tx.grid()

        ax = fig_tx.add_subplot(3, 1, 2)
        tempo = np.arange(0, len(bits_modulados)) / self.mod.taxa_amostragem
        ax.plot(tempo, bits_modulados)
        ax.set_title("Sinal Modulado")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylim(-4.0, 4.0)
        ax.set_ylabel("Amplitude")
        ax.grid()

        ax3 = fig_tx.add_subplot(3, 1, 3)
        tempo3 = np.arange(0, len(bits_codificados)) / self.cod.taxa_amostragem
        ax3.plot(tempo3, bits_codificados)
        ax3.set_title("Sinal Codificado")
        ax3.set_xlabel("Tempo (s)")
        ax3.set_ylim(-4.0, 4.0)
        ax3.set_ylabel("Amplitude")
        ax3.grid()

        subwindow_tx = Gtk.Window()
        subwindow_tx.set_title("Sinais da Transmissão")
        subwindow_tx.set_default_size(1500, 1200)

        subsubwindow_tx = Gtk.ScrolledWindow()
        subsubwindow_tx.set_border_width(2)

        subwindow_tx.add(subsubwindow_tx)
        subwindow_tx.show_all()

        self.canvas_tx = FigureCanvas(fig_tx)
        subsubwindow_tx.add(self.canvas_tx)
        subsubwindow_tx.show_all()

        fig_rx = Figure(figsize=(12, 12), dpi=100)
        fig_rx.tight_layout(pad=3.0)

        ax_enlace_rx = fig_rx.add_subplot(3, 1, 1)
        ax_enlace_rx.plot(
            np.append(bits_recebidos, bits_recebidos[-1]),
            drawstyle="steps-post",
        )
        ax_enlace_rx.set_title("Sinal na Camada de Enlace - Receptor")
        ax_enlace_rx.set_xlabel("Bits")
        ax_enlace_rx.set_ylabel("Amplitude")
        ax_enlace_rx.text(
            0.5,
            -0.1,
            "Bits Recebidos (Hex): 0x"
            + "".join(
                format(
                    int("".join(str(b) for b in bits_recebidos[i : i + 8]), 2), "02X"
                )
                for i in range(0, len(bits_recebidos), 8)
                # caracteres ascii recebidos
            )
            + " -> "
            + "".join(
                chr(int("".join(str(b) for b in bits_recebidos[i : i + 8]), 2))
                for i in range(0, len(bits_recebidos), 8)
            ),
            transform=ax_enlace_rx.transAxes,
            fontsize=10,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
        )
        ax_enlace_rx.grid()

        ax2 = fig_rx.add_subplot(3, 1, 2)
        ax2.plot(
            np.append(bits_demodulados, bits_demodulados[-1]),
            drawstyle="steps-post",
        )
        ax2.set_title("Sinal Demodulado")
        ax2.set_xlabel("Bits")
        ax2.set_ylabel("Amplitude")
        ax2.text(
            0.5,
            -0.1,
            "Bits Demodulados (Hex): 0x"
            + "".join(
                format(
                    int("".join(str(b) for b in bits_demodulados[i : i + 8]), 2), "02X"
                )
                for i in range(0, len(bits_demodulados), 8)
            ),
            transform=ax2.transAxes,
            fontsize=10,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
        )
        ax2.grid()

        ax4 = fig_rx.add_subplot(3, 1, 3)
        ax4.plot(
            np.append(bits_decodificados, bits_decodificados[-1]),
            drawstyle="steps-post",
        )
        ax4.set_title("Sinal Decodificado")
        ax4.set_xlabel("Bits")
        ax4.set_ylabel("Amplitude")
        ax4.text(
            0.5,
            -0.1,
            "Bits Decodificados (Hex): 0x"
            + "".join(
                format(
                    int("".join(str(b) for b in bits_decodificados[i : i + 8]), 2),
                    "02X",
                )
                for i in range(0, len(bits_decodificados), 8)
            ),
            transform=ax4.transAxes,
            fontsize=10,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
        )
        ax4.grid()

        subwindow_rx = Gtk.Window()
        subwindow_rx.set_title("Sinais da Transmissão")
        subwindow_rx.set_default_size(1500, 1200)

        subsubwindow_rx = Gtk.ScrolledWindow()
        subsubwindow_rx.set_border_width(2)

        subwindow_rx.add(subsubwindow_rx)
        subwindow_rx.show_all()

        self.canvas_rx = FigureCanvas(fig_rx)
        subsubwindow_rx.add(self.canvas_rx)
        subsubwindow_rx.show_all()


win = JanelaPrincipal()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
