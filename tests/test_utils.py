from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from utils import caminho_assets, pasta_recursos


class PastaRecursosTests(unittest.TestCase):
    def test_em_desenvolvimento_retorna_raiz_do_projeto(self) -> None:
        # Sem frozen, deve apontar para a raiz do projeto (onde utils.py esta)
        raiz = Path(__file__).resolve().parent.parent
        self.assertEqual(pasta_recursos(), raiz)

    def test_em_desenvolvimento_pasta_assets_existe(self) -> None:
        self.assertTrue(caminho_assets().is_dir())

    def test_frozen_usa_meipass(self) -> None:
        caminho_falso = Path("C:/fake/_internal")
        with patch.object(sys, "frozen", True, create=True), \
             patch.object(sys, "_MEIPASS", str(caminho_falso), create=True):
            self.assertEqual(pasta_recursos(), caminho_falso)

    def test_frozen_caminho_assets_usa_meipass(self) -> None:
        caminho_falso = Path("C:/fake/_internal")
        with patch.object(sys, "frozen", True, create=True), \
             patch.object(sys, "_MEIPASS", str(caminho_falso), create=True):
            self.assertEqual(caminho_assets(), caminho_falso / "assets")


if __name__ == "__main__":
    unittest.main()
