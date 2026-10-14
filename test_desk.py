"""Testes do desk.py. Rodar: python3 -m unittest test_desk -v"""
import io
import tempfile
import unittest
from pathlib import Path

import desk

FICHA = """# {nome}

| campo | valor |
|---|---|
| situacao | {situacao} |
| papel | Dev |
| estado | Em curso |

Contexto livre.
"""

PENDENCIAS_OK = """# Pendências

## Urgente
- [ ] Fechar contrato — @Danillo — 2026-10-20 — crítica

## Em aberto

## Concluídas
- [x] Entregar relatório — @Danillo — concluída em 2026-10-01
"""


def criar_frente(raiz: Path, rel: str, situacao: str = "ativa", pendencias: str | None = PENDENCIAS_OK,
                 nome: str | None = None) -> Path:
    pasta = raiz / rel
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "README.md").write_text(FICHA.format(nome=nome or rel, situacao=situacao), encoding="utf-8")
    if pendencias is not None:
        (pasta / "PENDENCIAS.md").write_text(pendencias, encoding="utf-8")
    return pasta


class GramaticaTests(unittest.TestCase):
    def test_linha_completa(self):
        p, erros = desk.interpretar_pendencia(
            "- [ ] Fechar contrato — @Danillo — 2026-10-20 — origem: ../x.md — crítica", "Urgente", 3)
        self.assertEqual(erros, [])
        self.assertEqual(p.descricao, "Fechar contrato")
        self.assertEqual(p.responsavel, "@Danillo")
        self.assertEqual(p.prazo, "2026-10-20")
        self.assertEqual(p.origem, "../x.md")
        self.assertTrue(p.critica)
        self.assertTrue(p.urgente)

    def test_concluida_com_data(self):
        p, erros = desk.interpretar_pendencia("- [x] Entregar — @Danillo — concluída em 2026-10-01",
                                              "Concluídas", 1)
        self.assertEqual(erros, [])
        self.assertFalse(p.aberta)
        self.assertEqual(p.concluida_em, "2026-10-01")

    def test_campo_livre_legado_tolerado(self):
        p, erros = desk.interpretar_pendencia("- [ ] X — @D — foo", "Em aberto", 1)
        self.assertEqual(erros, [])
        self.assertEqual(p.descricao, "X")

    def test_responsavel_ausente_tolerado_na_leitura(self):
        p, erros = desk.interpretar_pendencia("- [ ] X", "Em aberto", 1)
        self.assertEqual(erros, [])
        self.assertIsNone(p.responsavel)

    def test_data_invalida_nao_e_prazo(self):
        p, _ = desk.interpretar_pendencia("- [ ] X — @D — 2026-13-40", "Em aberto", 1)
        self.assertIsNone(p.prazo)

    def test_aberta_em_concluidas(self):
        _, erros = desk.interpretar_pendencia("- [ ] X — @D", "Concluídas", 1)
        self.assertTrue(any("aberta em 'Concluídas'" in e for e in erros))

    def test_concluida_fora_de_concluidas(self):
        _, erros = desk.interpretar_pendencia("- [x] X — @D — concluída em 2026-10-01", "Em aberto", 1)
        self.assertTrue(any("fora de 'Concluídas'" in e for e in erros))

    def test_descartada_completa(self):
        p, erros = desk.interpretar_pendencia(
            "- [-] Migrar X — @D — descartada em 2026-10-13 — motivo: absorvido pela refundação",
            "Descartadas", 1)
        self.assertEqual(erros, [])
        self.assertEqual(p.situacao, "descartada")
        self.assertFalse(p.aberta)
        self.assertEqual(p.descartada_em, "2026-10-13")
        self.assertEqual(p.motivo, "absorvido pela refundação")

    def test_descartada_sem_motivo(self):
        _, erros = desk.interpretar_pendencia("- [-] X — @D — descartada em 2026-10-13", "Descartadas", 1)
        self.assertTrue(any("sem 'motivo: ...'" in e for e in erros))

    def test_descartada_fora_de_descartadas(self):
        _, erros = desk.interpretar_pendencia(
            "- [-] X — @D — descartada em 2026-10-13 — motivo: m", "Concluídas", 1)
        self.assertTrue(any("fora de 'Descartadas'" in e for e in erros))

    def test_aberta_em_descartadas(self):
        _, erros = desk.interpretar_pendencia("- [ ] X — @D", "Descartadas", 1)
        self.assertTrue(any("aberta em 'Descartadas'" in e for e in erros))

    def test_motivo_com_separador_e_erro(self):
        _, erros = desk.interpretar_pendencia(
            "- [-] X — @D — descartada em 2026-10-01 — motivo: a — b", "Descartadas", 1)
        self.assertTrue(any("não pode conter ' — '" in e for e in erros))


class FichaTests(unittest.TestCase):
    def test_le_tabela(self):
        ficha, linha = desk.ler_ficha(FICHA.format(nome="x", situacao="ativa"))
        self.assertEqual(ficha["situacao"], "ativa")
        self.assertEqual(ficha["papel"], "Dev")
        self.assertEqual(linha, 3)

    def test_sem_tabela(self):
        ficha, _ = desk.ler_ficha("# Prosa sem ficha\n")
        self.assertIsNone(ficha)


class CheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def erros(self):
        return [str(e) for e in desk.carregar(self.raiz)[1]]

    def test_repo_conforme_sem_erros(self):
        criar_frente(self.raiz, "frente-a")
        self.assertEqual(self.erros(), [])

    def test_ficha_ausente(self):
        pasta = self.raiz / "sem-ficha"
        pasta.mkdir()
        (pasta / "projeto.md").write_text("prosa", encoding="utf-8")
        self.assertTrue(any("ficha ausente" in e for e in self.erros()))

    def test_artefato_nao_reconhecido(self):
        pasta = criar_frente(self.raiz, "frente-a")
        (pasta / "anotacoes.md").write_text("log", encoding="utf-8")
        self.assertTrue(any("artefato não reconhecido" in e for e in self.erros()))

    def test_artefato_legado_tolerado(self):
        pasta = criar_frente(self.raiz, "frente-a")
        (pasta / "monitoramento.md").write_text("log", encoding="utf-8")
        self.assertEqual(self.erros(), [])

    def test_sem_critica_em_ativa(self):
        criar_frente(self.raiz, "frente-a", pendencias="## Urgente\n\n## Em aberto\n\n## Concluídas\n")
        self.assertTrue(any("exatamente 1 pendência aberta crítica (tem 0)" in e for e in self.erros()))

    def test_duas_criticas_em_ativa(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n- [ ] B — @D — crítica\n## Concluídas\n"))
        self.assertTrue(any("(tem 2)" in e for e in self.erros()))

    def test_pausada_nao_exige_critica(self):
        criar_frente(self.raiz, "frente-a", situacao="pausada",
                     pendencias="## Urgente\n\n## Em aberto\n\n## Concluídas\n")
        self.assertEqual(self.erros(), [])

    def test_urgencia_duplicada_entre_frentes(self):
        mesmo = "## Urgente\n- [ ] Mesma coisa — @D — crítica\n## Em aberto\n## Concluídas\n"
        criar_frente(self.raiz, "frente-a", pendencias=mesmo)
        criar_frente(self.raiz, "frente-b", pendencias=mesmo)
        self.assertTrue(any("urgência duplicada" in e for e in self.erros()))

    def test_origem_inexistente(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — origem: nao-existe.md — crítica\n## Em aberto\n## Concluídas\n"))
        self.assertTrue(any("origem inexistente" in e for e in self.erros()))

    def test_origem_url_aceita(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — origem: https://exemplo.com/x — crítica\n## Em aberto\n## Concluídas\n"))
        self.assertEqual(self.erros(), [])

    def test_origem_relativa_resolvida_a_partir_da_frente(self):
        pasta = criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — origem: reunioes/ata.md — crítica\n## Em aberto\n## Concluídas\n"))
        (pasta / "reunioes").mkdir()
        (pasta / "reunioes" / "ata.md").write_text("ata", encoding="utf-8")
        self.assertEqual(self.erros(), [])

    def test_lista_numerada_e_denunciada(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n1. [ ] B — @D\n## Concluídas\n"))
        self.assertTrue(any("lista numerada" in e for e in self.erros()))

    def test_descartada_nao_conta_como_critica(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n## Concluídas\n## Descartadas\n"
            "- [-] B — @D — descartada em 2026-10-13 — motivo: m\n"))
        self.assertEqual(self.erros(), [])


class PainelTests(unittest.TestCase):
    def test_mostra_ativas_e_urgentes_sem_pausadas(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            criar_frente(raiz, "ativa-x", nome="Ativa X")
            criar_frente(raiz, "pausada-y", situacao="pausada")
            frentes, erros = desk.carregar(raiz)
            saida = "\n".join(desk.renderizar_painel(frentes, erros))
            self.assertIn("| ativa-x |", saida)
            self.assertNotIn("| pausada-y |", saida)
            self.assertIn("- [ativa-x] Fechar contrato — @Danillo — 2026-10-20", saida)
            self.assertNotIn("Entregar relatório", saida)

    def test_frente_numera_pendencias_abertas(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            criar_frente(raiz, "f", pendencias="## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n- [ ] B — @D\n")
            frentes, erros = desk.carregar(raiz)
            saida = "\n".join(desk.renderizar_frente(frentes[0], erros))
            self.assertIn("1. [URGENTE] A — @D", saida)
            self.assertIn("2. B — @D", saida)


class AddTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n\n## Em aberto\n\n## Concluídas\n"))

    def tearDown(self):
        self._tmp.cleanup()

    def frente(self) -> desk.Frente:
        return next(f for f in desk.carregar(self.raiz)[0] if f.id == "frente-a")

    def test_adiciona_urgente_em_linha_canonica(self):
        linha = desk.adicionar_pendencia(self.frente(), "Enviar proposta", "Danillo", urgente=True,
                                         critica=True, prazo="2026-10-30")
        self.assertEqual(linha, "- [ ] Enviar proposta — @Danillo — 2026-10-30 — crítica")
        texto = (self.raiz / "frente-a" / "PENDENCIAS.md").read_text(encoding="utf-8")
        self.assertIn("## Urgente\n- [ ] Enviar proposta — @Danillo — 2026-10-30 — crítica", texto)
        _, erros = desk.carregar(self.raiz)
        self.assertFalse(any("PENDENCIAS" in str(e) for e in erros))

    def test_recusa_segunda_critica(self):
        desk.adicionar_pendencia(self.frente(), "Primeira", "Danillo", critica=True)
        with self.assertRaises(ValueError):
            desk.adicionar_pendencia(self.frente(), "Segunda", "Danillo", critica=True)

    def test_recusa_descricao_com_separador(self):
        with self.assertRaises(ValueError):
            desk.adicionar_pendencia(self.frente(), "A — B", "Danillo")

    def test_recusa_origem_inexistente(self):
        with self.assertRaises(ValueError):
            desk.adicionar_pendencia(self.frente(), "X", "Danillo", origem="nao-existe.md")

    def test_assistente_roteirizado(self):
        respostas = iter(["frente-a", "Ler o paper", "Danillo", "s", "n", "", ""])
        saida: list[str] = []
        codigo = desk.assistente(self.raiz, entrada=lambda _: next(respostas), saida=saida.append)
        self.assertEqual(codigo, 0)
        texto = (self.raiz / "frente-a" / "PENDENCIAS.md").read_text(encoding="utf-8")
        self.assertIn("## Urgente\n- [ ] Ler o paper — @Danillo", texto)


class PrimitivasTests(unittest.TestCase):
    TEXTO = ("# P\n\n## Urgente\n\n## Em aberto\n\n- [ ] A — @D\n\n### Sub\n\n- [ ] B — @D\n\n"
             "## Concluídas\n\n<!-- mover para cá -->\n\n- [x] C — @D — concluída em 2026-10-01\n")

    def test_insere_no_fim_do_bloco_de_topo_antes_da_subsecao(self):
        linhas = desk.inserir_em_secao(self.TEXTO.splitlines(), "Em aberto", ["- [ ] N — @D"], topo=False)
        texto = "\n".join(linhas)
        self.assertIn("- [ ] A — @D\n- [ ] N — @D\n\n### Sub", texto)

    def test_insere_no_topo_de_concluidas_depois_do_comentario(self):
        linhas = desk.inserir_em_secao(self.TEXTO.splitlines(), "Concluídas", ["- [x] N"], topo=True)
        self.assertIn("<!-- mover para cá -->\n\n- [x] N\n- [x] C", "\n".join(linhas))

    def test_insere_no_topo_depois_de_comentario_multilinha(self):
        texto = "# P\n\n## Concluídas\n\n<!-- nota\nexplicando -->\n\n- [x] C — @D — concluída em 2026-10-01\n"
        linhas = desk.inserir_em_secao(texto.splitlines(), "Concluídas", ["- [x] N"], topo=True)
        saida = "\n".join(linhas)
        self.assertIn("explicando -->\n\n- [x] N\n- [x] C", saida)

    def test_cria_secao_ausente_no_fim(self):
        linhas = desk.inserir_em_secao(self.TEXTO.splitlines(), "Descartadas", ["- [-] N"], topo=True)
        self.assertEqual(linhas[-2:], ["## Descartadas", "- [-] N"])

    def test_resolve_frente_por_sufixo_unico(self):
        frentes = [desk.Frente("dgolabs/noesis", Path("x")), desk.Frente("simcaq", Path("y"))]
        self.assertEqual(desk.resolver_frente(frentes, "noesis").id, "dgolabs/noesis")
        self.assertEqual(desk.resolver_frente(frentes, "simcaq").id, "simcaq")
        with self.assertRaises(ValueError):
            desk.resolver_frente(frentes, "nada")

    def test_sufixo_ambiguo_recusado(self):
        frentes = [desk.Frente("a/x", Path("1")), desk.Frente("b/x", Path("2"))]
        with self.assertRaises(ValueError):
            desk.resolver_frente(frentes, "x")

    def test_gravar_atomico(self):
        with tempfile.TemporaryDirectory() as tmp:
            arq = Path(tmp) / "P.md"
            desk.gravar_atomico(arq, "oi\n")
            self.assertEqual(arq.read_text(encoding="utf-8"), "oi\n")
            self.assertEqual([p.name for p in Path(tmp).iterdir()], ["P.md"])


if __name__ == "__main__":
    unittest.main()
