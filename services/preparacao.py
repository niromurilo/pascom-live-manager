"""
Pascom Live Manager
Serviço de orquestração: busca a liturgia uma vez e gera os 4 arquivos da
transmissão. Único ponto de entrada da lógica de negócio — CLI e GUI
dependem só daqui, nunca uma da outra.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from shutil import copy2
from animated_lower_thirds import criar_lowers_da_liturgia, gerar_e_validar_json_dos_lowers, montar_resumo_dos_lowers
from buscar_liturgia import URL_LITURGIA, buscar_liturgia
from gerador_descricao import gerar_descricao, gerar_titulo, salvar_texto
from resultado import Resultado

PASTA_SAIDA_PADRAO = Path("output")
NOME_ARQUIVO_JSON = "animated_lower_thirds_liturgia.json"
NOME_ARQUIVO_TITULO = "titulo.txt"
NOME_ARQUIVO_DESCRICAO = "descricao.txt"
NOME_ARQUIVO_RESUMO = "resumo.txt"
CAMINHO_LOGO = Path("assets") / "logo.png"

@dataclass(frozen=True)
class ResultadoPreparacao(Resultado):
    """Resultado de preparar a transmissão inteira."""

    relatorio: str | None = None
    pasta_saida: Path | None = None


def executar_preparacao(
    nome_paroquia: str,
    celebrante: str | None,
    pasta_saida: Path = PASTA_SAIDA_PADRAO,
) -> ResultadoPreparacao:
    """Busca a liturgia uma vez e gera os 4 arquivos da transmissão.

    Não imprime nada — quem chama (CLI ou GUI) decide como exibir o
    resultado.
    """
    if not nome_paroquia:
        return ResultadoPreparacao(
            sucesso=False,
            mensagem="Nome da paróquia não informado. Defina NOME_PAROQUIA no .env ou informe manualmente.",
        )

    resultado_busca = buscar_liturgia(URL_LITURGIA)
    if not resultado_busca.sucesso:
        return ResultadoPreparacao(sucesso=False, mensagem=resultado_busca.mensagem)
    liturgia = resultado_busca.liturgia

    hoje = date.today()
    caminho_json = pasta_saida / NOME_ARQUIVO_JSON
    lowers = criar_lowers_da_liturgia(liturgia, celebrante=celebrante)

    resultado_json = gerar_e_validar_json_dos_lowers(lowers, caminho_json)
    if not resultado_json.sucesso:
        return ResultadoPreparacao(sucesso=False, mensagem=resultado_json.mensagem)

    titulo = gerar_titulo(liturgia, hoje)
    descricao = gerar_descricao(liturgia, hoje, nome_paroquia=nome_paroquia, celebrante=celebrante)
    caminho_titulo = pasta_saida / NOME_ARQUIVO_TITULO
    caminho_descricao = pasta_saida / NOME_ARQUIVO_DESCRICAO

    try:
        salvar_texto(titulo, caminho_titulo)
        salvar_texto(descricao, caminho_descricao)
    except OSError as erro:
        return ResultadoPreparacao(sucesso=False, mensagem=f"Problema ao salvar título/descrição: {erro}")

    # Copia o logo para a pasta de saída
    try:
        if CAMINHO_LOGO.exists():
            copy2(
                CAMINHO_LOGO,
                pasta_saida / CAMINHO_LOGO.name,
            )
    except OSError as erro:
        return ResultadoPreparacao(
            sucesso=False,
            mensagem=f"Problema ao copiar o logo: {erro}",
        )
    caminho_resumo = pasta_saida / NOME_ARQUIVO_RESUMO
    relatorio = "\n\n".join([
        f"TÍTULO DO VÍDEO:\n{titulo}",
        f"DESCRIÇÃO DO VÍDEO:\n{descricao}",
        f"LOWER THIRDS:\n{montar_resumo_dos_lowers(liturgia, lowers, caminho_json)}",
        f"Arquivos gerados em: {pasta_saida}/",])

    try:
        salvar_texto(relatorio, caminho_resumo)
    except OSError as erro:
        return ResultadoPreparacao(sucesso=False, mensagem=f"Problema ao salvar o relatório: {erro}")

    return ResultadoPreparacao(
        sucesso=True,
        mensagem="Transmissão preparada com sucesso!",
        relatorio=relatorio,
        pasta_saida=pasta_saida,
    )