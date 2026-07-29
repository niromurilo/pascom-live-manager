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
        self.configuracao = carregar_configuracao()
        self._configurar_janela()
        self._criar_variaveis()
        self._criar_widgets()

    def _atualizar_label_logo(self, tipo: str):
        caminho = getattr(self.configuracao, f'caminho_logo_{tipo}')
        label = getattr(self, f'label_logo_{tipo}')
        label.config(text=str(caminho) if caminho else "Nenhum arquivo selecionado")

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
            padding=20,
        )
        self.frame.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        
        self.frame_config = ttk.LabelFrame(
            self.frame,
            text=" Configurações da transmissão ",
            padding=15,
        )
        self.notebook = ttk.Notebook(self.frame)

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
        )
        self.frame_config.grid(
            row=0,
            column=0,
            sticky="ew",
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
            pady=(10, 0),
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
            ttk.Label(self.frame_recursos, text=label_texto + ":").grid(row=idx, column=0, sticky="w")
            label = ttk.Label(self.frame_recursos, text="", width=40)
            label.grid(row=idx, column=1, sticky="w", padx=(5, 0))
            setattr(self, f"label_logo_{tipo}", label)
            self._atualizar_label_logo(tipo)
            btn = ttk.Button(
                self.frame_recursos,
                text="Selecionar...",
                command=lambda t=tipo: self._selecionar_logo(t)
            )
            btn.grid(row=idx, column=2, padx=(5, 0))

        # Campo Preces
        ttk.Label(self.frame_recursos, text="Preces:").grid(row=3, column=0, sticky="nw", pady=(10, 0))
        self.text_preces = tk.Text(self.frame_recursos, height=4, width=40, wrap="word")
        self.text_preces.grid(row=3, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        self.text_preces.insert("1.0", self.configuracao.preces or "")
        self.text_preces.bind("<FocusOut>", self._salvar_preces)

        # Campo PIX da Paróquia
        ttk.Label(self.frame_recursos, text="PIX da Paróquia:").grid(row=4, column=0, sticky="nw", pady=(10, 0))
        self.text_pix = tk.Text(self.frame_recursos, height=2, width=40, wrap="word")
        self.text_pix.grid(row=4, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        self.text_pix.insert("1.0", self.configuracao.chave_pix or "")
        self.text_pix.bind("<FocusOut>", self._salvar_pix)
        self.btn_procurar = ttk.Button(
            self.frame_config,
            text="Procurar...",
            command=self.escolher_pasta_saida,
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
        )

        self.scroll_saida = ttk.Scrollbar(
            self.aba_relatorio,
            orient="vertical",
            command=self.texto_saida.yview,
        )

        self.texto_saida.configure(
            state="disabled",
            font=("Consolas", 10),
            yscrollcommand=self.scroll_saida.set,
        )
        self.texto_guia = tk.Text(
            self.aba_guia,
            wrap="word",
            font=("Segoe UI", 10),
            padx=10,
            pady=10,
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