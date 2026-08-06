from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from buscar_liturgia import LiturgiaDoDia, ResultadoBusca
from paroquia_config import ConfiguracaoParoquia
from services.preparacao import executar_preparacao


def liturgia_exemplo() -> LiturgiaDoDia:
    return LiturgiaDoDia(
        titulo="Solenidade de São José",
        leitura1="Leitura do Livro do Profeta Isaías (Is 7,10-14)",
        salmo="Responsório Sl 22(23),1-3a.3b-4.5.6",
        evangelho="Proclamação do Evangelho de Jesus Cristo segundo Lucas (Lc 1,26-38)",
        leitura2=None,
    )


class PreparacaoTests(unittest.TestCase):
    def test_prepara_transmissao_copiando_logos_configurados(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            pasta_logos = base / "logos"
            pasta_saida = base / "saida"
            pasta_logos.mkdir()

            logo_pix = pasta_logos / "pix-original.png"
            logo_leituras = pasta_logos / "leituras-original.jpg"
            logo_celebrante = pasta_logos / "celebrante-original.jpeg"
            logo_pix.write_bytes(b"pix")
            logo_leituras.write_bytes(b"leituras")
            logo_celebrante.write_bytes(b"celebrante")

            configuracao = ConfiguracaoParoquia(
                caminho_logo_pix=logo_pix,
                caminho_logo_leituras=logo_leituras,
                caminho_logo_celebrante=logo_celebrante,
                preces="ouvi-nos, Senhor",
                chave_pix="pix@example.com",
            )

            with patch(
                "services.preparacao.buscar_liturgia",
                return_value=ResultadoBusca(sucesso=True, mensagem="ok", liturgia=liturgia_exemplo()),
            ), patch("services.preparacao.carregar_configuracao", return_value=configuracao):
                resultado = executar_preparacao(
                    nome_paroquia="Paróquia São José",
                    celebrante="Pe. João",
                    pasta_saida=pasta_saida,
                )

            self.assertTrue(resultado.sucesso)
            self.assertTrue((pasta_saida / "titulo.txt").exists())
            self.assertTrue((pasta_saida / "descricao.txt").exists())
            self.assertTrue((pasta_saida / "resumo.txt").exists())
            self.assertEqual((pasta_saida / "logo_pix.png").read_bytes(), b"pix")
            self.assertEqual((pasta_saida / "logo_leituras.jpg").read_bytes(), b"leituras")
            self.assertEqual((pasta_saida / "logo_celebrante.jpeg").read_bytes(), b"celebrante")

            dados_json = json.loads((pasta_saida / "animated_lower_thirds_liturgia.json").read_text(encoding="utf-8"))
            self.assertEqual(dados_json["alt-3-info"], "pix@example.com")
            self.assertIn("LOGOS COPIADOS", resultado.relatorio or "")

    def test_preparacao_falha_quando_logo_configurado_nao_existe(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            configuracao = ConfiguracaoParoquia(
                caminho_logo_pix=base / "ausente.png",
                chave_pix="pix@example.com",
            )

            with patch(
                "services.preparacao.buscar_liturgia",
                return_value=ResultadoBusca(sucesso=True, mensagem="ok", liturgia=liturgia_exemplo()),
            ), patch("services.preparacao.carregar_configuracao", return_value=configuracao):
                resultado = executar_preparacao(
                    nome_paroquia="Paróquia São José",
                    celebrante=None,
                    pasta_saida=base / "saida",
                )

        self.assertFalse(resultado.sucesso)
        self.assertIn("não existe", resultado.mensagem)


if __name__ == "__main__":
    unittest.main()
