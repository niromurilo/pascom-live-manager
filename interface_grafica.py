"""
Pascom Live Manager
Interface gráfica principal.
"""
from __future__ import annotations
from paroquia_config import carregar_configuracao, salvar_configuracao, ConfiguracaoParoquia
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from config import NOME_PAROQUIA
from services.preparacao import (
    PASTA_SAIDA_PADRAO,
    executar_preparacao,
)

class Tema:
    """Paleta de cores e fontes centralizada do tema escuro.

    Único lugar que declara cor ou fonte em todo o arquivo — qualquer
    widget que precisar de uma dessas propriedades lê daqui, nunca
    declara um valor solto (objetivo de centralização).
    """

    FUNDO = "#1e1f26"
    FUNDO_PAINEL = "#262832"
    FUNDO_CAMPO = "#2d3040"
    BORDA = "#3a3d4d"

    TEXTO = "#e8e8ea"
    TEXTO_SECUNDARIO = "#9a9db0"

    DESTAQUE = "#4a7fc9"
    DESTAQUE_HOVER = "#5c8fd6"

    ABA_ATIVA = "#2d3040"
    ABA_INATIVA = "#1e1f26"

    FONTE_PADRAO = ("Segoe UI", 11)
    FONTE_SECAO = ("Segoe UI", 13, "bold")
    FONTE_BOTAO = ("Segoe UI", 11, "bold")
    FONTE_BOTAO_PRINCIPAL = ("Segoe UI", 13, "bold")
    FONTE_ABA = ("Segoe UI", 12, "bold")
    FONTE_MONO = ("Consolas", 11)

TITULO_JANELA = "Pascom Live Manager"
LARGURA = 700
ALTURA = 550
GUIA_OPERACIONAL = """
Bem-vindo ao Pascom Live Manager!

Este programa automatiza a preparação dos arquivos utilizados na transmissão da Santa Missa.

Primeira utilização

Antes da primeira transmissão, configure os recursos da sua paróquia na seção Recursos da Paróquia.

Selecione:

• Logo PIX
• Logo Leituras
• Logo Celebrante

Depois, preencha o campo Preces com o texto padrão utilizado pela sua paróquia.

Essas configurações são salvas automaticamente e não precisam ser configuradas novamente, exceto quando desejar alterá-las.

Preparando uma transmissão
Informe o nome do celebrante (opcional).
Confira o nome da paróquia.
Escolha a pasta onde os arquivos serão salvos.
Clique em Preparar transmissão.

Após alguns segundos, todos os arquivos necessários serão gerados automaticamente.

Arquivos gerados

O programa gera automaticamente:

• Título da transmissão
• Descrição para YouTube/Facebook
• Lower Thirds (JSON)
• Resumo da transmissão

Também copia para a pasta de saída:

• Logo PIX
• Logo Leituras
• Logo Celebrante

Alterando configurações

Sempre que desejar alterar algum recurso:

• Clique em Selecionar... ao lado do logo correspondente.

Para alterar as preces:

• Edite o campo Preces.

Todas as alterações são salvas automaticamente.

Em caso de erro

Verifique:

• Se há conexão com a internet.
• Se os logos selecionados ainda existem no computador.
• A mensagem exibida na aba Relatório.

Dica: Após gerar a transmissão, clique em Abrir pasta para acessar rapidamente todos os arquivos gerados.
"""

class JanelaPrincipal(tk.Tk):
    """Janela principal."""

    def __init__(self) -> None:
        super().__init__()
        self._configurar_estilo()
        self.configuracao = carregar_configuracao()
        self._configurar_janela()
        self._criar_variaveis()
        self._criar_widgets()

    def _configurar_estilo(self) -> None:
        """Configura o tema escuro da interface, usando ttk.Style sempre que possível."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TLabel",
            font=Tema.FONTE_PADRAO,
            padding=3,
            background=Tema.FUNDO_PAINEL,
            foreground=Tema.TEXTO,
        )
        estilo.configure("TEntry", font=Tema.FONTE_PADRAO, padding=3)

        estilo.configure(
            "TButton",
            font=Tema.FONTE_BOTAO,
            padding=8,
            background=Tema.FUNDO_CAMPO,
            foreground=Tema.TEXTO,
            borderwidth=1,
            relief="flat",
        )
        estilo.map(
            "TButton",
            background=[("active", Tema.DESTAQUE_HOVER), ("!active", Tema.FUNDO_CAMPO)],
            foreground=[("active", Tema.TEXTO), ("!active", Tema.TEXTO)],
        )

        estilo.configure(
            "Principal.TButton",
            font=Tema.FONTE_BOTAO_PRINCIPAL,
            padding=10,
            background=Tema.DESTAQUE,
            foreground=Tema.TEXTO,
            borderwidth=0,
            relief="flat",
        )
        estilo.map(
            "Principal.TButton",
            background=[("active", Tema.DESTAQUE_HOVER), ("!active", Tema.DESTAQUE)],
        )

        estilo.configure(
            "TLabelFrame.Label",
            font=Tema.FONTE_SECAO,
            padding=8,
            background=Tema.FUNDO_PAINEL,
            foreground=Tema.TEXTO,
        )
        estilo.configure(
            "TLabelFrame",
            padding=18,
            background=Tema.FUNDO_PAINEL,
            borderwidth=1,
            relief="groove",
        )

        # Abas maiores e mais legíveis — objetivo 8
        estilo.configure("TNotebook", tabposition="n", background=Tema.FUNDO, borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            font=Tema.FONTE_ABA,
            padding=[24, 12],
            background=Tema.ABA_INATIVA,
            foreground=Tema.TEXTO_SECUNDARIO,
            borderwidth=0,
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", Tema.ABA_ATIVA), ("!selected", Tema.ABA_INATIVA)],
            foreground=[("selected", Tema.TEXTO), ("!selected", Tema.TEXTO_SECUNDARIO)],
        )

        estilo.configure("TFrame", background=Tema.FUNDO)
        self.configure(bg=Tema.FUNDO)

    def _atualizar_label_logo(self, tipo: str):
        import os
        caminho = getattr(self.configuracao, f'caminho_logo_{tipo}')
        label = getattr(self, f'label_logo_{tipo}')
        if caminho:
            nome = os.path.basename(str(caminho))
            label.config(text=f'✔ {nome}')
            self._set_tooltip(label, str(caminho))
        else:
            label.config(text="Nenhum arquivo selecionado")
            self._set_tooltip(label, "")

    def _set_tooltip(self, widget, text):
        # Simples tooltip usando bind
        def on_enter(event):
            if text:
                self._tooltip = tk.Toplevel(widget)
                self._tooltip.wm_overrideredirect(True)
                x = widget.winfo_rootx() + 20
                y = widget.winfo_rooty() + 20
                self._tooltip.wm_geometry(f"+{x}+{y}")
                label = tk.Label(self._tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 9))
                label.pack()
        def on_leave(event):
            if hasattr(self, '_tooltip'):
                self._tooltip.destroy()
                self._tooltip = None
        widget.unbind("<Enter>")
        widget.unbind("<Leave>")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _selecionar_logo(self, tipo: str):
        arquivo = filedialog.askopenfilename(
            title=f"Selecione o logo {tipo.capitalize()}",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            setattr(self.configuracao, f'caminho_logo_{tipo}', Path(arquivo))
            salvar_configuracao(self.configuracao)
            self._atualizar_label_logo(tipo)

    def _salvar_preces(self, event=None):
        self.configuracao.preces = self.text_preces.get("1.0", "end-1c")
        salvar_configuracao(self.configuracao)

    def _salvar_pix(self, event=None):
        self.configuracao.chave_pix = self.text_pix.get("1.0", "end-1c")
        salvar_configuracao(self.configuracao)

    def preparar_transmissao(self) -> None:
        """Executa a preparação da transmissão."""

        nome_paroquia = self.paroquia_var.get().strip()
        celebrante = self.celebrante_var.get().strip() or None
        self.btn_preparar.config(
            state="disabled",
            text="Preparando...",
        )

        self.update_idletasks()
        resultado = executar_preparacao(
            nome_paroquia=nome_paroquia,
            celebrante=celebrante,
            pasta_saida=Path(self.pasta_saida_var.get()),
        )

        if resultado.sucesso:
            relatorio = resultado.relatorio or ""

            arquivos = (
                "\n\n"
                "Arquivos gerados\n"
                "────────────────────────\n"
                "📄 titulo.txt\n"
                "📄 descricao.txt\n"
                "📄 resumo.txt\n"
                "📄 animated_lower_thirds_liturgia.json\n"
                "📄 logo padre\n"
                "📄 logo leituras\n"
                "📄 logo pix\n\n"
            )

            self.atualizar_saida(relatorio + arquivos)

            messagebox.showinfo(
                "Pascom Live Manager",
                resultado.mensagem,
            )

        else:
            self.atualizar_saida("")

            messagebox.showerror(
                "Erro",
                resultado.mensagem,
            )
        self.btn_preparar.config(
            state="normal",
            text="Preparar transmissão",
        )

    def escolher_pasta_saida(self) -> None:
        """Permite escolher a pasta onde os arquivos serão gerados."""

        pasta = filedialog.askdirectory(
            title="Escolha a pasta de saída",
            initialdir=self.pasta_saida_var.get(),
        )

        if pasta:
            self.pasta_saida_var.set(pasta)

    def abrir_pasta_saida(self) -> None:
        """Abre a pasta onde os arquivos são gerados."""

        pasta = Path(self.pasta_saida_var.get())

        if not pasta.exists():
            messagebox.showwarning(
                "Pasta inexistente",
                "A pasta de saída ainda não existe.",
            )
            return

        os.startfile(pasta)

    def atualizar_saida(self, texto: str) -> None:
        """Atualiza a área de saída."""

        self.texto_saida.config(state="normal")

        self.texto_saida.delete(
            "1.0",
            tk.END,
        )

        self.texto_saida.insert(
            tk.END,
            texto,
        )

    def _configurar_janela(self) -> None:
        """Configura a janela."""

        self.title(TITULO_JANELA)
        self.geometry(f"{LARGURA}x{ALTURA}")
        self.minsize(LARGURA, ALTURA)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _criar_variaveis(self) -> None:
        """Cria as variáveis."""

        self.celebrante_var = tk.StringVar()

        self.paroquia_var = tk.StringVar(
            value=NOME_PAROQUIA or ""
        )

        self.pasta_saida_var = tk.StringVar(
            value=str(PASTA_SAIDA_PADRAO)
        )

    def _criar_widgets(self) -> None:
        """Cria os componentes da tela."""

        self.frame = ttk.Frame(
            self,
            padding=(8, 8, 8, 0),
        )
        self.frame.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        
        self.frame_config = ttk.LabelFrame(
            self.frame,
            text=" Configurações da transmissão ",
            padding=20,
        )
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.enable_traversal()

        self.notebook.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(15, 0),
        )
        self.aba_relatorio = ttk.Frame(self.notebook)
        self.aba_guia = ttk.Frame(self.notebook)

        self.aba_relatorio.columnconfigure(0, weight=1)
        self.aba_relatorio.rowconfigure(0, weight=1)

        self.aba_guia.columnconfigure(0, weight=1)
        self.aba_guia.rowconfigure(0, weight=1)

        self.notebook.add(
            self.aba_relatorio,
            text="Relatório",
        )

        self.notebook.add(
            self.aba_guia,
            text="Guia Operacional",
        )
        self.frame_config.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 6),
        )
        self.frame_config.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 6),
        )

        self.frame_recursos = ttk.LabelFrame(
            self.frame,
            text=" Recursos da Paróquia ",
            padding=20,
        )
        self.frame_recursos.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 6),
        )

        self.notebook.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(15, 0),
        )

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.frame_config.columnconfigure(1, weight=1)

        # Celebrante

        ttk.Label(
            self.frame_config,
            text="Celebrante:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            self.frame_config,
            textvariable=self.celebrante_var,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )
        # Paróquia

        ttk.Label(
            self.frame_config,
            text="Paróquia:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            self.frame_config,
            textvariable=self.paroquia_var,
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )

        # Pasta

        ttk.Label(
            self.frame_config,
            text="Pasta de saída:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        self.entry_pasta_saida = ttk.Entry(
            self.frame_config,
            textvariable=self.pasta_saida_var,
        )

        self.entry_pasta_saida.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )
        self.frame_recursos = ttk.LabelFrame(
            self.frame,
            text=" Recursos da Paróquia ",
            padding=15,
        )

        self.frame_recursos.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(15, 0),
        )
                # Widgets para Logos
        tipos = [("pix", "Logo PIX"), ("leituras", "Logo Leituras"), ("celebrante", "Logo Celebrante")]
        for idx, (tipo, label_texto) in enumerate(tipos):
            ttk.Label(self.frame_recursos, text=label_texto + ":").grid(row=idx, column=0, sticky="w", pady=(0, 6))
            label = ttk.Label(self.frame_recursos, text="", width=40)
            label.grid(row=idx, column=1, sticky="w", padx=(5, 0), pady=(0, 6))
            setattr(self, f"label_logo_{tipo}", label)
            self._atualizar_label_logo(tipo)
            btn = ttk.Button(
                self.frame_recursos,
                text="Selecionar...",
                command=lambda t=tipo: self._selecionar_logo(t)
            )
            btn.grid(row=idx, column=2, padx=(5, 0), pady=(0, 6))

        # Campo Preces
        ttk.Label(self.frame_recursos, text="Preces:").grid(row=3, column=0, sticky="nw", pady=(10, 0))
        self.text_preces = tk.Text(self.frame_recursos, height=7, width=40, wrap="word", font=("Segoe UI", 12), padx=10, pady=8, bd=1, relief="solid", bg="#23272e", fg="#f0f0f0", insertbackground="#f0f0f0")
        self.text_preces.grid(row=3, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        self.text_preces.insert("1.0", self.configuracao.preces or "")
        self.text_preces.bind("<FocusOut>", self._salvar_preces)

        # Campo PIX da Paróquia
        ttk.Label(self.frame_recursos, text="PIX da Paróquia:").grid(row=4, column=0, sticky="nw", pady=(10, 0))
        self.text_pix = tk.Text(self.frame_recursos, height=2, width=40, wrap="word", font=("Segoe UI", 11), padx=8, pady=6, bd=1, relief="solid", bg="#f7f7f7")
        self.text_pix.grid(row=4, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        self.text_pix.insert("1.0", self.configuracao.chave_pix or "")
        self.text_pix.bind("<FocusOut>", self._salvar_pix)
        self.btn_procurar = ttk.Button(
            self.frame_config,
            text="Procurar...",
            command=self.escolher_pasta_saida,
            width=12,
            style="Principal.TButton"
        )

        self.btn_procurar.grid(
            row=2,
            column=2,
            padx=(10, 0),
            pady=(0, 12),
        )
        # Botão

        self.btn_preparar = ttk.Button(
            self.frame_config,
            text="Preparar transmissão",
            command=self.preparar_transmissao,
            width=22,
            style="Principal.TButton"
        )

        self.btn_preparar.grid(
            row=3,
            column=0,
            columnspan=1,
            sticky="ew",
            padx=(0,5),
        )
        #botão abrir pasta
        self.btn_abrir_pasta = ttk.Button(
            self.frame_config,
            text="Abrir pasta",
            command=self.abrir_pasta_saida,
            width=18,
            style="Principal.TButton"
        )
        self.btn_abrir_pasta.grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(5,0),
        )
        # Área de saída

        self.texto_saida = tk.Text(
            self.aba_relatorio,
            height=12,
            wrap="word",
            font=("Consolas", 11),
            padx=16,
            pady=10,
            bd=1,
            relief="solid",
            bg="#f4f6fa",
            highlightthickness=1,
            highlightbackground="#bfc9d9",
            highlightcolor="#bfc9d9"
        )

        self.scroll_saida = ttk.Scrollbar(
            self.aba_relatorio,
            orient="vertical",
            command=self.texto_saida.yview,
        )

        self.texto_saida.configure(
            state="disabled",
            yscrollcommand=self.scroll_saida.set,
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc"
        )
        self.texto_guia = tk.Text(
            self.aba_guia,
            wrap="word",
            font=("Segoe UI", 12),
            padx=20,
            pady=14,
            bd=1,
            relief="solid",
            bg="#f4f6fa",
            highlightthickness=1,
            highlightbackground="#bfc9d9",
            highlightcolor="#bfc9d9"
        )
        self.texto_guia.insert(
            "1.0",
            GUIA_OPERACIONAL,
        )
        self.texto_guia.config(state="disabled")

        self.texto_guia.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        self.texto_saida.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.scroll_saida.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        
def main() -> None:
    """Ponto de entrada."""

    app = JanelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()