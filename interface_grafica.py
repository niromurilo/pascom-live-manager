"""
Pascom Live Manager
Interface gráfica principal.
"""

from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from config import NOME_PAROQUIA
from services.preparacao import PASTA_SAIDA_PADRAO


TITULO_JANELA = "Pascom Live Manager"
LARGURA = 700
ALTURA = 420
PADDING = 16


class JanelaPrincipal(tk.Tk):
    """Janela principal da aplicação."""

    def __init__(self) -> None:
        super().__init__()
        self._configurar_janela()
        self._criar_variaveis()
        self._criar_widgets()

    def preparar_transmissao(self) -> None:
        """Ação temporária do botão principal."""

        messagebox.showinfo(
        title="Pascom Live Manager",
        message="Ainda não implementado.",
        )
    


    def _configurar_janela(self) -> None:
        """Configura propriedades gerais da janela."""

        self.title(TITULO_JANELA)
        self.geometry(f"{LARGURA}x{ALTURA}")
        self.minsize(LARGURA, ALTURA)

        self.columnconfigure(1, weight=1)

    def _criar_variaveis(self) -> None:
        """Cria as variáveis ligadas aos campos da interface."""

        self.celebrante_var = tk.StringVar()

        self.paroquia_var = tk.StringVar(
            value=NOME_PAROQUIA or ""
        )

        self.pasta_saida_var = tk.StringVar(
            value=str(PASTA_SAIDA_PADRAO)
        )

    def _criar_widgets(self) -> None:
        """Cria todos os widgets da janela."""

        frame = ttk.Frame(self, padding=PADDING)
        frame.grid(sticky="nsew")

        frame.columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Celebrante:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            frame,
            textvariable=self.celebrante_var,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )

        ttk.Label(
            frame,
            text="Paróquia:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            frame,
            textvariable=self.paroquia_var,
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )

        ttk.Label(
            frame,
            text="Pasta de saída:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Entry(
            frame,
            textvariable=self.pasta_saida_var,
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            pady=(0, 12),
        )
        self.botao_preparar = ttk.Button(
        self,
        text="Preparar transmissão",
        command=self.preparar_transmissao,
        )

        self.botao_preparar.grid(
        row=6,
        column=0,
        columnspan=2,
        padx=20,
        pady=(20, 0),
        sticky="ew",
        )


def main() -> None:
    """Ponto de entrada da interface."""

    app = JanelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()