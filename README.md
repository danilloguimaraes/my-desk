# My Desk

Espaço pessoal de organização das minhas frentes de atuação. Cada frente tem uma pasta autocontida; este arquivo é o painel consolidado.

## Frentes

| Projeto | Meu papel | Status | Próxima ação crítica |
|---|---|---|---|
| [SimCAQ](simcaq/) | Gestor e Tech Lead | Crítico | Definir as 2 bolsas mantidas — **24/09/2026** |
| [Denodare](denodare/) | Dev | Ativo — 4 work items; #126 F1 técnica encerrada, MR postergada até revisor definido | Alinhar com Afonso sobre revisor dos ADRs e validação das divergências 0005/0016/0018 |
| [PDC 1](pdc-1/) | Tech Lead e Pesquisador | Em conclusão | Deploy bloqueado por incompatibilidade do processador do servidor (ADK web ok, API falha) |
| [PDC 2](pdc-2/) | Tech Lead e Pesquisador | Onboarding | Ler os 2 artigos da Frente 2 e explorar repositórios quando liberados |
| [Mestrado](mestrado/) | Pesquisador | _a preencher_ | — |
| [Terminus](dgolabs/terminus/) | Operador e mantenedor (IaC dgolabs) | Ativo — repo endurecido (5 PRs mergeados 26/09): identidade `${meta.name}`, `make drift`, runbooks, Kafka autodescoberto; requisitos e readiness catalogados | Aplicar o ADR-0010 no Pool seguindo a ordem estrita do PR #39 (`pool.yml` antes do `job run`); depois fechar issue #1 |
| [Trantor](dgolabs/trantor/) | Criador e Operador (produto dgolabs) | Ativo — v0.11.0 em homologação (coxinha); E12–E18 mesclados, E19 parcial; 2 épicos abertos (E19 parcial, E20) | Reabrir solicitação de #130 (duas execuções coexistiram em 26/09); depois disparar E20 (#159) |
| [Noesis](dgolabs/noesis/) | Criador e Operador (produto dgolabs) | Ativo — v0.8.1; MVP Guided concluído; sequência pós-MVP definida; repo com AGENTS.md/CONTRIBUTING (LLM Readiness 59→~73) | Reconciliar status de #44; publicar imagem GHCR (#87); abrir issues dos impasses achados na simulação de uso |
| [Principles](dgolabs/principles/) | Criador e Operador (produto dgolabs) | Ativo — Épico 0 concluído; Épico 1 (Debt) mergeado, Ledger pendente; self-contained v0 entregue (#23) | Implementar `GET /ledger` e homologar Épico 1 (tag `v1.0.0-epic-1`) |
| [Prisma](dgolabs/prisma/) | Criador e Operador (produto dgolabs) | Setup concluído — 7 épicos mapeados (#1–#7), 14 tasks `agent/ready` (#8–#21) | Disparar E1 (UX/UI) ∥ E2 (Backend) via agentes |
| [Preleção](dgolabs/prelecao/) | Criador e Operador (produto dgolabs) | Ativo — backend v0 entregue (fatia Fechar Chamada → Cobrança Avulsa); mensalidade, avaliação e escalação pendentes | Implementar Tesouraria de Mensalistas (Competência) |
| [my-skills](my-skills/) | Criador e mantenedor de skills pessoais | Ativo — skills novas em iteração | Testar `desk-sync` em projeto real e ajustar |

## Pendências urgentes (todas as frentes)

- [ ] **SimCAQ** — Definir quem fica com as 2 bolsas — 24/09/2026
- [ ] **SimCAQ** — Restabelecer contato com Leonardo — imediato
- [ ] **Denodare** — #126: alinhar com Afonso revisor dos ADRs `Accepted` e validação das divergências 0005/0016/0018 antes de abrir MR — próximo passo
- [ ] **Denodare** — #207: confirmar com Afonso quais dos 3 bloqueantes seguem abertos após !401 — esta semana
- [ ] **Noesis** — Reconciliar E10.2 #44: CLOSED no GitHub, desk o trata como gate de E11 — próxima sessão
- [ ] **PDC 1** — Deploy bloqueado: ADK web ok, mas execução via API falha por incompatibilidade do processador do servidor — imediato
- [ ] **PDC 1** — Confirmar arquitetura do servidor com Danilo Ramos e viabilizar alternativa compatível — imediato
- [ ] **PDC 1** — Executar HumanEval com as LLMs definidas e gerar relatórios — após o deploy
- [ ] **Trantor** — Fechar/atualizar issues de E12 e E13 após merges de PR #134 e #142 — esta semana
- [ ] **Trantor** — Refazer #84 (E12 · Interface & E2E) que falhou por `model_overloaded` — esta semana
- [ ] **my-skills** — Testar `desk-sync` em projeto real (denodare, trantor ou noesis) e ajustar SKILL.md — próxima sessão

_Manter esta lista como espelho das seções "Urgente" de cada `PENDENCIAS.md`._

## Estrutura de cada projeto

```
<projeto>/
├── README.md        # papel, contexto, navegação, linha do tempo
├── PESSOAS.md       # stakeholders e papéis
├── PENDENCIAS.md    # lista viva de ações
├── DECISOES.md      # registro de decisões (contexto → decisão → consequências)
├── reunioes/        # YYYY-MM-DD-assunto.md
├── rascunhos/       # YYYY-MM-DD-assunto.md
└── leituras/        # notas de papers (apenas frentes de pesquisa)
```

Convenções detalhadas em [AGENTS.md](AGENTS.md).
