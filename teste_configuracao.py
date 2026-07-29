from pathlib import Path

from paroquia_config import (
    carregar_configuracao,
    salvar_configuracao,
)

config = carregar_configuracao()

print(config)

config.caminho_logo_pix = Path("C:/teste/logo.png")
config.preces = "Teste das preces"

salvar_configuracao(config)

config = carregar_configuracao()

print(config)
print(type(config.caminho_logo_pix))