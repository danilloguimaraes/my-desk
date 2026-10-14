# Plano — Descarte de pendências e ingestão por ciclo de vida

> **Para agentes executores:** use `subagent-driven-development` (recomendado) ou `executing-plans`, tarefa por tarefa. Os passos usam checkbox (`- [ ]`) para acompanhamento.

Criado em 13/10/2026. Documento de definição temporário (fora do sistema modelado, como `VISAO.md`); apagar quando o plano estiver concluído e o conteúdo absorvido por `DOMINIO.md`, `ARQUITETURA.md` e `SOLUCAO.md`.

**Objetivo:** permitir alterar pendências já registradas (concluir, descartar, mudar prioridade, transferir a crítica, editar) sem editar markdown à mão, individualmente ou em lote.

**Arquitetura:** um núcleo de escrita puro (texto entra, texto sai) implementa as transições do ciclo de vida sobre `PENDENCIAS.md`. Dois clientes usam esse núcleo: os verbos (`desk feito`, `descartar`, `urgente`, `normal`, `critica`) para uma mudança, e `desk triagem` para muitas, num buffer do editor no estilo `git rebase -i`. Toda escrita é validada antes de gravar e só é recusada se *piorar* o estado.

**Tecnologia:** Python ≥ 3.10, stdlib apenas (AD-3), `unittest`.

---

## Decisões de design

| # | Decisão | Alternativa descartada | Motivo |
|---|---|---|---|
| D1 | `descartada` é uma terceira situação, terminal, ao lado de `concluída` | Marcar como concluída com nota | Concluir mentindo fere N2; o painel e o histórico precisam distinguir "feito" de "abandonado" |
| D2 | Descarte exige data e motivo; vive em `## Descartadas` com marca `- [-]` | Seção comum de encerradas; motivo opcional | Seção própria mantém `Concluídas` honesta; motivo evita relitigar (N6) e dá contexto na retomada (N4) |
| D3 | Pendência encerrada perde a marca `crítica` | Manter a marca no histórico | A crítica é um papel de item aberto (invariante 3); marca em item fechado só confunde leitura |
| D4 | Item é apontado por número efêmero (ordem do arquivo) ou trecho do texto, com menu quando ambíguo | ID fixo gravado no markdown | ID fixo polui o arquivo e exige migração; número vale para a versão atual do arquivo e a confirmação mostra a linha |
| D5 | Triagem mostra só pendências abertas; subseções `###` aparecem como comentário | Editar o arquivo inteiro | Histórico é imutável; prosa e subseções não são pendências e não devem ser reescritas |
| D6 | Apagar uma linha numerada no buffer é erro; buffer sem itens cancela | Apagar = descartar, ou apagar = ignorar | As duas leituras são plausíveis; ambiguidade em compromisso fere N3. Encerrar é sempre explícito |
| D7 | Linha sem número no buffer = pendência nova | Só permitir criar via `desk add` | A triagem é a sessão de fechamento; criar ali evita trocar de ferramenta |
| D8 | Reordenar dentro da seção não reordena o arquivo; mudar de seção insere no fim do bloco de topo (antes da primeira `###`) | Reordenar fiel ao buffer | Reordenação atravessaria subseções sem semântica no modelo; YAGNI |
| D9 | Encerradas entram no **topo** de `Concluídas`/`Descartadas` (mais recente primeiro) | Fim da seção | Convenção já usada nas frentes e em `DECISOES.md` |
| D10 | Validação bloqueia apenas erros **novos** (multiconjunto de mensagens antes × depois) | Bloquear qualquer erro | Frentes com legado inválido ficariam intrancáveis; a regra "não piorar" mais o portão de commit preservam N2 |
| D11 | Verbos e triagem têm forma não interativa (`--sim`, `--motivo`, `--exportar`/`--aplicar`) para o agente | Agente edita markdown direto | O agente é o segundo consumidor (Visão); argumentos aqui *selecionam* item, não capturam texto livre do usuário, então não contradizem AD-2 |
| D12 | `<frente>` aceita o id completo ou o último segmento quando único (`noesis` → `dgolabs/noesis`) | Só id completo | Atrito de digitação sem ambiguidade real |
| D13 | Leitura continua tolerante (campos livres legados, responsável ausente); escrita assistida exige responsável | Endurecer a leitura | Os dados atuais quebrariam em massa; o código já faz isso, os testes é que ficaram para trás |
| D14 | Não haverá verbo `desk editar`; edição de texto é feita na triagem | Verbo dedicado | A triagem já cobre com UX melhor; menos superfície |

## Mapa de arquivos

| Arquivo | Responsabilidade | Ação |
|---|---|---|
| `desk.py` | Modelo, leitura, verificação, renderização, CLI; primitivas `inserir_em_secao` e `gravar_atomico` | Modificar |
| `desk_escrita.py` | Itens abertos, transições (`Mudanca`), `reescrever`, validação "não piorar", seleção de item, verbos | Criar |
| `desk_triagem.py` | Buffer: renderizar, interpretar, aplicar, laço com editor, exportar/aplicar | Criar |
| `test_desk.py` | Testes de leitura/check/painel/add | Modificar |
| `test_escrita.py` | Testes do núcleo e dos verbos | Criar |
| `test_triagem.py` | Testes do buffer e do laço | Criar |
| `DOMINIO.md`, `ARQUITETURA.md`, `SOLUCAO.md`, `AGENTS.md` | Contratos | Modificar |
| `.githooks/pre-commit` | Portão AD-6 (hoje inexistente) | Criar |
| `dgolabs/noesis/PENDENCIAS.md` | Migrar 7 itens em lista numerada | Modificar |
| `../../dgolabs/my-skills/skill/desk-sync/SKILL.md` | Fechamento de sessão passa a usar triagem exportada | Modificar (outro repo) |

Comando de testes, usado em todas as tarefas: `python3 -m unittest -v` na raiz (descobre `test_*.py`).

## Ordem das tarefas

0. Pré-requisito: árvore de trabalho limpa (decisão do usuário)
1. Linha de base: testes alinhados ao código atual
2. Contrato de domínio: `descartada` em `DOMINIO.md`
3. Gramática: leitura de `[-]`, `Descartadas`, listas numeradas
4. Primitivas em `desk.py`: inserção por seção, gravação atômica, resolução de frente, numeração no `desk frente`
5. Núcleo de escrita: itens, `Mudanca`, `reescrever`, validação
6. Verbos: seleção, transições, CLI
7. Triagem I: renderizar buffer
8. Triagem II: interpretar e aplicar buffer
9. Triagem III: laço com editor, exportar/aplicar, CLI
10. Contratos: `ARQUITETURA.md`, `SOLUCAO.md`, `AGENTS.md`
11. Dados: migrar listas numeradas do Noesis
12. Portão: hook de pre-commit
13. Agente: `desk-sync` usa triagem exportada
14. Homologação com dados reais (pdc-1)

**Validação prévia (13/10/2026):** os blocos de código deste plano foram montados numa cópia descartável do repositório. Resultado: 73 testes verdes; com os dados reais, `desk check` denunciou as 7 listas numeradas do Noesis e a migração da Tarefa 11 zerou as inconsistências; a triagem por `--exportar`/`--aplicar` no `pdc-1` restaurado concluiu, descartou e transferiu a crítica com o painel refletindo a mudança. Defeito cosmético conhecido e aceito: seção criada pela escrita (`## Descartadas`) nasce sem linha em branco após o título.

---

### Tarefa 0: Árvore de trabalho limpa (decisão do usuário)

Há mudanças não commitadas em `README.md`, `SOLUCAO.md`, `mestrado/README.md`, `pdc-1/PENDENCIAS.md` e `simcaq/PENDENCIAS.md`. As tarefas 10 e 14 editam `SOLUCAO.md` e `pdc-1/PENDENCIAS.md`, então elas precisam estar resolvidas antes.

- [ ] **Passo 1:** O usuário decide o destino de cada arquivo. Dois pontos pedem atenção:
  - a versão em edição de `SOLUCAO.md` perdeu a acentuação ("Solucao", "decisao", "critica"); confirmar se é intencional antes de commitar;
  - `pdc-1/PENDENCIAS.md` teve 3 urgentes **apagadas**, incluindo a crítica, e por isso o `desk check` falha. É o caso real que este plano resolve. Recomendação: `git checkout pdc-1/PENDENCIAS.md` e encerrar os itens pela triagem na Tarefa 14.
- [ ] **Passo 2:** `git status --short` mostra só `__pycache__/` (adicionar ao `.gitignore` se desejado).

---

### Tarefa 1: Linha de base — testes alinhados ao código atual

O código evoluiu (campos livres legados tolerados, `concluída em` no lugar de `concluída:`, `monitoramento.md` aceito como legado) e 6 dos 25 testes falham. Sem base verde não há TDD.

**Arquivos:** modificar `test_desk.py`, `desk.py:164`

- [ ] **Passo 1: Confirmar a falha atual**

Run: `python3 -m unittest -v 2>&1 | tail -3`
Expected: `FAILED (failures=6)`

- [ ] **Passo 2: Ajustar os testes à gramática vigente**

Em `test_desk.py`:

```python
# PENDENCIAS_OK, linha 28
- [x] Entregar relatório — @Danillo — concluída em 2026-10-01
```

```python
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
```

```python
    def test_concluida_fora_de_concluidas(self):
        _, erros = desk.interpretar_pendencia("- [x] X — @D — concluída em 2026-10-01", "Em aberto", 1)
        self.assertTrue(any("fora de 'Concluídas'" in e for e in erros))
```

```python
    def test_artefato_nao_reconhecido(self):
        pasta = criar_frente(self.raiz, "frente-a")
        (pasta / "anotacoes.md").write_text("log", encoding="utf-8")
        self.assertTrue(any("artefato não reconhecido" in e for e in self.erros()))

    def test_artefato_legado_tolerado(self):
        pasta = criar_frente(self.raiz, "frente-a")
        (pasta / "monitoramento.md").write_text("log", encoding="utf-8")
        self.assertEqual(self.erros(), [])
```

- [ ] **Passo 3: Corrigir a mensagem que cita a gramática antiga**

Em `desk.py:164`, trocar `"pendência concluída sem 'concluída: AAAA-MM-DD'"` por `"pendência concluída sem 'concluída em AAAA-MM-DD'"`.

- [ ] **Passo 4: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3`
Expected: `OK` (26 testes)

- [ ] **Passo 5: Commit**

```bash
git add test_desk.py desk.py
git commit -m "desk: alinha testes à gramática vigente (linha de base verde)"
```

---

### Tarefa 2: Contrato de domínio — `descartada`

Mudança de contrato vem antes do código (regra dos documentos de definição).

**Arquivos:** modificar `DOMINIO.md`

- [ ] **Passo 1: Conceito Pendência** (tabela de Conceitos, linha "Pendência"), campos estruturados passam a ser:

```text
descrição, situação (`aberta`/`concluída`/`descartada`), prioridade (`urgente`/`normal`), responsável, prazo (opcional), origem (link, quando houver), crítica (`sim`/`não`), data de encerramento (conclusão ou descarte), motivo do descarte
```

- [ ] **Passo 2: Ciclo de vida**, substituir a linha da Pendência por:

```markdown
- **Pendência**: `aberta` → `concluída` (com data) **ou** `aberta` → `descartada` (com data e motivo). Prioridade e o papel de crítica podem mudar enquanto aberta. Concluída e descartada são terminais: permanecem como histórico, nunca reaparecem e nunca são apagadas.
```

- [ ] **Passo 3: Invariantes 2 e 3**, reescrever:

```markdown
2. Pendência encerrada (concluída ou descartada) não aparece como pendente em nenhuma projeção.
3. Toda frente ativa tem exatamente uma Pendência aberta marcada como crítica; pendência encerrada não carrega a marca.
```

- [ ] **Passo 4: Decisões resolvidas**, acrescentar:

```markdown
- **Descarte é uma situação própria, não uma conclusão.** Motivo: a Visão (necessidade 3) promete que nada some até ser "resolvido ou descartado por mim"; sem a situação, descartar exigia concluir mentindo ou apagar a linha — as duas ferem a necessidade 2. O motivo é obrigatório para que o descarte não seja relitigado (necessidade 6). Aprovado em 13/10/2026.
```

- [ ] **Passo 5: Commit**

```bash
git add DOMINIO.md
git commit -m "domínio: pendência descartada como situação terminal com motivo"
```

---

### Tarefa 3: Gramática — `[-]`, `## Descartadas` e listas numeradas

**Arquivos:** modificar `desk.py:17-25, 42-57, 127-190`; teste em `test_desk.py`

- [ ] **Passo 1: Testes que falham** (em `GramaticaTests` e `CheckTests`)

```python
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
```

```python
    def test_lista_numerada_e_denunciada(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n1. [ ] B — @D\n## Concluídas\n"))
        self.assertTrue(any("lista numerada" in e for e in self.erros()))

    def test_descartada_nao_conta_como_critica(self):
        criar_frente(self.raiz, "frente-a", pendencias=(
            "## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n## Concluídas\n## Descartadas\n"
            "- [-] B — @D — descartada em 2026-10-13 — motivo: m\n"))
        self.assertEqual(self.erros(), [])
```

Run: `python3 -m unittest test_desk -v 2>&1 | tail -3` → Expected: FAIL (6 novos)

- [ ] **Passo 2: Constantes** (substituem `desk.py:18` e `desk.py:25`)

```python
SECOES = ("Urgente", "Em aberto", "Concluídas", "Descartadas")
SECOES_ABERTAS = ("Urgente", "Em aberto")
MARCA_SITUACAO = {" ": "aberta", "x": "concluída", "-": "descartada"}
SECAO_FINAL = {"concluída": "Concluídas", "descartada": "Descartadas"}
PENDENCIA_RE = re.compile(r"^- \[( |x|-)\] (.+)$")
NUMERADA_RE = re.compile(r"^\s*\d+\. \[[ x-]\]")
```

- [ ] **Passo 3: `Pendencia`** (substitui `desk.py:42-56`; `aberta` vira propriedade derivada)

```python
@dataclass
class Pendencia:
    descricao: str
    secao: str
    linha: int
    situacao: str = "aberta"
    responsavel: str | None = None
    prazo: str | None = None
    origem: str | None = None
    critica: bool = False
    concluida_em: str | None = None
    descartada_em: str | None = None
    motivo: str | None = None

    @property
    def aberta(self) -> bool:
        return self.situacao == "aberta"

    @property
    def urgente(self) -> bool:
        return self.aberta and self.secao == "Urgente"
```

- [ ] **Passo 4: `interpretar_pendencia`** — no início, trocar a criação:

```python
    m = PENDENCIA_RE.match(linha)
    if m is None:
        return None, ["linha malformada: esperado '- [ ] ', '- [x] ' ou '- [-] ' no início"]
    partes = [p.strip() for p in m.group(2).split(SEPARADOR)]
    p = Pendencia(descricao=partes[0], secao=secao, linha=numero, situacao=MARCA_SITUACAO[m.group(1)])
```

No laço de campos, antes do `elif campo.startswith("origem: ")`, acrescentar:

```python
        elif campo.startswith("descartada em "):
            data_txt = campo[len("descartada em "):]
            if _eh_data(data_txt):
                p.descartada_em = _normalizar_data(data_txt)
            else:
                erros.append(f"data de descarte inválida: {data_txt}")
        elif campo.startswith("motivo: "):
            p.motivo = campo[len("motivo: "):].strip() or None
```

Substituir as quatro checagens finais (`if aberta and p.concluida_em` … `fora de 'Concluídas'`) por `erros += _coerencia(p)` e definir, logo acima da função:

```python
def _coerencia(p: Pendencia) -> list[str]:
    erros: list[str] = []
    if p.concluida_em and p.situacao != "concluída":
        erros.append(f"pendência {p.situacao} com data de conclusão")
    if p.descartada_em and p.situacao != "descartada":
        erros.append(f"pendência {p.situacao} com data de descarte")
    if p.situacao == "concluída" and not p.concluida_em:
        erros.append("pendência concluída sem 'concluída em AAAA-MM-DD'")
    if p.situacao == "descartada":
        if not p.descartada_em:
            erros.append("pendência descartada sem 'descartada em AAAA-MM-DD'")
        if not p.motivo:
            erros.append("pendência descartada sem 'motivo: ...'")
    esperada = SECAO_FINAL.get(p.situacao)
    if esperada is None and p.secao not in SECOES_ABERTAS:
        erros.append(f"pendência aberta em '{p.secao}'")
    if esperada and p.secao != esperada:
        erros.append(f"pendência {p.situacao} fora de '{esperada}' (está em '{p.secao}')")
    return erros
```

- [ ] **Passo 5: `ler_pendencias`** separa texto de arquivo (a validação da Tarefa 5 precisa ler texto em memória) e denuncia listas numeradas:

```python
def ler_pendencias_texto(texto: str, rel: str) -> tuple[list[Pendencia], list[Erro]]:
    pendencias: list[Pendencia] = []
    erros: list[Erro] = []
    secao = ""
    for numero, linha in enumerate(texto.splitlines(), start=1):
        if linha.startswith("## "):
            secao = linha[3:].strip()
            continue
        if NUMERADA_RE.match(linha):
            erros.append(Erro(rel, numero, "pendência em lista numerada: use '- [ ] ' (invisível ao painel)"))
            continue
        if not linha.lstrip().startswith("- ["):
            continue
        if secao not in SECOES:
            erros.append(Erro(rel, numero, f"pendência fora das seções {', '.join(SECOES)}"))
            continue
        pend, problemas = interpretar_pendencia(linha, secao, numero)
        erros += [Erro(rel, numero, msg) for msg in problemas]
        if pend:
            pendencias.append(pend)
    return pendencias, erros


def ler_pendencias(arquivo: Path, rel: str) -> tuple[list[Pendencia], list[Erro]]:
    return ler_pendencias_texto(arquivo.read_text(encoding="utf-8"), rel)
```

- [ ] **Passo 6: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`
Run: `./desk check` → Expected: passa a listar 7 erros "lista numerada" em `dgolabs/noesis` (corrigidos na Tarefa 11). Isso é o comportamento desejado: o que era invisível agora é denunciado.

- [ ] **Passo 7: Commit**

```bash
git add desk.py test_desk.py
git commit -m "desk: gramática de descarte e denúncia de pendências em lista numerada"
```

---

### Tarefa 4: Primitivas em `desk.py`

Quatro peças que verbos e triagem compartilham. Como efeito colateral, corrige um defeito do `desk add`: hoje ele insere no fim da seção, ou seja, dentro da última subseção `###` (em `dgolabs/noesis`, um item novo de "Em aberto" cairia sob "### Higiene").

**Arquivos:** modificar `desk.py` (`inserir_na_secao` em 355-368, `adicionar_pendencia` em 386-389, `renderizar_frente` em 308-321, `main` em 463-475); testes em `test_desk.py`

- [ ] **Passo 1: Testes que falham** (nova classe em `test_desk.py`)

```python
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
```

E em `PainelTests`:

```python
    def test_frente_numera_pendencias_abertas(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            criar_frente(raiz, "f", pendencias="## Urgente\n- [ ] A — @D — crítica\n## Em aberto\n- [ ] B — @D\n")
            frentes, erros = desk.carregar(raiz)
            saida = "\n".join(desk.renderizar_frente(frentes[0], erros))
            self.assertIn("1. [URGENTE] A — @D", saida)
            self.assertIn("2. B — @D", saida)
```

Run: `python3 -m unittest test_desk -v 2>&1 | tail -3` → Expected: FAIL (`AttributeError: ... 'inserir_em_secao'`)

- [ ] **Passo 2: `inserir_em_secao`** substitui `inserir_na_secao`

```python
def inserir_em_secao(linhas: list[str], secao: str, novas: list[str], topo: bool) -> list[str]:
    """Insere `novas` em `## secao`: no topo (encerradas, mais recente primeiro) ou no fim do
    bloco de topo, antes da primeira subseção `###`. Cria a seção no fim se não existir."""
    cabecalho = f"## {secao}"
    if cabecalho not in linhas:
        linhas = linhas + ["", cabecalho]
    i = linhas.index(cabecalho)
    fim = i + 1
    while fim < len(linhas) and not linhas[fim].startswith("## "):
        fim += 1
    if topo:
        k = i + 1
        while k < fim and (not linhas[k].strip() or linhas[k].lstrip().startswith("<!--")):
            k += 1
    else:
        k = next((j for j in range(i + 1, fim) if linhas[j].startswith("### ")), fim)
        while k > i + 1 and not linhas[k - 1].strip():
            k -= 1
    return linhas[:k] + novas + linhas[k:]
```

Nota: com `topo=True` numa seção vazia seguida de outra seção, `k` para no próximo `##`; isso está correto (insere antes dele).

- [ ] **Passo 3: `gravar_atomico`** (acrescentar `import os` no topo)

```python
def gravar_atomico(arquivo: Path, texto: str) -> None:
    tmp = arquivo.with_name(f".{arquivo.name}.tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, arquivo)
```

- [ ] **Passo 4: `adicionar_pendencia`** usa as primitivas (substitui as duas últimas linhas antes do `return`)

```python
    arquivo = frente.pasta / "PENDENCIAS.md"
    texto = arquivo.read_text(encoding="utf-8") if arquivo.is_file() else "# Pendências\n"
    linhas = inserir_em_secao(texto.splitlines(), "Urgente" if urgente else "Em aberto", [linha], topo=False)
    gravar_atomico(arquivo, "\n".join(linhas) + "\n")
    return linha
```

- [ ] **Passo 5: `resolver_frente`**

```python
def resolver_frente(frentes: list[Frente], texto: str) -> Frente:
    exata = next((f for f in frentes if f.id == texto), None)
    if exata:
        return exata
    por_sufixo = [f for f in frentes if f.id.rsplit("/", 1)[-1] == texto]
    if len(por_sufixo) == 1:
        return por_sufixo[0]
    if por_sufixo:
        raise ValueError(f"frente ambígua '{texto}': {', '.join(f.id for f in por_sufixo)}")
    raise ValueError(f"frente não encontrada: {texto}")
```

- [ ] **Passo 6: `renderizar_frente` numera** (a numeração é a mesma que verbos e triagem usam)

```python
    abertas = [p for p in f.pendencias if p.aberta and p.secao in SECOES_ABERTAS]
    linhas += ["", f"### Pendências abertas ({len(abertas)})"]
    linhas += [f"{n}. {'[URGENTE] ' if p.urgente else ''}{p.descricao}{_sufixo(p)}"
               for n, p in enumerate(abertas, start=1)]
```

- [ ] **Passo 7: `main`** — o comando `frente` usa `resolver_frente`, e o módulo se registra como `desk` para que `desk_escrita`/`desk_triagem` não carreguem uma segunda cópia quando o script roda como `__main__`:

```python
    if comando == "frente":
        try:
            f = resolver_frente(frentes, args.id)
        except ValueError as e:
            print(e)
            return 1
        print("\n".join(renderizar_frente(f, erros)))
        return 0
```

```python
if __name__ == "__main__":
    sys.modules.setdefault("desk", sys.modules[__name__])
    sys.exit(main())
```

- [ ] **Passo 8: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`
Run: `./desk frente noesis | head -12` → Expected: lista numerada `1. [URGENTE] Reconciliar status de **E10.2 #44** — @Danillo — 2026-09-26`

- [ ] **Passo 9: Commit**

```bash
git add desk.py test_desk.py
git commit -m "desk: primitivas de escrita, frente por sufixo e pendências numeradas"
```

---

### Tarefa 5: Núcleo de escrita — `desk_escrita.py`

O coração do plano: `reescrever` recebe o texto atual e um conjunto de mudanças desejadas por item e devolve o texto novo. Itens não mencionados ficam **byte a byte** intactos, assim como prosa, subseções e histórico. Não há reserialização de linha inteira: a escrita só troca a marca, acrescenta/remove campos e move a linha. Assim campos legados (links markdown, "bloqueia ...") nunca se perdem.

**Arquivos:** criar `desk_escrita.py`, `test_escrita.py`

- [ ] **Passo 1: Testes que falham** — criar `test_escrita.py`

```python
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
```

Run: `python3 -m unittest test_escrita -v 2>&1 | tail -3` → Expected: FAIL (`ModuleNotFoundError: desk_escrita`)

- [ ] **Passo 2: Esqueleto e modelo** — criar `desk_escrita.py`

```python
"""desk_escrita — transições do ciclo de vida da pendência sobre PENDENCIAS.md.

Funções puras sobre texto; gravar é responsabilidade do chamador. Contrato: SOLUCAO.md.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from typing import Callable

import desk

SITUACOES = ("aberta", "concluída", "descartada")


@dataclass
class Item:
    chave: int      # 1..n na ordem do arquivo; vale para a versão atual do texto
    indice: int     # índice 0-based da linha no texto
    secao: str
    conteudo: str   # tudo após '- [ ] '


@dataclass
class Mudanca:
    situacao: str   # uma de SITUACOES
    secao: str      # seção de destino enquanto aberta ("Urgente" | "Em aberto")
    conteudo: str   # campos desejados, sem marca de encerramento


def itens_abertos(texto: str) -> list[Item]:
    itens: list[Item] = []
    secao = ""
    for i, linha in enumerate(texto.splitlines()):
        if linha.startswith("## "):
            secao = linha[3:].strip()
        elif secao in desk.SECOES_ABERTAS and linha.startswith("- [ ] "):
            itens.append(Item(len(itens) + 1, i, secao, linha[6:]))
    return itens


def campos(conteudo: str) -> list[str]:
    return [c.strip() for c in conteudo.split(desk.SEPARADOR)]


def juntar(lista: list[str]) -> str:
    return desk.SEPARADOR.join(lista)


def sem_critica(conteudo: str) -> str:
    return juntar([c for c in campos(conteudo) if c != "crítica"]) if "crítica" in campos(conteudo) else conteudo


def com_critica(conteudo: str) -> str:
    return conteudo if "crítica" in campos(conteudo) else juntar(campos(conteudo) + ["crítica"])


def tem_motivo(conteudo: str) -> bool:
    return any(c.startswith("motivo: ") and c[len("motivo: "):].strip() for c in campos(conteudo))
```

Os testes de `Item` já passam; os demais continuam falhando.

- [ ] **Passo 3: `linha_de` e `reescrever`** (acrescentar ao fim de `desk_escrita.py`)

```python
def linha_de(m: Mudanca, hoje: date) -> str:
    if m.situacao == "aberta":
        return f"- [ ] {m.conteudo}"
    base = campos(sem_critica(m.conteudo))
    if m.situacao == "concluída":
        return "- [x] " + juntar(base + [f"concluída em {hoje.isoformat()}"])
    motivo = [c for c in base if c.startswith("motivo: ")]
    resto = [c for c in base if not c.startswith("motivo: ")]
    return "- [-] " + juntar(resto + [f"descartada em {hoje.isoformat()}"] + motivo)


def reescrever(texto: str, mudancas: dict[int, Mudanca], novas: list[Mudanca], hoje: date) -> str:
    """`mudancas`: chave do Item -> estado desejado. Itens ausentes ficam intactos."""
    if not mudancas and not novas:
        return texto
    linhas = texto.splitlines()
    por_chave = {it.chave: it for it in itens_abertos(texto)}
    destino: dict[str, list[str]] = {s: [] for s in desk.SECOES}
    remover: set[int] = set()
    for chave, m in mudancas.items():
        it = por_chave[chave]
        alvo = m.secao if m.situacao == "aberta" else desk.SECAO_FINAL[m.situacao]
        if alvo == it.secao:
            linhas[it.indice] = linha_de(m, hoje)
        else:
            remover.add(it.indice)
            destino[alvo].append(linha_de(m, hoje))
    destino_novas = [linha_de(m, hoje) for m in novas]
    linhas = [l for i, l in enumerate(linhas) if i not in remover]
    for secao in desk.SECOES:
        extras = destino[secao] + [l for l, m in zip(destino_novas, novas) if m.secao == secao]
        if extras:
            topo = secao in desk.SECAO_FINAL.values()
            linhas = desk.inserir_em_secao(linhas, secao, extras, topo=topo)
    return "\n".join(linhas) + "\n"
```

- [ ] **Passo 4: Validação "não piorar"** (acrescentar)

```python
def validar_texto(frente: desk.Frente, texto: str) -> list[desk.Erro]:
    rel = f"{frente.id}/PENDENCIAS.md"
    pendencias, erros = desk.ler_pendencias_texto(texto, rel)
    copia = desk.Frente(id=frente.id, pasta=frente.pasta, ficha=frente.ficha, pendencias=pendencias)
    return erros + desk.verificar_cruzado([copia])


def erros_novos(frente: desk.Frente, antes: str, depois: str) -> list[str]:
    """Mensagens que aparecem em `depois` e não em `antes` (multiconjunto; ignora nº de linha)."""
    contar = lambda t: Counter(err.mensagem for err in validar_texto(frente, t))
    return sorted((contar(depois) - contar(antes)).elements())
```

- [ ] **Passo 5: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`

- [ ] **Passo 6: Commit**

```bash
git add desk_escrita.py test_escrita.py
git commit -m "desk: núcleo de escrita por transições do ciclo de vida"
```

---

### Tarefa 6: Verbos — `feito`, `descartar`, `urgente`, `normal`, `critica`

Forma de uso: `desk <verbo> <frente> [nº | trecho...] [--sim] [--motivo TEXTO]`. Sem alvo, abre menu com todas as abertas. Trecho único seleciona direto; ambíguo abre menu (ou falha em `--sim`). Sempre mostra a linha antes/depois e pede confirmação, exceto com `--sim`. Se o verbo encerra a crítica de uma frente ativa, pergunta qual passa a ser a crítica (em `--sim`, falha e orienta).

**Arquivos:** modificar `desk_escrita.py`, `desk.py` (`main`); testes em `test_escrita.py`

- [ ] **Passo 1: Testes que falham** (acrescentar a `test_escrita.py`)

```python
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
```

Run: `python3 -m unittest test_escrita -v 2>&1 | tail -3` → Expected: FAIL (`AttributeError: ... 'executar'`)

- [ ] **Passo 2: Seleção e menu** (acrescentar a `desk_escrita.py`)

```python
def selecionar(itens: list[Item], alvo: str | None, escolher: Callable[[list[Item]], Item]) -> Item:
    if not itens:
        raise ValueError("a frente não tem pendências abertas")
    if alvo and alvo.isdigit():
        achado = next((it for it in itens if it.chave == int(alvo)), None)
        if achado is None:
            raise ValueError(f"não há pendência aberta nº {alvo} (veja `desk frente`)")
        return achado
    candidatos = [it for it in itens if not alvo or alvo.casefold() in it.conteudo.casefold()]
    if not candidatos:
        raise ValueError(f"nenhuma pendência aberta contém '{alvo}'")
    return candidatos[0] if len(candidatos) == 1 else escolher(candidatos)


def menu(candidatos: list[Item], entrada: Callable[[str], str], saida: Callable[[str], None]) -> Item:
    for n, it in enumerate(candidatos, start=1):
        saida(f"  {n}. [{it.secao}] {it.conteudo}")
    while True:
        resposta = entrada("Qual? (nº): ").strip()
        if resposta.isdigit() and 1 <= int(resposta) <= len(candidatos):
            return candidatos[int(resposta) - 1]
        saida(f"  ! responda um número de 1 a {len(candidatos)}")


def sem_escolha(candidatos: list[Item]) -> Item:
    lista = "; ".join(f"{it.chave}: {it.conteudo}" for it in candidatos)
    raise ValueError(f"{len(candidatos)} pendências casam com o trecho; use o nº. {lista}")
```

- [ ] **Passo 3: Transições** (acrescentar)

```python
def transicao(verbo: str, it: Item, itens: list[Item], motivo: str | None) -> dict[int, Mudanca]:
    if verbo == "feito":
        return {it.chave: Mudanca("concluída", it.secao, it.conteudo)}
    if verbo == "descartar":
        return {it.chave: Mudanca("descartada", it.secao, juntar(campos(it.conteudo) + [f"motivo: {motivo}"]))}
    if verbo in ("urgente", "normal"):
        secao = "Urgente" if verbo == "urgente" else "Em aberto"
        return {it.chave: Mudanca("aberta", secao, it.conteudo)}
    if verbo == "critica":
        mudancas = {o.chave: Mudanca("aberta", o.secao, sem_critica(o.conteudo))
                    for o in itens if o.chave != it.chave and "crítica" in campos(o.conteudo)}
        mudancas[it.chave] = Mudanca("aberta", it.secao, com_critica(it.conteudo))
        return mudancas
    raise ValueError(f"verbo desconhecido: {verbo}")
```

- [ ] **Passo 4: `executar`** (acrescentar)

```python
VERBOS = ("feito", "descartar", "urgente", "normal", "critica")


def executar(verbo: str, frente: desk.Frente, alvo: str | None, *, motivo: str | None = None,
             sim: bool = False, hoje: date | None = None, entrada: Callable[[str], str] = input,
             saida: Callable[[str], None] = print) -> int:
    hoje = hoje or date.today()
    arquivo = frente.pasta / "PENDENCIAS.md"
    texto = arquivo.read_text(encoding="utf-8")
    itens = itens_abertos(texto)
    escolher = sem_escolha if sim else (lambda c: menu(c, entrada, saida))
    it = selecionar(itens, alvo, escolher)

    if verbo == "descartar" and not (motivo and motivo.strip()):
        if sim:
            raise ValueError("descartar exige --motivo em modo --sim")
        while not (motivo := entrada("Motivo do descarte: ").strip()):
            saida("  ! o motivo é obrigatório")
    mudancas = transicao(verbo, it, itens, motivo)

    encerra_critica = verbo in ("feito", "descartar") and "crítica" in campos(it.conteudo)
    if encerra_critica and frente.situacao == "ativa":
        outros = [o for o in itens if o.chave != it.chave]
        if sim or not outros:
            raise ValueError(f"'{it.conteudo}' é a crítica de {frente.id}; "
                             f"rode `desk critica {frente.id} <nº>` antes")
        saida(f"Este item é a crítica de {frente.id}. Qual passa a ser a crítica?")
        sucessora = menu(outros, entrada, saida)
        mudancas[sucessora.chave] = Mudanca("aberta", sucessora.secao, com_critica(sucessora.conteudo))

    novo = reescrever(texto, mudancas, [], hoje)
    problemas = erros_novos(frente, texto, novo)
    if problemas:  # valida antes de pedir confirmação: não se confirma o que será recusado
        saida("recusado: a mudança criaria inconsistência(s):")
        for p in problemas:
            saida(f"  ! {p}")
        return 1
    for chave, m in mudancas.items():
        saida(f"  - {itens[chave - 1].conteudo}\n  + {linha_de(m, hoje)[6:]}  [{m.situacao}]")
    if not sim and entrada("Confirmar? [S/n]: ").strip().lower() not in ("", "s", "sim"):
        saida("nada foi gravado")
        return 1
    desk.gravar_atomico(arquivo, novo)
    saida(f"ok: {frente.id}/PENDENCIAS.md atualizado")
    return 0
```

Nota: `itens[chave - 1]` é válido porque `chave` é a posição 1-based em `itens`.

- [ ] **Passo 5: CLI** — em `desk.main`, registrar os subcomandos (após `add`):

```python
    for verbo, ajuda in (("feito", "conclui uma pendência"), ("descartar", "descarta uma pendência, com motivo"),
                         ("urgente", "move para Urgente"), ("normal", "move para Em aberto"),
                         ("critica", "transfere a marca de crítica da frente")):
        p = sub.add_parser(verbo, help=ajuda)
        p.add_argument("frente")
        p.add_argument("alvo", nargs="*", help="nº de `desk frente` ou trecho do texto; vazio = menu")
        p.add_argument("--sim", action="store_true", help="não pergunta (uso por agentes)")
        if verbo == "descartar":
            p.add_argument("--motivo")
```

E o despacho, logo após `frentes, erros = carregar(RAIZ)`:

```python
    if comando in ("feito", "descartar", "urgente", "normal", "critica"):
        import desk_escrita
        try:
            f = resolver_frente(frentes, args.frente)
            return desk_escrita.executar(comando, f, " ".join(args.alvo) or None,
                                         motivo=getattr(args, "motivo", None), sim=args.sim)
        except ValueError as e:
            print(f"erro: {e}")
            return 1
```

- [ ] **Passo 6: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`
Run: `./desk feito noesis 999 --sim; echo $?` → Expected: `erro: não há pendência aberta nº 999 (veja \`desk frente\`)` e `1`

- [ ] **Passo 7: Commit**

```bash
git add desk.py desk_escrita.py test_escrita.py
git commit -m "desk: verbos feito, descartar, urgente, normal e critica"
```

---

### Tarefa 7: Triagem I — renderizar o buffer

Formato do buffer (contrato; vai para `SOLUCAO.md` na Tarefa 10):

```text
# desk triagem dgolabs/noesis — versão 3f9a1c07
# Marcas: [ ] aberta · [x] concluir hoje · [-] descartar (exige '— motivo: ...')
# Mover a linha para a outra seção muda a prioridade. '— crítica' marca a crítica da frente.
# Linha sem número = pendência nova (exige @responsável). Apagar linha numerada é erro.
# Remover todas as linhas de item cancela. Linhas iniciadas por '#' são ignoradas.

## Urgente
1 [ ] Reconciliar status de **E10.2 #44** — @Danillo — 2026-09-26 — crítica

## Em aberto
# ### Bloqueio de infraestrutura (Terminus)
2 [ ] **#87** Publicar imagem multi-arch no GHCR — ...
```

O número à esquerda é a chave do item nesta versão do arquivo; a versão é o início do SHA-256 do `PENDENCIAS.md` e protege contra aplicar um buffer velho.

**Arquivos:** criar `desk_triagem.py`, `test_triagem.py`

- [ ] **Passo 1: Teste que falha** — criar `test_triagem.py`

```python
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
```

Run: `python3 -m unittest test_triagem -v 2>&1 | tail -3` → Expected: FAIL (`ModuleNotFoundError: desk_triagem`)

- [ ] **Passo 2: Implementação** — criar `desk_triagem.py`

```python
"""desk_triagem — revisão em lote das pendências abertas de uma frente, num buffer de editor.

Contrato do buffer: SOLUCAO.md. As transições são as de desk_escrita.
"""
from __future__ import annotations

import hashlib
import os
import re
import shlex
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable

import desk
import desk_escrita as esc

LINHA_RE = re.compile(r"^(?:(\d+)\s+)?\[( |x|-)\]\s+(.+?)\s*$")
VERSAO_RE = re.compile(r"^# desk triagem (\S+) — versão ([0-9a-f]{8})$")
MARCA_ERRO = "# ! "
AJUDA = [
    "# Marcas: [ ] aberta · [x] concluir hoje · [-] descartar (exige '— motivo: ...')",
    "# Mover a linha para a outra seção muda a prioridade. '— crítica' marca a crítica da frente.",
    "# Linha sem número = pendência nova (exige @responsável). Apagar linha numerada é erro.",
    "# Remover todas as linhas de item cancela. Linhas iniciadas por '#' são ignoradas.",
]


def versao(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:8]


def renderizar_buffer(frente_id: str, texto: str) -> str:
    itens = {it.indice: it for it in esc.itens_abertos(texto)}
    blocos: dict[str, list[str]] = {s: [] for s in desk.SECOES_ABERTAS}
    secao = ""
    for i, linha in enumerate(texto.splitlines()):
        if linha.startswith("## "):
            secao = linha[3:].strip()
        elif secao in blocos and linha.startswith("### "):
            blocos[secao].append(f"# {linha}")
        elif i in itens:
            blocos[itens[i].secao].append(f"{itens[i].chave} [ ] {itens[i].conteudo}")
    saida = [f"# desk triagem {frente_id} — versão {versao(texto)}", *AJUDA]
    for s in desk.SECOES_ABERTAS:
        saida += ["", f"## {s}", *blocos[s]]
    return "\n".join(saida) + "\n"
```

- [ ] **Passo 3: Rodar** — `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`

- [ ] **Passo 4: Commit**

```bash
git add desk_triagem.py test_triagem.py
git commit -m "desk: triagem — renderização do buffer"
```

---

### Tarefa 8: Triagem II — interpretar e aplicar o buffer

Erros citam o item pelo número (ou pelo texto, se for linha nova), não pelo número da linha do buffer: assim continuam corretos depois que as anotações de erro são inseridas no topo.

**Arquivos:** modificar `desk_triagem.py`, `test_triagem.py`

- [ ] **Passo 1: Testes que falham** (acrescentar a `test_triagem.py`)

```python
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
```

Run: `python3 -m unittest test_triagem -v 2>&1 | tail -3` → Expected: FAIL

- [ ] **Passo 2: `Leitura` e `interpretar_buffer`** (acrescentar a `desk_triagem.py`)

```python
@dataclass
class Leitura:
    mudancas: dict[int, esc.Mudanca] = field(default_factory=dict)
    novas: list[esc.Mudanca] = field(default_factory=list)
    erros: list[str] = field(default_factory=list)
    cancelado: bool = False


def interpretar_buffer(buffer: str, itens: list[esc.Item]) -> Leitura:
    por_chave = {it.chave: it for it in itens}
    r, vistas, secao, algum = Leitura(), set(), None, False
    for bruta in buffer.splitlines():
        linha = bruta.strip()
        if linha.startswith("## "):
            nome = linha[3:].strip()
            secao = nome if nome in desk.SECOES_ABERTAS else None
            if secao is None:
                r.erros.append(f"seção desconhecida '{nome}' (use Urgente ou Em aberto)")
            continue
        if not linha or linha.startswith("#"):
            continue
        m = LINHA_RE.match(linha)
        if not m:
            r.erros.append(f"'{linha[:50]}': esperado '<nº> [ ] texto' ou '[ ] texto'")
            continue
        algum = True
        chave, situacao, conteudo = m.group(1), desk.MARCA_SITUACAO[m.group(2)], m.group(3)
        ref = f"nº {chave}" if chave else f"'{linha[:50]}'"
        if chave is not None:
            k = int(chave)
            if k not in por_chave:
                r.erros.append(f"{ref}: não existe nesta versão do arquivo")
                continue
            if k in vistas:
                r.erros.append(f"{ref}: repetido")
                continue
            vistas.add(k)
        if secao is None:
            r.erros.append(f"{ref}: item fora de '## Urgente' ou '## Em aberto'")
            continue
        if situacao == "descartada" and not esc.tem_motivo(conteudo):
            r.erros.append(f"{ref}: descarte exige '— motivo: ...'")
            continue
        if chave is None:
            if situacao != "aberta":
                r.erros.append(f"{ref}: pendência nova não nasce encerrada")
            elif not any(c.startswith("@") and len(c) > 1 for c in esc.campos(conteudo)[1:]):
                r.erros.append(f"{ref}: pendência nova exige '— @responsável'")
            else:
                r.novas.append(esc.Mudanca("aberta", secao, conteudo))
            continue
        it = por_chave[int(chave)]
        if situacao == "aberta" and secao == it.secao and conteudo == it.conteudo.strip():
            continue
        r.mudancas[int(chave)] = esc.Mudanca(situacao, secao, conteudo)
    if not algum:
        return Leitura(cancelado=True)
    faltando = sorted(set(por_chave) - vistas)
    if faltando:
        r.erros.append(f"nº {', '.join(map(str, faltando))} sumiram do buffer; para encerrar use [x] ou [-]")
    return r
```

- [ ] **Passo 3: `aplicar_buffer` e `resumir`** (acrescentar)

```python
def aplicar_buffer(frente: desk.Frente, texto: str, buffer: str,
                   hoje: date) -> tuple[str | None, list[str], Leitura]:
    """(texto novo, erros, leitura). Texto None = cancelado; com erros, nada deve ser gravado."""
    leitura = interpretar_buffer(buffer, esc.itens_abertos(texto))
    if leitura.cancelado:
        return None, [], leitura
    if leitura.erros:
        return texto, leitura.erros, leitura
    novo = esc.reescrever(texto, leitura.mudancas, leitura.novas, hoje)
    return novo, esc.erros_novos(frente, texto, novo), leitura


def resumir(leitura: Leitura) -> str:
    rotulos = (("concluída", "concluída(s)"), ("descartada", "descartada(s)"), ("aberta", "alterada(s)"))
    partes = [f"{n} {rotulo}" for situacao, rotulo in rotulos
              if (n := sum(m.situacao == situacao for m in leitura.mudancas.values()))]
    if leitura.novas:
        partes.append(f"{len(leitura.novas)} nova(s)")
    return ", ".join(partes) or "nada mudou"
```

- [ ] **Passo 4: Rodar** — `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`

- [ ] **Passo 5: Commit**

```bash
git add desk_triagem.py test_triagem.py
git commit -m "desk: triagem — interpretação e aplicação do buffer"
```

---

### Tarefa 9: Triagem III — laço com editor, exportar/aplicar e CLI

Uso humano: `desk triagem <frente>` abre `$VISUAL`/`$EDITOR` (padrão `vi`). Se houver erro, o editor reabre com o buffer do usuário preservado e os erros no topo como `# ! ...`. Remover todos os itens ou sair do editor com erro cancela. Antes de gravar, confere se o arquivo não mudou durante a edição.

Uso por agente: `desk triagem <frente> --exportar > buf.md`, editar, mostrar ao usuário, `desk triagem <frente> --aplicar buf.md` (ou `-` para stdin). A versão no cabeçalho impede aplicar sobre um arquivo que mudou.

**Arquivos:** modificar `desk_triagem.py`, `desk.py` (`main`), `test_triagem.py`

- [ ] **Passo 1: Testes que falham** (acrescentar a `test_triagem.py`)

```python
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
```

Run: `python3 -m unittest test_triagem -v 2>&1 | tail -3` → Expected: FAIL

- [ ] **Passo 2: Editor e anotações** (acrescentar a `desk_triagem.py`)

```python
class Cancelado(Exception):
    pass


def editor_do_sistema(buffer: str) -> str:
    comando = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vi"
    with tempfile.NamedTemporaryFile("w", suffix=".desk-triagem.md", delete=False, encoding="utf-8") as f:
        f.write(buffer)
        caminho = f.name
    try:
        if subprocess.run([*shlex.split(comando), caminho]).returncode != 0:
            raise Cancelado("o editor saiu com erro")
        return Path(caminho).read_text(encoding="utf-8")
    finally:
        os.unlink(caminho)


def remover_erros(buffer: str) -> str:
    return "".join(l for l in buffer.splitlines(keepends=True) if not l.startswith(MARCA_ERRO))


def anotar_erros(buffer: str, erros: list[str]) -> str:
    linhas = buffer.splitlines()
    k = 1 if linhas and linhas[0].startswith("# desk triagem") else 0
    return "\n".join(linhas[:k] + [f"{MARCA_ERRO}{e}" for e in erros] + linhas[k:]) + "\n"
```

- [ ] **Passo 3: `triar`, `exportar`, `aplicar_arquivo`** (acrescentar)

```python
def _gravar(frente: desk.Frente, texto: str, novo: str, leitura: Leitura,
            saida: Callable[[str], None]) -> int:
    arquivo = frente.pasta / "PENDENCIAS.md"
    if novo == texto:
        saida("nada mudou")
        return 0
    if arquivo.read_text(encoding="utf-8") != texto:
        saida("recusado: PENDENCIAS.md mudou durante a triagem; rode de novo")
        return 1
    desk.gravar_atomico(arquivo, novo)
    saida(f"ok: {frente.id} — {resumir(leitura)}")
    return 0


def triar(frente: desk.Frente, editar: Callable[[str], str] = editor_do_sistema,
          hoje: date | None = None, saida: Callable[[str], None] = print) -> int:
    hoje = hoje or date.today()
    texto = (frente.pasta / "PENDENCIAS.md").read_text(encoding="utf-8")
    buffer = renderizar_buffer(frente.id, texto)
    while True:
        try:
            buffer = remover_erros(editar(buffer))
        except Cancelado as e:
            saida(f"triagem cancelada ({e}); nada foi gravado")
            return 1
        novo, erros, leitura = aplicar_buffer(frente, texto, buffer, hoje)
        if novo is None:
            saida("triagem cancelada; nada foi gravado")
            return 1
        if not erros:
            return _gravar(frente, texto, novo, leitura, saida)
        buffer = anotar_erros(buffer, erros)


def exportar(frente: desk.Frente) -> str:
    return renderizar_buffer(frente.id, (frente.pasta / "PENDENCIAS.md").read_text(encoding="utf-8"))


def aplicar_arquivo(frente: desk.Frente, buffer: str, hoje: date | None = None,
                    saida: Callable[[str], None] = print) -> int:
    texto = (frente.pasta / "PENDENCIAS.md").read_text(encoding="utf-8")
    primeira = buffer.splitlines()[0] if buffer.strip() else ""
    m = VERSAO_RE.match(primeira)
    if not m or m.group(1) != frente.id:
        saida(f"recusado: o buffer não tem o cabeçalho de triagem de {frente.id}")
        return 1
    if m.group(2) != versao(texto):
        saida("recusado: PENDENCIAS.md mudou desde a exportação; exporte de novo")
        return 1
    novo, erros, leitura = aplicar_buffer(frente, texto, remover_erros(buffer), hoje or date.today())
    if novo is None:
        saida("buffer sem itens: nada foi gravado")
        return 1
    if erros:
        for e in erros:
            saida(f"  ! {e}")
        return 1
    return _gravar(frente, texto, novo, leitura, saida)
```

- [ ] **Passo 4: CLI** — em `desk.main`, registrar (após os verbos):

```python
    p_tri = sub.add_parser("triagem", help="revisa em lote as pendências abertas de uma frente no editor")
    p_tri.add_argument("frente")
    modo = p_tri.add_mutually_exclusive_group()
    modo.add_argument("--exportar", action="store_true", help="imprime o buffer (uso por agentes)")
    modo.add_argument("--aplicar", metavar="ARQUIVO", help="aplica um buffer editado; '-' lê da entrada padrão")
```

E o despacho, junto ao dos verbos:

```python
    if comando == "triagem":
        import desk_triagem
        try:
            f = resolver_frente(frentes, args.frente)
        except ValueError as e:
            print(f"erro: {e}")
            return 1
        if args.exportar:
            print(desk_triagem.exportar(f), end="")
            return 0
        if args.aplicar:
            buffer = sys.stdin.read() if args.aplicar == "-" else Path(args.aplicar).read_text(encoding="utf-8")
            return desk_triagem.aplicar_arquivo(f, buffer)
        return desk_triagem.triar(f)
```

- [ ] **Passo 5: Rodar**

Run: `python3 -m unittest -v 2>&1 | tail -3` → Expected: `OK`
Run: `./desk triagem noesis --exportar | head -8` → Expected: cabeçalho `# desk triagem dgolabs/noesis — versão ........` e `1 [ ] Reconciliar status de **E10.2 #44** ...`
Run: `EDITOR=true ./desk triagem noesis` → Expected: `nada mudou` (o editor `true` não altera o arquivo)

- [ ] **Passo 6: Commit**

```bash
git add desk.py desk_triagem.py test_triagem.py
git commit -m "desk: triagem em lote no editor, com exportar/aplicar para agentes"
```

---

### Tarefa 10: Contratos — `ARQUITETURA.md`, `SOLUCAO.md`, `AGENTS.md`, `README.md`

Depende da Tarefa 0 (a versão de `SOLUCAO.md` em edição precisa estar resolvida).

**Arquivos:** modificar `ARQUITETURA.md`, `SOLUCAO.md`, `AGENTS.md`, `README.md`

- [ ] **Passo 1: `ARQUITETURA.md`** — acrescentar às decisões arquiteturais:

```markdown
- **AD-7 · Ingestão cobre o ciclo de vida, não só o nascimento.** A via assistida ganha verbos de transição (concluir, descartar, mudar prioridade, transferir a crítica) e uma triagem em lote num buffer de editor; ambos compartilham um núcleo de escrita que valida o resultado e recusa apenas o que piora o estado. Argumentos de linha de comando são aceitos para *selecionar* itens e para uso por agentes (`--sim`, `--exportar`/`--aplicar`); isso não reabre a alternativa descartada em AD-2, que tratava da *captura* de texto livre. Motivo: com escrita só na criação, toda alteração caía na edição direta, que AD-2 define como saída de emergência. Aprovado em 13/10/2026.
```

E, na tabela de Componentes, linha **Ingestão**, acrescentar ao fim do papel: `; cobre criação e transições (AD-7)`.

- [ ] **Passo 2: `SOLUCAO.md`** — atualizar:
  - **Referência rápida**: acrescentar linhas para `desk feito|descartar|urgente|normal|critica <frente> [nº|trecho]` ("Quando uma pendência muda de situação, prioridade ou crítica") e `desk triagem <frente>` ("No fechamento de sessão ou revisão da frente"); nota de que `<frente>` aceita o último segmento quando único.
  - **Seção de cada comando novo**, com o comportamento descrito nas Tarefas 6 e 9 (seleção, menu, confirmação, sucessora da crítica, `--sim`, `--motivo`, `--exportar`, `--aplicar`).
  - **`desk frente`**: as pendências abertas saem numeradas; o número é o mesmo usado pelos verbos e pela triagem e vale para a versão atual do arquivo.
  - **Gramática de pendência**: seções `## Urgente | ## Em aberto | ## Concluídas | ## Descartadas` e a linha `- [-] Descrição — @Responsável — descartada em AAAA-MM-DD — motivo: <texto>`; regra "encerrada não carrega `crítica`"; regra "lista numerada não é pendência e é denunciada pelo check".
  - **Formato do buffer de triagem**: o bloco de exemplo da Tarefa 7 mais as regras D5–D8.
  - **Erros comuns**: linhas para `pendência em lista numerada`, `pendência descartada sem 'motivo: ...'` e `... sumiram do buffer`.

- [ ] **Passo 3: `AGENTS.md`** — em "Regras ao registrar", substituir a regra 4 e acrescentar a 7:

```markdown
4. **Pendência encerrada não é apagada.** Concluída vai para "Concluídas" com `concluída em AAAA-MM-DD`; descartada vai para "Descartadas" com `descartada em AAAA-MM-DD — motivo: ...`.
7. **Agente altera pendências pelo `desk`, não pelo markdown.** Mudança pontual: `desk <verbo> <frente> <nº> --sim`. Várias mudanças: `desk triagem <frente> --exportar`, editar o buffer, mostrar ao usuário, `desk triagem <frente> --aplicar <arquivo>`. Edição direta de `PENDENCIAS.md` é saída de emergência.
```

E remover a regra 2 ("Painel raiz espelha o urgente"), ver Passo 4.

- [ ] **Passo 4: Espelho de urgentes (decisão do usuário)** — com verbos movendo urgência sem tocar no `README.md` raiz, o espelho em "Pendências urgentes (todas as frentes)" passa a mentir na primeira mudança (fere N2). AD-1 já decidiu que ele deve morrer; o `desk` é o painel. Recomendação: remover a seção do `README.md` raiz e a regra 2 do `AGENTS.md` nesta tarefa, deixando a tabela de frentes para a migração de AD-1. Se o usuário preferir adiar, registrar a pendência no lugar.

- [ ] **Passo 5: Commit**

```bash
git add ARQUITETURA.md SOLUCAO.md AGENTS.md README.md
git commit -m "contratos: AD-7, comandos de transição e triagem, regra do agente"
```

---

### Tarefa 11: Dados — migrar as listas numeradas do Noesis

As 7 pendências do épico E11 estão como `1. [ ] ...` e eram invisíveis ao painel; desde a Tarefa 3 o check as denuncia. A ordem por valor é preservada pela própria ordem das linhas (o texto "Ordem sugerida por valor" acima delas continua válido).

**Arquivos:** modificar `dgolabs/noesis/PENDENCIAS.md`

- [ ] **Passo 1: Converter**

Run: `sed -i -E 's/^[0-9]+\. \[ \] /- [ ] /' dgolabs/noesis/PENDENCIAS.md && git diff --stat dgolabs/noesis/PENDENCIAS.md`
Expected: `1 file changed, 7 insertions(+), 7 deletions(-)`

- [ ] **Passo 2: Verificar**

Run: `./desk check`
Expected: `ok: nenhuma inconsistência` (supondo a Tarefa 0 resolvida para `pdc-1`)
Run: `./desk frente noesis | grep -c 'E11\.'` → Expected: `7`

- [ ] **Passo 3: Commit**

```bash
git add dgolabs/noesis/PENDENCIAS.md
git commit -m "noesis: pendências do E11 em lista canônica (estavam invisíveis ao painel)"
```

---

### Tarefa 12: Portão — hook de pre-commit (AD-6)

`SOLUCAO.md` descreve o hook, mas `.githooks/` não existe; foi por isso que `pdc-1` pôde ficar sem crítica sem que nada avisasse.

**Arquivos:** criar `.githooks/pre-commit`

- [ ] **Passo 1: Criar o hook**

```sh
#!/usr/bin/env sh
# Portão AD-6: estado inválido não entra no repositório.
exec "$(git rev-parse --show-toplevel)/desk" check
```

Run: `chmod +x .githooks/pre-commit && ./.githooks/pre-commit; echo $?` → Expected: `ok: nenhuma inconsistência` e `0`

- [ ] **Passo 2: Ativar (o usuário roda; configuração local do clone)**

```bash
git config core.hooksPath .githooks
```

- [ ] **Passo 3: Commit**

```bash
git add .githooks/pre-commit
git commit -m "desk: instala o portão de pre-commit (AD-6)"
```

---

### Tarefa 13: Agente — `desk-sync` passa a usar a triagem

O fechamento de sessão da skill `desk-sync` é hoje o principal canal de escrita em `PENDENCIAS.md` e edita o markdown diretamente. Esta tarefa troca isso pela triagem exportada, que é a via conversada da AD-2 com a gramática verificada.

**Arquivos:** modificar `/home/danillo/workspace/dgolabs/my-skills/skill/desk-sync/SKILL.md` (outro repositório)

- [ ] **Passo 1: Passo 5 do fechamento** — substituir as linhas "Pendências novas → `PENDENCIAS.md`" e "Pendências concluídas" por:

```markdown
   - **Pendências (novas, concluídas, descartadas, mudança de prioridade ou de crítica):** nunca editar `PENDENCIAS.md` à mão. Rodar `$DESK_ROOT/desk triagem <projeto> --exportar > /tmp/opencode/triagem-<projeto>.md`, editar o buffer (`[x]` conclui, `[-] ... — motivo: ...` descarta, mover de seção muda prioridade, linha sem número cria), mostrar ao usuário o buffer editado e, após aprovação, rodar `$DESK_ROOT/desk triagem <projeto> --aplicar /tmp/opencode/triagem-<projeto>.md`. Se o comando recusar, corrigir o buffer conforme os erros e repetir.
```

- [ ] **Passo 2: Espelhamento raiz** — se a Tarefa 10, Passo 4, removeu o espelho, apagar a linha "Espelhamento raiz" do passo 5.

- [ ] **Passo 3: Regras invioláveis** — substituir "Nunca apagar pendências concluídas — move para "Concluídas"." por:

```markdown
- Nunca apagar pendências: encerrar com `[x]` (concluída) ou `[-]` com motivo (descartada), sempre via `desk triagem` ou verbos do `desk`.
```

- [ ] **Passo 4: Commit** (no repositório `my-skills`)

```bash
git -C /home/danillo/workspace/dgolabs/my-skills add skill/desk-sync/SKILL.md
git -C /home/danillo/workspace/dgolabs/my-skills commit -m "desk-sync: fechamento usa desk triagem em vez de editar PENDENCIAS.md"
```

---

### Tarefa 14: Homologação com dados reais

Critério: os três cenários abaixo funcionam sem abrir `PENDENCIAS.md` no editor de texto comum, e `desk check` termina verde.

- [ ] **Cenário A — o caso que motivou o plano (pdc-1):** `./desk triagem pdc-1`; encerrar as três urgentes restauradas na Tarefa 0 com `[x]` ou `[-] — motivo: ...`, conforme a realidade; marcar `— crítica` em uma das abertas. Esperado: `ok: pdc-1 — ...`; `./desk` mostra a nova próxima ação crítica do PDC 1.
- [ ] **Cenário B — verbo pontual:** `./desk frente noesis`, escolher um item e `./desk feito noesis <nº>`. Esperado: diff mostra a linha movida para o topo de "Concluídas" com a data de hoje, e nada mais mudou (`git diff --stat` = 1 arquivo).
- [ ] **Cenário C — agente:** numa sessão de outro repositório, pedir "fecha sessão do noesis" e conferir que a skill usou `--exportar`/`--aplicar` e mostrou o buffer antes de aplicar.
- [ ] **Encerramento do plano:** confirmar que `DOMINIO.md`, `ARQUITETURA.md` e `SOLUCAO.md` contêm tudo o que este documento decidiu (tabela D1–D14) e apagar este arquivo num commit próprio.

---

## Fora deste plano

- **Detectar pendência apagada no check** (comparar com `HEAD` no pre-commit). É a proteção que pegaria o caso do `pdc-1` mesmo por edição direta. Fica fora porque introduz dependência de git no verificador; vale reavaliar depois de a triagem virar hábito.
- **Migração completa de AD-1** (tabela de frentes do `README.md` raiz e do `AGENTS.md`).
- **Escrita assistida de Decisão e Pessoa** (`desk add` continua só para pendência).
- **Reordenação dentro da seção pela triagem** (D8).







