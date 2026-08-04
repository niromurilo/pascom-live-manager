"""
Funções utilitárias do projeto.
"""

from __future__ import annotations

import sys
from pathlib import Path


def pasta_projeto() -> Path:
    """
    Retorna a pasta raiz do projeto.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent


def caminho_assets() -> Path:
    """
    Retorna a pasta assets.
    """

    return pasta_projeto() / "assets"


def caminho_output() -> Path:
    """
    Retorna a pasta output.
    """

    return pasta_projeto() / "output"

def pasta_dados_usuario() -> Path:
    """
    Retorna a pasta onde serão armazenados os dados do usuário.

    Durante o desenvolvimento:
        <projeto>/dados

    No executável:
        Documentos/Pascom Live Manager
    """

    if getattr(sys, "frozen", False):
        documentos = Path.home() / "Documents" / "Pascom Live Manager"
        documentos.mkdir(parents=True, exist_ok=True)
        return documentos

    pasta = pasta_projeto() / "dados"
    pasta.mkdir(exist_ok=True)
    return pasta