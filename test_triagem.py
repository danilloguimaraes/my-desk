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


class InterpretarTests(unittest.TestCase):
    def setUp(self):
        self.itens = esc.itens_abertos(TEXTO)
        self.buf = t.renderizar_buffer("f", TEXTO)

    def ler(self, buf):
        return t.interpretar_buffer(buf, self.itens)

    def test_buffer_intacto_nao_muda_nada(self):
        r = self.ler(self.buf)
        self.assertEqual((r.mudancas, r.novas, r.erros, r.cancelado), ({}, [], [], False))

    def test_concluir_e_mover(self):
        buf = self.buf.replace("3 [ ] C — @D", "3 [x] C — @D")
        buf = buf.replace("2 [ ] B — @D — [issue](https://x)\n", "").replace(
            "## Urgente\n", "## Urgente\n2 [ ] B — @D — [issue](https://x)\n")
        r = self.ler(buf)
        self.assertEqual(r.erros, [])
        self.assertEqual(r.mudancas[3].situacao, "concluída")
        self.assertEqual((r.mudancas[2].situacao, r.mudancas[2].secao), ("aberta", "Urgente"))

    def test_descarte_sem_motivo(self):
        r = self.ler(self.buf.replace("3 [ ] C — @D", "3 [-] C — @D"))
        self.assertEqual(r.erros, ["nº 3: descarte exige '— motivo: ...'"])

    def test_linha_apagada_e_erro(self):
        r = self.ler(self.buf.replace("3 [ ] C — @D\n", ""))
        self.assertIn("nº 3 sumiram do buffer; para encerrar use [x] ou [-]", r.erros)

    def test_numero_inexistente_e_repetido(self):
        r = self.ler(self.buf + "9 [ ] X — @D\n3 [ ] C — @D\n")
        self.assertIn("nº 9: não existe nesta versão do arquivo", r.erros)
        self.assertIn("nº 3: repetido", r.erros)

    def test_nova_exige_responsavel(self):
        self.assertIn("'[ ] Nova sem dono': pendência nova exige '— @responsável'",
                      self.ler(self.buf + "[ ] Nova sem dono\n").erros)
        r = self.ler(self.buf + "[ ] Nova — @D\n")
        self.assertEqual((r.erros, r.novas[0].conteudo, r.novas[0].secao), ([], "Nova — @D", "Em aberto"))

    def test_sem_itens_cancela(self):
        self.assertTrue(self.ler("# só comentário\n## Urgente\n").cancelado)

    def test_so_linha_malformada_nao_cancela_em_silencio(self):
        r = self.ler("- [ ] X — @D\n")
        self.assertFalse(r.cancelado)
        self.assertTrue(any("esperado" in e for e in r.erros))

    def test_concluir_sem_responsavel_original_e_erro(self):
        r = self.ler(self.buf.replace("3 [ ] C — @D", "3 [x] C"))
        self.assertTrue(any("falta '— @responsável'" in e for e in r.erros))

    def test_concluir_mantendo_responsavel_passa(self):
        r = self.ler(self.buf.replace("3 [ ] C — @D", "3 [x] C — @D"))
        self.assertEqual(r.erros, [])


class AplicarTests(unittest.TestCase):
    def test_tirar_a_unica_critica_e_erro_novo(self):
        with tempfile.TemporaryDirectory() as tmp:
            criar_frente(Path(tmp), "f", pendencias=TEXTO)
            frente = desk.carregar(Path(tmp))[0][0]
            buf = t.renderizar_buffer("f", TEXTO).replace("1 [ ] A — @D — crítica", "1 [x] A — @D")
            novo, erros, _ = t.aplicar_buffer(frente, TEXTO, buf, HOJE)
            self.assertTrue(any("(tem 0)" in e for e in erros))

    def test_aplicacao_valida_devolve_texto_novo(self):
        with tempfile.TemporaryDirectory() as tmp:
            criar_frente(Path(tmp), "f", pendencias=TEXTO)
            frente = desk.carregar(Path(tmp))[0][0]
            buf = t.renderizar_buffer("f", TEXTO).replace("3 [ ] C — @D", "3 [-] C — @D — motivo: obsoleto")
            novo, erros, leitura = t.aplicar_buffer(frente, TEXTO, buf, HOJE)
            self.assertEqual(erros, [])
            self.assertIn("- [-] C — @D — descartada em 2026-10-13 — motivo: obsoleto", novo)
            self.assertEqual(t.resumir(leitura), "1 descartada(s)")


class LacoTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.pasta = criar_frente(Path(self._tmp.name), "f", pendencias=TEXTO)
        self.frente = desk.carregar(Path(self._tmp.name))[0][0]
        self.saida: list[str] = []

    def tearDown(self):
        self._tmp.cleanup()

    def texto(self):
        return (self.pasta / "PENDENCIAS.md").read_text(encoding="utf-8")

    def test_erro_reabre_com_anotacao_e_depois_grava(self):
        vistos: list[str] = []
        edicoes = iter([lambda b: b.replace("3 [ ] C — @D", "3 [-] C — @D"),
                        lambda b: b.replace("3 [-] C — @D", "3 [-] C — @D — motivo: obsoleto")])

        def editor(buf):
            vistos.append(buf)
            return next(edicoes)(buf)

        self.assertEqual(t.triar(self.frente, editar=editor, hoje=HOJE, saida=self.saida.append), 0)
        self.assertIn("# ! nº 3: descarte exige '— motivo: ...'", vistos[1])
        self.assertIn("- [-] C — @D — descartada em 2026-10-13 — motivo: obsoleto", self.texto())
        self.assertEqual(self.saida[-1], "ok: f — 1 descartada(s)")

    def test_buffer_vazio_cancela(self):
        self.assertEqual(t.triar(self.frente, editar=lambda b: "", hoje=HOJE, saida=self.saida.append), 1)
        self.assertEqual(self.texto(), TEXTO)

    def test_sem_mudanca(self):
        self.assertEqual(t.triar(self.frente, editar=lambda b: b, hoje=HOJE, saida=self.saida.append), 0)
        self.assertEqual(self.saida[-1], "nada mudou")

    def test_aplicar_recusa_versao_velha(self):
        buf = t.exportar(self.frente)
        (self.pasta / "PENDENCIAS.md").write_text(TEXTO + "- [ ] tarde — @D\n", encoding="utf-8")
        self.assertEqual(t.aplicar_arquivo(self.frente, buf, hoje=HOJE, saida=self.saida.append), 1)
        self.assertIn("mudou desde a exportação", self.saida[-1])

    def test_aplicar_arquivo_valido(self):
        buf = t.exportar(self.frente).replace("2 [ ] B", "2 [x] B")
        self.assertEqual(t.aplicar_arquivo(self.frente, buf, hoje=HOJE, saida=self.saida.append), 0)
        self.assertIn("- [x] B — @D — [issue](https://x) — concluída em 2026-10-13", self.texto())
