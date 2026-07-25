"""
Pascom Live Manager
Interface gráfica principal.
"""

from __future__ import annotations
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import NOME_PAROQUIA
from services.preparacao import (
    PASTA_SAIDA_PADRAO,
    executar_preparacao,
)

TITULO_JANELA = "Pascom Live Manager"
LARGURA = 700
ALTURA = 420


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

        resultado = executar_preparacao(
            nome_paroquia=nome_paroquia,
            celebrante=celebrante,
            pasta_saida=Path(self.pasta_saida_var.get()),
        )

        if resultado.sucesso:
            self.atualizar_saida(resultado.relatorio or "")

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
    def escolher_pasta_saida(self) -> None:
        """Permite escolher a pasta onde os arquivos serão gerados."""

        pasta = filedialog.askdirectory(
            title="Escolha a pasta de saída",
            initialdir=self.pasta_saida_var.get(),
        )

        if pasta:
            self.pasta_saida_var.set(pasta)

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

        self.texto_saida.config(state="disabled")

    def _configurar_janela(self) -> None:
        """Configura a janela."""

        self.title(TITULO_JANELA)
        self.geometry(f"{LARGURA}x{ALTURA}")
        self.minsize(LARGURA, ALTURA)

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

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.rowconfigure(4, weight=1)

        # Celebrante

        ttk.Label(
            self.frame,
            text="Celebrante:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            self.frame,
            textvariable=self.celebrante_var,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )

        # Paróquia

        ttk.Label(
            self.frame,
            text="Paróquia:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            self.frame,
            textvariable=self.paroquia_var,
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )

        # Pasta

        ttk.Label(
            self.frame,
            text="Pasta de saída:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        self.entry_pasta_saida = ttk.Entry(
            self.frame,
            textvariable=self.pasta_saida_var,
        )

        self.entry_pasta_saida.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )
        self.btn_procurar = ttk.Button(
            self.frame,
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
            self.frame,
            text="Preparar transmissão",
            command=self.preparar_transmissao,
        )

        self.btn_preparar.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(20, 0),
        )
        # Área de saída

        self.texto_saida = tk.Text(
            self.frame,
            height=12,
            wrap="word",
        )

        self.scroll_saida = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.texto_saida.yview,
        )

        self.texto_saida.configure(
            yscrollcommand=self.scroll_saida.set,
        )

        self.texto_saida.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=(20, 0),
        )

        self.scroll_saida.grid(
            row=4,
            column=2,
            sticky="ns",
            pady=(20, 0),
        )

        self.texto_saida.config(state="disabled")

def main() -> None:
    """Ponto de entrada."""

    app = JanelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()