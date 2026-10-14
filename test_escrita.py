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


FRENTE = ("## Urgente\n- [ ] Fechar contrato — @D — crítica\n## Em aberto\n- [ ] Ler paper — @D\n"
          "- [ ] Ler artigo — @D\n## Concluídas\n")


class VerbosTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.pasta = criar_frente(self.raiz, "f", pendencias=FRENTE)
        self.saida: list[str] = []

    def tearDown(self):
        self._tmp.cleanup()

    def rodar(self, verbo, alvo, respostas=(), **kw):
        frente = desk.carregar(self.raiz)[0][0]
        it = iter(respostas)
        return e.executar(verbo, frente, alvo, hoje=HOJE, entrada=lambda _: next(it),
                          saida=self.saida.append, **kw)

    def texto(self):
        return (self.pasta / "PENDENCIAS.md").read_text(encoding="utf-8")

    def test_feito_por_numero(self):
        self.assertEqual(self.rodar("feito", "2", sim=True), 0)
        self.assertIn("- [x] Ler paper — @D — concluída em 2026-10-13", self.texto())

    def test_feito_por_trecho_com_confirmacao(self):
        self.assertEqual(self.rodar("feito", "artigo", respostas=["s"]), 0)
        self.assertIn("- [x] Ler artigo", self.texto())

    def test_recusa_na_confirmacao_nao_grava(self):
        self.assertEqual(self.rodar("feito", "artigo", respostas=["n"]), 1)
        self.assertEqual(self.texto(), FRENTE)

    def test_ambiguo_em_sim_falha(self):
        with self.assertRaisesRegex(ValueError, "2 pendências"):
            self.rodar("feito", "Ler", sim=True)

    def test_ambiguo_interativo_usa_menu(self):
        self.assertEqual(self.rodar("feito", "Ler", respostas=["2", "s"]), 0)
        self.assertIn("- [x] Ler artigo", self.texto())

    def test_descartar_exige_motivo_em_sim(self):
        with self.assertRaisesRegex(ValueError, "motivo"):
            self.rodar("descartar", "paper", sim=True)

    def test_descartar_com_motivo(self):
        self.assertEqual(self.rodar("descartar", "paper", sim=True, motivo="fora do escopo"), 0)
        self.assertIn("## Descartadas\n- [-] Ler paper — @D — descartada em 2026-10-13 — motivo: fora do escopo",
                      self.texto())

    def test_motivo_com_separador_recusado(self):
        with self.assertRaisesRegex(ValueError, "separador"):
            self.rodar("descartar", "paper", sim=True, motivo="a — b")

    def test_urgente_move(self):
        self.assertEqual(self.rodar("urgente", "paper", sim=True), 0)
        self.assertIn("— crítica\n- [ ] Ler paper — @D\n## Em aberto", self.texto())

    def test_critica_transfere(self):
        self.assertEqual(self.rodar("critica", "artigo", sim=True), 0)
        self.assertIn("- [ ] Fechar contrato — @D\n", self.texto())
        self.assertIn("- [ ] Ler artigo — @D — crítica", self.texto())

    def test_encerrar_critica_pede_sucessora(self):
        self.assertEqual(self.rodar("feito", "contrato", respostas=["1", "s"]), 0)
        self.assertIn("- [ ] Ler paper — @D — crítica", self.texto())

    def test_encerrar_critica_em_sim_falha(self):
        with self.assertRaisesRegex(ValueError, "desk critica"):
            self.rodar("feito", "contrato", sim=True)
