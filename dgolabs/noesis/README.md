# Noesis (dgolabs)

**Meu papel:** Criador e Operador — defino o backlog (épicos), homologo a hipótese de rigor e uso o produto na pesquisa
**Status:** Ativo — MVP Guided concluído (E1–E10 fechados); v0.8.1 declarado em `develop`; aguardando gate de rigor (E10.2/#44) para iniciar pós-MVP

## Contexto

[`dgolabs/noesis`](https://github.com/dgolabs/noesis) é o pipeline de **leitura científica → Zettelkasten**. Ele ingere papers (PDF), processa através de estágios cognitivos (S1–S4) e gera notas atômicas no vault Obsidian. O produto é o consumidor natural do skill `pat-pesquisa` (leitura acadêmica em 5 fases).

Criei o projeto porque **a leitura profunda de papers é trabalho de alto valor cognitivo, mas mecânica repetitiva**. O Noesis existe para absorver a triagem, extração de evidência e formatação, me devolvendo a análise crítica. É também o segundo produto dgolabs consumido pelo Trantor (depois do próprio Trantor).

**Os épicos são a fonte primária do backlog.** Cada épico (`level/epic`) registra problema, proposta e sub-issues (`level/task`). O Trantor executa as folhas; esta bandeja acompanha os épicos como unidades de trabalho.

### Arquitetura em uma linha

Event-sourced (Kafka fonte de verdade, SQLite projeção), Python, pipeline S1–S4 (Triagem → Evidência → Dialética → Curadoria) com gates humanos. LLM Gateway com consentimento granular por estágio. Vault adapter para Obsidian.

### Épicos em aberto (25/09/2026)

| Épico | Tema | Sub-issues | Situação |
|---|---|---|---|
| [E11 #47](https://github.com/dgolabs/noesis/issues/47) | Backlog Pós-MVP: Delegated/Deep, tipologias especiais, Ollama, integrações e foco humano | #48–#54 | **Bloqueado** aguardando aprovação de E10.2 (#44); 7 sub-issues mapeadas |

### Issues críticas fora de épico (25/09/2026)

| Issue | Assunto | Impacto |
|---|---|---|
| [#87](https://github.com/dgolabs/noesis/issues/87) | Publicar imagem multi-arch no GHCR | **Bloqueio do Terminus** — sem imagem, homologação não roda |
| [#79](https://github.com/dgolabs/noesis/issues/79) | `remote_processing_consented` nunca propagado por S1/S2/S3 | Modo Delegated remoto sempre rejeitado |
| [#82](https://github.com/dgolabs/noesis/issues/82) | EventStore.load trava com LSO presa por transação órfã | Leituras travam silenciosamente |
| [#83](https://github.com/dgolabs/noesis/issues/83) | SDK: modo "plain" para consumidores de fan-out somente-leitura | Edge em homologação precisa de grupo efêmero |
| [#85](https://github.com/dgolabs/noesis/issues/85) | WriteConflict inalcançável no fluxo do vault | Falta "Regravar no cofre" explícito |
| [#86](https://github.com/dgolabs/noesis/issues/86) | Prompts nunca exercitados fora do mock | Homologação com LLM real pendente |

### Referências no repositório

- `docs/adr/0006-stack-corte-mvp-privacidade-homologacao.md` — corte do MVP e hipótese de rigor
- `docs/business/value-byproducts.md` — subprodutos de valor do pipeline
- `CONTEXT.md` — vocabulário (Reading, Gate, S1–S4, Vault, Delegated/Deep)

Operação em homologação (compose, release, deploy) fica na bandeja [dgolabs/terminus/](../terminus/).

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Atores e repositórios consumidores |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto, por tema |
| [DECISOES.md](DECISOES.md) | Decisões de produto/priorização (as arquiteturais ficam nos ADRs) |
| [reunioes/](reunioes/) | Notas de sessões de trabalho e homologação |
| [rascunhos/](rascunhos/) | Épicos, issues e ADRs em preparação |
| [leituras/](leituras/) | Notas de papers processados (saída do produto) |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 26/09/2026 | #84 fechada (TriageFailed como Fato); sequência de execução definida: #87 → #79 → #83 → #82 → #85 → #86 → E10.2 → E11 |
| 25/09/2026 | Bandeja criada a partir da análise das issues abertas (17 issues: 1 épico E11, 6 bugs críticos, 7 sub-issues E11, 3 operacionais) |
| 19/09/2026 | Release noesis 0.8.0 → 0.8.1 (PR #14/#15) — [terminus](../terminus/README.md) |
| 16/09/2026 | E10 Integração ponta a ponta fechado; MVP Guided concluído |
| 14/09/2026 | E1–E9 fechados: fundação, contratos, SDK, gatekeeper, document worker, LLM gateway, domain workers, vault, edge |
