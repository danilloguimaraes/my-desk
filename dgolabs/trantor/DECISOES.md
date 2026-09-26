# Decisões — Trantor

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

As decisões **arquiteturais** vivem nos ADRs do repositório ([`docs/adr/`](https://github.com/dgolabs/trantor/tree/develop/docs/adr), 0001–0023) e não são duplicadas aqui. Este arquivo registra decisões de **produto, priorização e operação** minhas como criador e operador.

ADRs de referência rápida:

| ADR | Assunto |
|---|---|
| 0001 | Local-Only Autonomy — nada chega ao remoto sem veredito |
| 0003 | Review Context Isolation — revisor selado |
| 0005 / 0007 | Epic Delivery: branch integrador; entrega parcial permitida |
| 0006 | Refuse Broken Baseline |
| 0012 | Kafka event sourcing atrás do port `bus` |
| 0017 | Forge Least Privilege |
| 0020 | Bounded Self-Repair limitado por progresso |
| 0021 | Stepwise Implementation — um passo por chamada ao motor |
| 0022 | Pós-publicação e resposta a revisão (E12) |
| 0023 | Autonomia graduada pós-publicação (E13) |

---

## 26/09/2026 — Gate local do repositório é obrigatório, ferramenta ausente falha (ADR-0027)

**Contexto:** Avaliação de prontidão do repositório para agentes (skill `repo-llm-readiness`) apontou taxa de CI verde recente em 67%. Investigação das falhas mostrou padrão consistente: toda vez que um PR ficou vermelho no primeiro push, a causa era detectável localmente (erro de compilação, `errcheck`, testes de sincronia de docs), mas `make lint` pulava em silêncio quando `golangci-lint` não estava instalado, e `make ci` passava verde em máquinas sem o binário. Agentes concluíam "tudo passou" e o remoto virava o primeiro leitor real do próprio código.

**Decisão:** Formalizar como ADR-0027 o princípio de que o gate local (`make ci`) é idêntico ao remoto. Cada dependência do gate (`golangci-lint`, Node 20, `node_modules`, compilador C para `-race`) é obrigatória; ausência falha alto com remédio, nunca vira `skip` silencioso. Ferramentas verdadeiramente opcionais (Kafka `e2e`, Docker `test-docker`) permanecem opt-in via alvos separados de `ci`. Toda futura dependência de gate segue o mesmo padrão desde o primeiro commit.

**Consequências:** `make lint` falha com instrução de instalação (`make lint-install`); `deploy/bootstrap-ubuntu.sh` instala o linter; `.nvmrc` e `engines` fixam Node 20; AGENTS.md explica a regra e pede rodar `make ci` inteiro antes de push. ADR-0027 fica ancorado ao eixo Evidência (o determinismo da ADR-0002 exige paridade real, não aparente). Corolário em aberto: `-race` sem `CC` ainda é warning no Makefile; virar falha assim que houver caminho sem travar sandboxes do `.opencode`.

## 26/09/2026 — Simulação de uso por LLM descartada como fonte de acionáveis

**Contexto:** Rodada de simulação de uso pelo método Elicitron (12 personas geradas em série, cada uma vivendo Ação/Observação/Desafio sobre 10 funcionalidades, entrevistadas com a experiência em contexto). Produziu 41 necessidades com rastreabilidade e três achados de espinha dorsal (onboarding, dossiê adaptável, F4 Accountability Profile sobrecarregado).

**Decisão:** Descartar todos os acionáveis derivados da simulação. Manter o material bruto em `/tmp/opencode/trantor-simulation/` apenas como registro de hipóteses de setembro/26.

**Consequências:** Nenhum item entra em backlog do Trantor a partir desta rodada. A crítica de fundo — validação com pessoas simuladas é extensão de alucinação, não observação — vale para futuras aplicações do método neste projeto. Se voltar ao tema, será via conversa com usuário real, não outra rodada de simulação.

## 22/09/2026 — Ordem dos épicos: E19 antes de E18, E14, E16, E17

**Contexto:** Cinco épicos em aberto sem ordem declarada. A execução de E12 perdeu a sub-issue #84 (e ~3 h de trabalho encadeado) por um `model_overloaded` pontual; qualquer épico seguinte corre o mesmo risco.

**Decisão:** Executar E19 (resiliência do motor e retomada de sub-issue) primeiro. Em seguida E18 (SPA), depois E14 (observabilidade). E16 e E17 ficam sem prazo: E16 depende de ADR sobre executor; E17 precisa renumerar seu ADR.

**Consequências:** #84 é refeita de forma isolada antes de tudo, para não deixar E12 sem UX. Bug #118 e plano #112 são absorvidos por E19 e fechados como tal.

## 22/09/2026 — Trantor vira frente própria no my-desk

**Contexto:** Desenvolvimento de features e revisão de entregas são as minhas maiores dragas de energia e atenção. O Trantor foi criado para absorver esse trabalho. Operação do produto em homologação já era acompanhada em `terminus/`, mas o backlog de produto (épicos, bugs, decisões humanas pendentes) não tinha lugar.

**Decisão:** Criar a bandeja `trantor/`. A unidade de acompanhamento é o **épico**: as issues `level/epic` do repositório são a fonte primária do backlog e concentram problema, proposta e sub-issues. Sub-issues só entram em `PENDENCIAS.md` quando exigem intervenção minha.

**Consequências:** Terminus segue responsável por release/deploy da imagem; esta bandeja cuida do que entra em cada release. Épicos novos nascem em `rascunhos/` e viram issue no repo.
