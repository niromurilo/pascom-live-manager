"""
Utilitarios para preparar dados do Animated Lower Thirds.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from resultado import Resultado
from buscar_liturgia import (
    LiturgiaDoDia,
    extrair_citacao,
    extrair_citacao_do_salmo,
)

QUANTIDADE_MAXIMA_DE_PAINEIS = 4
QUANTIDADE_MAXIMA_DE_SLOTS = 10
PAINEL_TITULO = 1
PAINEL_LEITURAS = 2
PAINEL_PIX = 3
CAMINHO_CONFIG_BASE = Path(__file__).parent / "config" / "animated_lower_thirds_base.json"

@dataclass(frozen=True)
class LowerThird:
    """Representa um valor a publicar num Lower Third do Animated Lower Thirds.

    slot=None -> valor "ativo" do painel (usado hoje só pelo título).
    slot=1..10 -> memory slot específico dentro do painel.
    """

    painel: int
    nome: str
    info: str
    slot: int | None = None


def criar_lowers_da_liturgia(
    liturgia: LiturgiaDoDia,
    celebrante: str | None = None,
    chave_pix: str = "",
    preces: str = "",
) -> list[LowerThird]:
    """Cria os lowers disponiveis a partir dos dados extraidos da liturgia."""
    lower_titulo = _criar_lower_titulo(liturgia, celebrante)
    sequencia_de_leituras = _criar_sequencia_de_leituras(liturgia, preces=preces)
    lower_pix = LowerThird(painel=3, nome="PIX DA PARÓQUIA", info=chave_pix)

    return [lower_titulo, *sequencia_de_leituras, lower_pix]


def gerar_configuracao_importacao(
    lowers: list[LowerThird],
    logos_por_painel: dict[int, str] | None = None,
) -> dict[str, str]:
    """Gera um dicionario compativel com a importacao do Animated Lower Thirds."""
    if not CAMINHO_CONFIG_BASE.exists():
        raise FileNotFoundError(
            f"Arquivo-base não encontrado: {CAMINHO_CONFIG_BASE}"
        )

    dados = json.loads(
        CAMINHO_CONFIG_BASE.read_text(encoding="utf-8")
    )

    logos_por_painel = logos_por_painel or {}
    lowers_ordenados = _ordenar_lowers_por_painel_e_slot(lowers)
    _limpar_slots_dinamicos(dados)
    _aplicar_logos_configurados(dados, logos_por_painel)

    for lower in lowers_ordenados:
        if lower.slot is None:
            dados[f"alt-{lower.painel}-name"] = lower.nome
            dados[f"alt-{lower.painel}-info"] = lower.info
            dados[f"alt-{lower.painel}-title"] = lower.nome
            _atualizar_primeiro_slot_do_painel(dados, lower, logos_por_painel)
        else:
            dados[f"alt-{lower.painel}-name-{lower.slot}"] = lower.nome
            dados[f"alt-{lower.painel}-info-{lower.slot}"] = lower.info
            if lower.painel in logos_por_painel:
                dados[f"alt-{lower.painel}-logo-{lower.slot}"] = "default"

    _sincronizar_painel_leituras_ativo(dados, lowers_ordenados)
    return dados

def salvar_configuracao_importacao(dados: dict[str, str], caminho: Path) -> None:
    """Salva a configuracao em JSON para importar no painel do Animated Lower Thirds."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _criar_lower_titulo(
    liturgia: LiturgiaDoDia,
    celebrante: str | None,
) -> LowerThird:
    """Monta o Lower Third do título/celebrante — painel 1, valor único, sem slot."""
    if celebrante:
        return LowerThird(painel=PAINEL_TITULO, nome=liturgia.titulo, info=celebrante)

    return LowerThird(painel=PAINEL_TITULO, nome="Liturgia Diaria", info=liturgia.titulo)


def _criar_sequencia_de_leituras(liturgia: LiturgiaDoDia, preces: str = "") -> list[LowerThird]:
    """Monta a sequencia de leituras no painel 2, um slot por item, na ordem da missa.
    Adiciona PRECES como último slot se houver resposta cadastrada.
    """
    sequencia = [
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Primeira Leitura",
            info=extrair_citacao(liturgia.leitura1),
            slot=1,
        ),
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Salmo Responsorial",
            info=extrair_citacao_do_salmo(liturgia.salmo),
            slot=2,
        ),
    ]

    proximo_slot = 3
    if liturgia.leitura2 is not None:
        sequencia.append(
            LowerThird(
                painel=PAINEL_LEITURAS,
                nome="Segunda Leitura",
                info=extrair_citacao(liturgia.leitura2),
                slot=proximo_slot,
            )
        )
        proximo_slot += 1

    sequencia.append(
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Evangelho",
            info=extrair_citacao(liturgia.evangelho),
            slot=proximo_slot,
        )
    )
    proximo_slot += 1

    preces = preces.strip()
    if preces:
        sequencia.append(
            LowerThird(
                painel=PAINEL_LEITURAS,
                nome="PRECES",
                info=f"R. {preces}",
                slot=proximo_slot,
            )
        )

    return sequencia



def _limpar_slots_dinamicos(dados: dict[str, str]) -> None:
    """Limpa textos/logos de slots gerados sem alterar aparência e tempos do base."""
    for painel in (PAINEL_TITULO, PAINEL_LEITURAS, PAINEL_PIX):
        for slot in range(1, QUANTIDADE_MAXIMA_DE_SLOTS + 1):
            dados[f"alt-{painel}-name-{slot}"] = ""
            dados[f"alt-{painel}-info-{slot}"] = ""
            dados[f"alt-{painel}-logo-{slot}"] = ""



def _aplicar_logos_configurados(dados: dict[str, str], logos_por_painel: dict[int, str]) -> None:
    for painel, caminho_logo in logos_por_painel.items():
        _validar_painel(painel)
        dados[f"alt-{painel}-logo-default"] = caminho_logo
        dados[f"alt-{painel}-logo-preview"] = caminho_logo



def _atualizar_primeiro_slot_do_painel(
    dados: dict[str, str],
    lower: LowerThird,
    logos_por_painel: dict[int, str],
) -> None:
    """Mantem o slot 1 alinhado aos paineis usados como valor ativo."""
    if lower.painel not in (PAINEL_TITULO, PAINEL_PIX):
        return

    dados[f"alt-{lower.painel}-name-1"] = lower.nome
    dados[f"alt-{lower.painel}-info-1"] = lower.info
    if lower.painel in logos_por_painel:
        dados[f"alt-{lower.painel}-logo-1"] = "default"



def _sincronizar_painel_leituras_ativo(
    dados: dict[str, str],
    lowers: list[LowerThird],
) -> None:
    primeira_leitura = next(
        (
            lower
            for lower in lowers
            if lower.painel == PAINEL_LEITURAS and lower.slot is not None
        ),
        None,
    )
    if primeira_leitura is None:
        dados[f"alt-{PAINEL_LEITURAS}-name"] = ""
        dados[f"alt-{PAINEL_LEITURAS}-info"] = ""
        return

    dados[f"alt-{PAINEL_LEITURAS}-name"] = primeira_leitura.nome
    dados[f"alt-{PAINEL_LEITURAS}-info"] = primeira_leitura.info
    dados[f"alt-{PAINEL_LEITURAS}-title"] = primeira_leitura.nome



def _ordenar_lowers_por_painel_e_slot(lowers: list[LowerThird]) -> list[LowerThird]:
    lowers_por_posicao: dict[tuple[int, int], LowerThird] = {}
    for lower in lowers:
        _validar_painel(lower.painel)
        if lower.slot is not None:
            _validar_slot(lower.slot)
        ordem_slot = lower.slot if lower.slot is not None else 0
        lowers_por_posicao[(lower.painel, ordem_slot)] = lower

    return [
        lowers_por_posicao[posicao]
        for posicao in sorted(lowers_por_posicao)
    ]


def _resetar_slots_do_painel(painel: int) -> dict[str, str]:
    """Limpa os slots de memoria de um painel antes de preenche-los de novo.

    Evita que um slot usado ontem (ex: leitura2 num domingo) sobreviva
    escondido num dia em que ele nao deveria existir.
    """
    dados: dict[str, str] = {}
    for slot in range(1, QUANTIDADE_MAXIMA_DE_SLOTS + 1):
        dados[f"alt-{painel}-name-{slot}"] = ""
        dados[f"alt-{painel}-info-{slot}"] = ""

    return dados


def _validar_painel(painel: int) -> None:
    if painel < 1 or painel > QUANTIDADE_MAXIMA_DE_PAINEIS:
        raise ValueError(f"Numero de painel invalido: {painel}")


def _validar_slot(slot: int) -> None:
    if slot < 1 or slot > QUANTIDADE_MAXIMA_DE_SLOTS:
        raise ValueError(f"Numero de slot invalido: {slot}")

def validar_configuracao_gerada(lowers: list[LowerThird], caminho: Path) -> None:
    """Valida o JSON gerado antes do operador importar no Animated Lower Thirds.

    Confere que o arquivo existe, é JSON válido, e que cada lower que
    deveria ter sido escrito de fato aparece no arquivo com conteúdo não
    vazio. Levanta ValueError com mensagem clara em caso de problema —
    nunca falha silenciosamente, nunca deixa o operador importar um JSON
    quebrado sem saber.
    """
    if not caminho.exists():
        raise ValueError(f"Arquivo não foi criado: {caminho}")

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise ValueError(f"Arquivo gerado não é um JSON válido: {erro}") from erro

    for lower in lowers:
        if lower.slot is None:
            chave_nome = f"alt-{lower.painel}-name"
            chave_info = f"alt-{lower.painel}-info"
        else:
            chave_nome = f"alt-{lower.painel}-name-{lower.slot}"
            chave_info = f"alt-{lower.painel}-info-{lower.slot}"

        if not dados.get(chave_nome):
            raise ValueError(f"Campo '{chave_nome}' ficou vazio no JSON gerado ({lower.nome}).")
        if not dados.get(chave_info):
            raise ValueError(f"Campo '{chave_info}' ficou vazio no JSON gerado ({lower.nome}).")
        
def gerar_e_validar_json_dos_lowers(lowers: list[LowerThird], caminho: Path, logos_por_painel: dict[int, str] | None = None) -> Resultado:
    """Salva e valida o JSON dos lowers.

    Não imprime nada — quem chama decide como exibir o resultado
    (CLI imprime, GUI mostra na tela).
    """
    try:
        dados = gerar_configuracao_importacao(lowers, logos_por_painel=logos_por_painel)
        salvar_configuracao_importacao(dados, caminho)
        validar_configuracao_gerada(lowers, caminho)
        return Resultado(sucesso=True, mensagem="JSON gerado e validado com sucesso!")
    except (OSError, ValueError) as erro:
        return Resultado(sucesso=False, mensagem=f"Problema ao gerar o arquivo: {erro}")


def montar_resumo_dos_lowers(liturgia: LiturgiaDoDia, lowers: list[LowerThird], caminho: Path) -> str:
    """Monta o texto de resumo dos lowers gerados, pra impressão ou gravação em arquivo."""
    linhas = [f"Título: {liturgia.titulo}"]
    for lower in _ordenar_lowers_por_painel_e_slot(lowers):
        slot_txt = f" slot {lower.slot}" if lower.slot else ""
        linhas.append(f"Painel {lower.painel}{slot_txt} — {lower.nome}: {lower.info}")
    linhas.append(f"\nArquivo: {caminho}")
    return "\n".join(linhas)
