"""Testes da triagem em lote. Rodar: python3 -m unittest test_triagem -v"""
import tempfile
import unittest
from pathlib import Path

import desk
import desk_escrita as esc
import desk_triagem as t
from test_desk import criar_frente
from test_escrita import HOJE, TEXTO


class RenderizarTests(unittest.TestCase):
    def test_buffer_tem_versao_secoes_subsecoes_e_so_abertas(self):
        buf = t.renderizar_buffer("f", TEXTO)
        primeira = buf.splitlines()[0]
        self.assertEqual(primeira, f"# desk triagem f — versão {t.versao(TEXTO)}")
        self.assertIn("## Urgente\n1 [ ] A — @D — crítica\n\n## Em aberto\n"
                      "2 [ ] B — @D — [issue](https://x)\n# ### Sub\n3 [ ] C — @D\n", buf)
        self.assertNotIn("Z — @D", buf)
