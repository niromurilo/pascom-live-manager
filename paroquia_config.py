"""
Pascom Live Manager
Persistência das configurações específicas de cada paróquia — logos e
preces padrão. Único módulo que sabe que essas configurações existem
como um arquivo JSON em disco; GUI e serviços não devem ler/escrever
esse arquivo diretamente.
"""

from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from utils import pasta_dados_usuario

CAMINHO_ARQUIVO = (
    pasta_dados_usuario() / "configuracao_paroquia.json"
)


@dataclass
class ConfiguracaoParoquia:
    """Configurações da paróquia que persistem entre execuções do programa.

    Diferente de Resultado e suas subclasses (retornos imutáveis de uma
    operação concluída), essa classe representa estado editável — a GUI
    mantém uma instância viva e atualiza os campos conforme o usuário
    interage, por isso não é frozen.
    """

    caminho_logo_pix: Path | None = None
    caminho_logo_leituras: Path | None = None
    caminho_logo_celebrante: Path | None = None
    preces: str = ""
    chave_pix: str = ""


def carregar_configuracao() -> ConfiguracaoParoquia:
    """Carrega a configuração salva da paróquia.

    Se o arquivo ainda não existir (primeira execução do programa, ou
    outra paróquia usando o projeto pela primeira vez), devolve uma
    ConfiguracaoParoquia com valores vazios em vez de lançar erro — quem
    chama não precisa tratar "arquivo não existe" como caso especial.
    """
    if not CAMINHO_ARQUIVO.exists():
        return ConfiguracaoParoquia()

    dados = json.loads(CAMINHO_ARQUIVO.read_text(encoding="utf-8"))

    return ConfiguracaoParoquia(
        caminho_logo_pix=_para_path(dados.get("caminho_logo_pix")),
        caminho_logo_leituras=_para_path(dados.get("caminho_logo_leituras")),
        caminho_logo_celebrante=_para_path(dados.get("caminho_logo_celebrante")),
        preces=dados.get("preces", ""),
        chave_pix=dados.get("chave_pix", ""),
    )


def salvar_configuracao(configuracao: ConfiguracaoParoquia) -> None:
    """Salva a configuração da paróquia em disco, sobrescrevendo o arquivo anterior."""
    dados = {
        chave: str(valor) if isinstance(valor, Path) else valor
        for chave, valor in asdict(configuracao).items()
    }
    CAMINHO_ARQUIVO.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def _para_path(valor: str | None) -> Path | None:
    """Converte um valor lido do JSON para Path, preservando None quando ausente."""
    return Path(valor) if valor else None