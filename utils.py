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
    Retorna a pasta assets — recurso empacotado pelo PyInstaller.

    Rodando como .exe, assets fica dentro de _internal/, não ao lado do
    executável — por isso usa sys._MEIPASS aqui, não pasta_projeto().
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "assets"
    return pasta_projeto() / "assets"


def caminho_output() -> Path:
    """
    Retorna a pasta onde os arquivos gerados são salvos.

    Empacotado, usa Documentos do usuário (mesma lógica de
    pasta_dados_usuario) — escrever dentro da pasta de instalação pode
    falhar por permissão (ex: Program Files), e escrever dentro de
    _internal misturaria dado gerado com recurso empacotado, somente leitura.
    """
    if getattr(sys, "frozen", False):
        pasta = Path.home() / "Documents" / "Pascom Live Manager" / "output"
    else:
        pasta = pasta_projeto() / "output"

    pasta.mkdir(parents=True, exist_ok=True)
    return pasta

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
