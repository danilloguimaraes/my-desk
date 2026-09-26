# My Desk

Espaço pessoal de organização das minhas frentes de atuação. Cada frente tem uma pasta autocontida; este arquivo é o painel consolidado.

## Frentes

| Projeto | Meu papel | Status | Próxima ação crítica |
|---|---|---|---|
| [SimCAQ](simcaq/) | Gestor e Tech Lead | Crítico | Definir as 2 bolsas mantidas — **24/09/2026** |
| [Denodare](denodare/) | Dev | Ativo — 4 work items; #126 F0 encerrada, F1 em força-tarefa (plano em 6 blocos) | Escolher modo de execução e rodar Bloco A (tornar branch mergeável) até o checkpoint; confirmar bloqueantes restantes da #207 |
| [PDC 1](pdc-1/) | Tech Lead e Pesquisador | Em conclusão | Deploy bloqueado por incompatibilidade do processador do servidor (ADK web ok, API falha) |
| [PDC 2](pdc-2/) | Tech Lead e Pesquisador | Onboarding | Ler os 2 artigos da Frente 2 e explorar repositórios quando liberados |
| [Mestrado](mestrado/) | Pesquisador | _a preencher_ | — |
| [Terminus](dgolabs/terminus/) | Operador e mantenedor (IaC dgolabs) | Ativo — v0.2, homologação rodando | Migrar compose do trantor para api + worker (issue #1); destravar publish do noesis |
| [Trantor](dgolabs/trantor/) | Criador e Operador (produto dgolabs) | Ativo — v0.9.0; E12/E13 mesclados; 5 épicos abertos | Refazer #84 (UX pós-publicação); fechar issues de E12/E13; disparar E19 |
| [Noesis](dgolabs/noesis/) | Criador e Operador (produto dgolabs) | Ativo — v0.8.1; MVP Guided concluído; aguardando gate E10.2 | Resolver bugs críticos #79/#82/#84; publicar imagem GHCR (#87) |
| [my-skills](my-skills/) | Criador e mantenedor de skills pessoais | Ativo — skills novas em iteração | Testar `desk-sync` em projeto real e ajustar |

## Pendências urgentes (todas as frentes)

- [ ] **SimCAQ** — Definir quem fica com as 2 bolsas — 24/09/2026
- [ ] **SimCAQ** — Restabelecer contato com Leonardo — imediato
- [ ] **Denodare** — #126: F1 Bloco A — tornar `poc/126-multitenant` mergeável e parar no checkpoint — próximo passo
- [ ] **Denodare** — #126: escolher modo de execução da força-tarefa (subagent-driven ou inline) — antes do Bloco A
- [ ] **Denodare** — #207: confirmar com Afonso quais dos 3 bloqueantes seguem abertos após !401 — esta semana
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
