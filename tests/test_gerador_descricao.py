from __future__ import annotations

import unittest
from datetime import date

from buscar_liturgia import LiturgiaDoDia
from gerador_descricao import gerar_descricao, gerar_titulo


class GeradorDescricaoTests(unittest.TestCase):
    def test_gera_titulo_e_descricao_com_citacoes(self) -> None:
        liturgia = LiturgiaDoDia(
            titulo="Solenidade de São José",
            leitura1="Leitura do Livro do Profeta Isaías (Is 7,10-14)",
            salmo="Responsório Sl 22(23),1-3a.3b-4.5.6",
            evangelho="Proclamação do Evangelho de Jesus Cristo segundo Lucas (Lc 1,26-38)",
            leitura2="Leitura da Carta de São Paulo aos Romanos (Rm 4,13.16-18.22)",
        )

        titulo = gerar_titulo(liturgia, date(2026, 8, 6))
        descricao = gerar_descricao(
            liturgia,
            date(2026, 8, 6),
            nome_paroquia="Paróquia São José",
            celebrante="Pe. João",
        )

        self.assertEqual(titulo, "Santa Missa | Solenidade de São José | 06/08/2026")
        self.assertIn("Celebrante: Pe. João", descricao)
        self.assertIn("1ª Leitura: Is 7,10-14", descricao)
        self.assertIn("2ª Leitura: Rm 4,13.16-18.22", descricao)
        self.assertIn("Evangelho: Lc 1,26-38", descricao)


if __name__ == "__main__":
    unittest.main()
