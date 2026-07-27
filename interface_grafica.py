"""
Pascom Live Manager
Interface gráfica principal.
"""

from __future__ import annotations
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
Fluxo da transmissão

1. Informe o celebrante (opcional).

2. Confira o nome da paróquia.

3. Escolha a pasta onde os arquivos serão gerados.

4. Clique em "Preparar transmissão".

5. Aguarde a mensagem de sucesso.

6. No OBS, abra o Animated Lower Thirds.

7. Clique em Import.

8. Selecione:
animated_lower_thirds_liturgia.json

9. Utilize:
• titulo.txt
• descricao.txt

10. Consulte a aba Relatório para revisar todo o conteúdo gerado.
"""

class JanelaPrincipal(tk.Tk):
    """Janela principal."""

    def __init__(self) -> None:
        super().__init__()

        self._configurar_janela()
        self._criar_variaveis()
        self._criar_widgets()

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
            row=1,
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

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

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