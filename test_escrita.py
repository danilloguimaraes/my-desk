"""Testes do núcleo de escrita. Rodar: python3 -m unittest test_escrita -v"""
import tempfile
import unittest
from datetime import date
from pathlib import Path

import desk
import desk_escrita as e
from test_desk import criar_frente

HOJE = date(2026, 10, 13)
TEXTO = ("# P\n\n## Urgente\n\n- [ ] A — @D — crítica\n\n## Em aberto\n\n- [ ] B — @D — [issue](https://x)\n\n"
         "### Sub\n\n- [ ] C — @D\n\n## Concluídas\n\n- [x] Z — @D — concluída em 2026-10-01\n")


class ItensTests(unittest.TestCase):
    def test_numera_abertas_em_ordem_de_arquivo(self):
        itens = e.itens_abertos(TEXTO)
        self.assertEqual([(i.chave, i.secao, i.conteudo) for i in itens],
                         [(1, "Urgente", "A — @D — crítica"), (2, "Em aberto", "B — @D — [issue](https://x)"),
                          (3, "Em aberto", "C — @D")])


class ReescreverTests(unittest.TestCase):
    def test_sem_mudancas_preserva_texto(self):
        self.assertEqual(e.reescrever(TEXTO, {}, [], HOJE), TEXTO)

    def test_concluir_move_para_topo_e_tira_critica(self):
        novo = e.reescrever(TEXTO, {1: e.Mudanca("concluída", "Urgente", "A — @D — crítica")}, [], HOJE)
        self.assertNotIn("- [ ] A", novo)
        self.assertIn("## Concluídas\n\n- [x] A — @D — concluída em 2026-10-13\n- [x] Z", novo)

    def test_descartar_cria_secao_e_ordena_campos(self):
        m = e.Mudanca("descartada", "Em aberto", "C — @D — motivo: obsoleto")
        novo = e.reescrever(TEXTO, {3: m}, [], HOJE)
        self.assertTrue(novo.endswith("## Descartadas\n- [-] C — @D — descartada em 2026-10-13 — motivo: obsoleto\n"))

    def test_mover_preserva_campos_legados(self):
        novo = e.reescrever(TEXTO, {2: e.Mudanca("aberta", "Urgente", "B — @D — [issue](https://x)")}, [], HOJE)
        self.assertIn("- [ ] A — @D — crítica\n- [ ] B — @D — [issue](https://x)\n\n## Em aberto", novo)

    def test_editar_no_lugar(self):
        novo = e.reescrever(TEXTO, {3: e.Mudanca("aberta", "Em aberto", "C revisto — @D")}, [], HOJE)
        self.assertIn("### Sub\n\n- [ ] C revisto — @D\n", novo)

    def test_nova_pendencia(self):
        novo = e.reescrever(TEXTO, {}, [e.Mudanca("aberta", "Em aberto", "N — @D")], HOJE)
        self.assertIn("- [ ] B — @D — [issue](https://x)\n- [ ] N — @D\n\n### Sub", novo)


class ValidacaoTests(unittest.TestCase):
    def test_so_erros_novos_contam(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = criar_frente(Path(tmp), "f", pendencias="## Urgente\n- [ ] A — @D\n## Em aberto\n")
            frente = desk.carregar(Path(tmp))[0][0]
            antes = (pasta / "PENDENCIAS.md").read_text(encoding="utf-8")
            # sem crítica antes e depois: não é erro novo
            self.assertEqual(e.erros_novos(frente, antes, antes + "- [ ] B — @D\n"), [])
            # duas críticas: erro novo
            depois = antes.replace("- [ ] A — @D", "- [ ] A — @D — crítica") + "- [ ] B — @D — crítica\n"
            self.assertTrue(any("(tem 2)" in m for m in e.erros_novos(frente, antes, depois)))
