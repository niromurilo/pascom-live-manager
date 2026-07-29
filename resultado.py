"""
Pascom Live Manager
Classe base para objetos de resultado — usada no lugar de exceções soltas
ou retornos silenciosos (None/bool), para que CLI e GUI decidam como
apresentar sucesso e erro, sem duplicar essa estrutura em cada módulo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resultado:
    """Resultado base de uma operação: se deu certo, e uma mensagem pra exibir.

    Módulos que precisam devolver dado extra junto do resultado (a liturgia
    buscada, o caminho de saída) devem herdar dessa classe, não recriar
    sucesso/mensagem do zero.
    """

    sucesso: bool
    mensagem: str