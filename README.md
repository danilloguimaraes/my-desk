# My Desk

Espaço pessoal de organização das minhas frentes de atuação. Cada frente tem uma pasta autocontida; este arquivo é o painel consolidado.

## Contexto Rápido

Se você chegou aqui para usar a documentação, siga esta ordem:

1. Leia [VISAO.md](VISAO.md) para entender o que o sistema deve contemplar e o que está fora de escopo.
2. Leia [REQUISITOS.md](REQUISITOS.md) para ver o que cada necessidade pede em termos verificáveis.
3. Leia [SOLUCAO.md](SOLUCAO.md) para usar os comandos e a gramática correta.
4. Use `desk check` sempre que alterar arquivos, antes de commitar.
5. Use o README de cada frente quando for trabalhar dentro de uma pasta específica.

## Frentes

| Projeto | Meu papel | Status | Próxima ação crítica |
|---|---|---|---|
| [SimCAQ](simcaq/) | Gestor e Tech Lead | Crítico | Definir as 2 bolsas mantidas — **24/09/2026** |
| [Denodare](denodare/) | Dev | Ativo — 4 work items; #126 F1 técnica encerrada, MR postergada até revisor definido | Alinhar com Afonso sobre revisor dos ADRs e validação das divergências 0005/0016/0018 |
| [PDC 1](pdc-1/) | Tech Lead e Pesquisador | Em conclusão | Deploy bloqueado por incompatibilidade do processador do servidor (ADK web ok, API falha) |
| [PDC 2](pdc-2/) | Tech Lead e Pesquisador | Onboarding | Ler os 2 artigos da Frente 2 e explorar repositórios quando liberados |
| [Mestrado](mestrado/) | Pesquisador | _a preencher_ | — |
| [Terminus](dgolabs/terminus/) | Operador e mantenedor (IaC dgolabs) | Ativo — repo endurecido (5 PRs mergeados 26/09): identidade `${meta.name}`, `make drift`, runbooks, Kafka autodescoberto; requisitos e readiness catalogados | Aplicar o ADR-0010 no Pool seguindo a ordem estrita do PR #39 (`pool.yml` antes do `job run`); depois fechar issue #1 |
| [Trantor](dgolabs/trantor/) | Criador e Operador (produto dgolabs) | Ativo — `develop` em v0.13.0; homologação em v0.11.0 (coxinha), v0.12.0 e v0.13.0 pendentes de deploy; E12–E18 mesclados, E19 parcial; 2 épicos abertos | Atualizar homologação para v0.13.0 no Terminus; depois disparar E20 (#159) |
| [Noesis](dgolabs/noesis/) | Criador e Operador (produto dgolabs) | Ativo — v0.8.1; MVP Guided concluído; sequência pós-MVP definida; repo com AGENTS.md/CONTRIBUTING (LLM Readiness 59→~73) | Reconciliar status de #44; publicar imagem GHCR (#87); abrir issues dos impasses achados na simulação de uso |
| [Principles](dgolabs/principles/) | Criador e Operador (produto dgolabs) | Ativo — Épico 0 concluído; Épico 1 (Debt) mergeado, Ledger pendente; self-contained v0 entregue (#23) | Implementar `GET /ledger` e homologar Épico 1 (tag `v1.0.0-epic-1`) |
| [Prisma](dgolabs/prisma/) | Criador e Operador (produto dgolabs) | Setup concluído — 7 épicos mapeados (#1–#7), 14 tasks `agent/ready` (#8–#21) | Disparar E1 (UX/UI) ∥ E2 (Backend) via agentes |
| [Preleção](dgolabs/prelecao/) | Criador e Operador (produto dgolabs) | Ativo — backend v0 entregue (fatia Fechar Chamada → Cobrança Avulsa); mensalidade, avaliação e escalação pendentes | Implementar Tesouraria de Mensalistas (Competência) |
| [my-skills](my-skills/) | Criador e mantenedor de skills pessoais | Ativo — skills novas em iteração | Testar `desk-sync` em projeto real e ajustar |

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

Convenções detalhadas em [AGENTS.md](AGENTS.md); o que o sistema deve contemplar (e o que não deve) está em [VISAO.md](VISAO.md); os requisitos derivados de cada necessidade estão em [REQUISITOS.md](REQUISITOS.md); o modelo de domínio está em [DOMINIO.md](DOMINIO.md); a arquitetura está em [ARQUITETURA.md](ARQUITETURA.md); a solução concreta (gramáticas e comandos) está em [SOLUCAO.md](SOLUCAO.md).
