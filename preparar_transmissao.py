"""
Pascom Live Manager
CLI: prepara a transmissão do dia chamando o serviço de preparação.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from config import NOME_PAROQUIA
from services.preparacao import PASTA_SAIDA_PADRAO, executar_preparacao


def parse_args() -> argparse.Namespace:
    """Lê os argumentos opcionais do script."""
    parser = argparse.ArgumentParser(
        description="Prepara todos os arquivos da transmissão a partir da liturgia do dia.",
    )
    parser.add_argument("--celebrante", help="Nome do celebrante usado no Lower 1 e na descrição.")
    parser.add_argument("--paroquia", help="Sobrepõe NOME_PAROQUIA do .env, se informado.")
    parser.add_argument("--pasta-saida", type=Path, default=PASTA_SAIDA_PADRAO, help="Pasta onde os arquivos serão gerados.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    nome_paroquia = args.paroquia or NOME_PAROQUIA
    
    resultado = executar_preparacao(
        nome_paroquia=nome_paroquia,
        celebrante=args.celebrante,
        pasta_saida=args.pasta_saida,
    )

    if not resultado.sucesso:
        print(f"❌ {resultado.mensagem}")
        return

    print(f"✅ {resultado.mensagem}\n")
    print(resultado.relatorio)

if __name__ == "__main__":
    main()