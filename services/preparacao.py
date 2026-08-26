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
from animated_lower_thirds import (
    PAINEL_LEITURAS,
    PAINEL_PIX,
    PAINEL_TITULO,
    criar_lowers_da_liturgia,
    gerar_e_validar_json_dos_lowers,
    montar_resumo_dos_lowers,
)
from buscar_liturgia import URL_LITURGIA, buscar_liturgia
from gerador_descricao import gerar_descricao, gerar_titulo, salvar_texto
from paroquia_config import ConfiguracaoParoquia, carregar_configuracao
from resultado import Resultado
from utils import caminho_output

PASTA_SAIDA_PADRAO = caminho_output()
NOME_ARQUIVO_JSON = "animated_lower_thirds_liturgia.json"
NOME_ARQUIVO_TITULO = "titulo.txt"
NOME_ARQUIVO_DESCRICAO = "descricao.txt"
NOME_ARQUIVO_RESUMO = "resumo.txt"

LOGOS_CONFIGURADOS = (
    ("Logo PIX", "caminho_logo_pix", "logo_pix", PAINEL_PIX),
    ("Logo Leituras", "caminho_logo_leituras", "logo_leituras", PAINEL_LEITURAS),
    ("Logo Celebrante", "caminho_logo_celebrante", "logo_celebrante", PAINEL_TITULO),
)
LOGOS_GERADOS_ANTIGOS = ("logo_pix", "logo_leituras", "logo_celebrante", "logo_padre")
PAINEL_POR_LOGO_GERADO = {
    "logo_pix": PAINEL_PIX,
    "logo_leituras": PAINEL_LEITURAS,
    "logo_celebrante": PAINEL_TITULO,
}
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
    if liturgia is None:
        return ResultadoPreparacao(sucesso=False, mensagem="Liturgia não retornou dados para preparar a transmissão.")

    hoje = date.today()
    caminho_json = pasta_saida / NOME_ARQUIVO_JSON
    config = carregar_configuracao()
    lowers = criar_lowers_da_liturgia(
        liturgia,
        celebrante=celebrante,
        chave_pix=config.chave_pix,
        preces=config.preces,
    )
    try:
        logos_copiados = copiar_logos_configurados(config, pasta_saida)
    except (OSError, ValueError) as erro:
        return ResultadoPreparacao(
            sucesso=False,
            mensagem=f"Problema ao copiar os logos: {erro}",
        )

    logos_por_painel = montar_logos_por_painel(logos_copiados)
    resultado_json = gerar_e_validar_json_dos_lowers(
        lowers,
        caminho_json,
        logos_por_painel=logos_por_painel,
    )
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
    caminho_resumo = pasta_saida / NOME_ARQUIVO_RESUMO
    relatorio = "\n\n".join(
        [
            f"TÍTULO DO VÍDEO:\n{titulo}",
            f"DESCRIÇÃO DO VÍDEO:\n{descricao}",
            f"LOWER THIRDS:\n{montar_resumo_dos_lowers(liturgia, lowers, caminho_json)}",
            f"LOGOS COPIADOS:\n{montar_resumo_dos_logos(logos_copiados)}",
            f"Arquivos gerados em: {pasta_saida}/",
        ]
    )

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


def copiar_logos_configurados(configuracao: ConfiguracaoParoquia, pasta_saida: Path) -> list[Path]:
    """Copia para a saída os logos escolhidos na configuração da paróquia."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    origens_configuradas = _origens_de_logos_configuradas(configuracao)
    limpar_logos_gerados_antigos(pasta_saida, preservar=origens_configuradas)
    destinos: list[Path] = []

    for rotulo, atributo, nome_saida, _painel in LOGOS_CONFIGURADOS:
        origem = getattr(configuracao, atributo)
        if origem is None:
            continue

        if not origem.exists():
            raise ValueError(f"{rotulo} configurado não existe: {origem}")
        if not origem.is_file():
            raise ValueError(f"{rotulo} configurado não é um arquivo: {origem}")

        destino = pasta_saida / f"{nome_saida}{origem.suffix.lower()}"
        if origem.resolve() != destino.resolve():
            copy2(origem, destino)

        destinos.append(destino)

    return destinos



def _origens_de_logos_configuradas(configuracao: ConfiguracaoParoquia) -> set[Path]:
    origens: set[Path] = set()
    for _rotulo, atributo, _nome_saida, _painel in LOGOS_CONFIGURADOS:
        origem = getattr(configuracao, atributo)
        if origem is not None:
            origens.add(origem.resolve())
    return origens



def limpar_logos_gerados_antigos(pasta_saida: Path, preservar: set[Path] | None = None) -> None:
    """Remove apenas logos gerados anteriormente dentro da pasta de saída."""
    if not pasta_saida.exists():
        return

    preservar = preservar or set()
    pasta_saida_resolvida = pasta_saida.resolve()
    for nome_logo in LOGOS_GERADOS_ANTIGOS:
        for caminho in pasta_saida.glob(f"{nome_logo}.*"):
            caminho_resolvido = caminho.resolve()
            if caminho_resolvido in preservar:
                continue
            if caminho_resolvido.parent != pasta_saida_resolvida:
                continue
            if caminho.is_file():
                caminho.unlink()



def montar_logos_por_painel(logos_copiados: list[Path]) -> dict[int, str]:
    """Converte os logos copiados para caminhos que o navegador consegue abrir."""
    logos_por_painel: dict[int, str] = {}
    for logo in logos_copiados:
        painel = PAINEL_POR_LOGO_GERADO.get(logo.stem)
        if painel is not None:
            logos_por_painel[painel] = logo.resolve().as_uri()
    return logos_por_painel

def montar_resumo_dos_logos(logos_copiados: list[Path]) -> str:
    """Monta o resumo dos logos copiados para o relatório final."""
    if not logos_copiados:
        return "Nenhum logo configurado."

    return "\n".join(f"- {logo.name}" for logo in logos_copiados)
