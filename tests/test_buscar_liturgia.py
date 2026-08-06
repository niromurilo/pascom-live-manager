from __future__ import annotations

import unittest
from unittest.mock import patch

import requests

from buscar_liturgia import buscar_liturgia, extrair_citacao, extrair_liturgia


HTML_LITURGIA = """
<html>
  <head>
    <meta property="og:title" content="Liturgia Diária" />
  </head>
  <body>
    <div id="liturgia-1">
      <p>Leitura do Livro do Gênesis (Gn 1,1-5)</p>
      <p>No princípio&nbsp;Deus criou o céu e a terra.</p>
    </div>
    <div id="liturgia-2">
      <p>Responsório Sl 23(24),1-2.3-4ab</p>
    </div>
    <div id="liturgia-4">
      <p>Proclamação do Evangelho de Jesus Cristo segundo Marcos (Mc 1,14-20)</p>
    </div>
  </body>
</html>
"""


class BuscarLiturgiaTests(unittest.TestCase):
    def test_extrai_liturgia_do_html_renderizado(self) -> None:
        liturgia = extrair_liturgia(HTML_LITURGIA)

        self.assertEqual(liturgia.titulo, "Liturgia Diária")
        self.assertIn("No princípio Deus", liturgia.leitura1)
        self.assertEqual(liturgia.leitura2, None)
        self.assertEqual(extrair_citacao(liturgia.evangelho), "Mc 1,14-20")

    def test_buscar_liturgia_retorna_resultado_de_erro_em_falha_de_rede(self) -> None:
        with patch(
            "buscar_liturgia.buscar_html_da_liturgia",
            side_effect=requests.exceptions.Timeout("tempo esgotado"),
        ):
            resultado = buscar_liturgia("https://exemplo.invalid")

        self.assertFalse(resultado.sucesso)
        self.assertIsNone(resultado.liturgia)
        self.assertIn("problema de conexão", resultado.mensagem)


if __name__ == "__main__":
    unittest.main()
