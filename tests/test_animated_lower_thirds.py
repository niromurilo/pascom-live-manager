from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from animated_lower_thirds import (
    criar_lowers_da_liturgia,
    gerar_configuracao_importacao,
    gerar_e_validar_json_dos_lowers,
)
from buscar_liturgia import LiturgiaDoDia


def liturgia_exemplo() -> LiturgiaDoDia:
    return LiturgiaDoDia(
        titulo="Solenidade de São José",
        leitura1="Leitura do Livro do Profeta Isaías (Is 7,10-14)",
        salmo="Responsório Sl 22(23),1-3a.3b-4.5.6",
        evangelho="Proclamação do Evangelho de Jesus Cristo segundo Lucas (Lc 1,26-38)",
        leitura2="Leitura da Carta de São Paulo aos Romanos (Rm 4,13.16-18.22)",
    )


class AnimatedLowerThirdsTests(unittest.TestCase):
    def test_cria_lowers_com_pix_preces_e_leitura2(self) -> None:
        lowers = criar_lowers_da_liturgia(
            liturgia_exemplo(),
            celebrante="Pe. João",
            chave_pix="pix@example.com",
            preces="ouvi-nos, Senhor",
        )

        self.assertEqual(lowers[0].info, "Pe. João")
        self.assertEqual(lowers[-1].nome, "PIX DA PARÓQUIA")
        self.assertEqual(lowers[-1].info, "pix@example.com")

        preces = next(lower for lower in lowers if lower.nome == "PRECES")
        self.assertEqual(preces.slot, 5)
        self.assertEqual(preces.info, "R. ouvi-nos, Senhor")

    def test_gera_e_valida_json_dos_lowers(self) -> None:
        lowers = criar_lowers_da_liturgia(
            liturgia_exemplo(),
            celebrante="Pe. João",
            chave_pix="pix@example.com",
            preces="ouvi-nos, Senhor",
        )
        dados = gerar_configuracao_importacao(lowers)

        self.assertEqual(dados["alt-2-info-5"], "R. ouvi-nos, Senhor")
        self.assertEqual(dados["alt-3-info"], "pix@example.com")

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "lowers.json"
            resultado = gerar_e_validar_json_dos_lowers(lowers, caminho)

            self.assertTrue(resultado.sucesso)
            self.assertEqual(json.loads(caminho.read_text(encoding="utf-8"))["alt-3-info"], "pix@example.com")


if __name__ == "__main__":
    unittest.main()
