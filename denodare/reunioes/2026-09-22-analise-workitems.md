# Análise dos 4 work items atribuídos — 22/09/2026

**Tipo:** nota de trabalho (não é ata de reunião). Levantamento feito a partir do GitLab (`fakenews-bff`): descrição das issues, comentários, MRs, branches e sub-issues.
**Motivação:** as demandas do Denodare chegam de forma confusa nos work items (mistura de comunicação, débito técnico e continuação de branch). Este levantamento reconstrói a situação real de cada um para orientar a ordem de ataque.

## Situação encontrada

| # | Work item | O que a issue diz | O que o repositório mostra |
|---|---|---|---|
| [#126](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/126) | Arquitetura multi-tenant | Descrição ampla (isolamento, gestão de tenants, JWT, customização, observabilidade); um único critério: "avaliar a proposta de plano" (anexo `plano-multitenant-daurora.md`) | Nenhum MR, nenhuma branch, nenhuma sub-issue. Rótulos em 3 repositórios (bff, bChain, front), um só assignee |
| [#207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207) | Recebimento de solicitações de análise do Guaia (M2M) | Fluxo de solicitação → aceite/contraproposta → despacho | Fundação merged em 01/09 (!383, !385–!388), endpoints em 08/09 (!399), materialização fiel em 11/09 (!401). Comentário de Afonso em 08/09: MR aprovado, mas develop ainda deve à "V2" 3 bloqueantes (map `publication`→news, `ValidateIf`, race de idempotência) e vários gaps (timeline, dossiê, org/tenant de domínio, pricing, outbox). Hotfix de migrações que derrubaram develop |
| [#217](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/217) | Refatoração de duplicações e código morto | 518 clones, ~4,9% de duplicação; regra bloqueante `analise-obrigatoria-bff.mdc` | Já fatiada: #221–#225 concluídas em 26/08 (!377–!381); #226–#230 abertas e atribuídas a mim. Branches `feat-217-refatoracao` e `feature-217-refatoracao` paradas desde 21/08 |
| [#154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154) | Débito residual do épico #138 | 5 itens (12.1 Grafana, 12.2 `syncRewards`, 12.3 claim no sync de mídia, 12.4 ADR, 12.5 outbox) | Nenhum MR. Milestone 1.7.0, a mais antiga em aberto |

## Leitura

- A lista informada tinha 4 work items; o GitLab mostra 8 issues abertas comigo porque #226–#230 são sub-issues da #217. Não são demanda nova.
- #207 e #217 já andaram e têm próximo passo claro. #154 e #126 estão paradas.
- #126 é a única em que o critério de aceite está fora da issue (anexo) e sem decomposição. É o ponto de enriquecimento: mover o plano para `docs/` versionado, explicitar as decisões em aberto no corpo da issue e abrir sub-issues por camada, como já foi feito com #207 e #217.
- Há risco de dois modelos de tenant: o fluxo M2M da #207 já introduziu org/tenant em `oauth_clients` (e `m2m_organization`/`m2m_tenant` na V2). O plano da #126 precisa decidir se é a mesma coisa.
- O ambiente de desenvolvimento (blockchain que ninguém roda local; VPN + infra completa para executar qualquer coisa; exploratórios inviáveis) encarece toda validação manual. Refatorações (#217) e mudanças em crons/eventos (#154) dependem de cobertura unitária forte. Detalhe no [README](../README.md#ambiente-de-desenvolvimento).

## Bloqueio registrado

O anexo `plano-multitenant-daurora.md` não pôde ser baixado por API (uploads exigem Maintainer; a URL direta cai no desafio do Cloudflare). Download só pelo navegador.

## Propagação

- Ordem de ataque → [DECISOES.md](../DECISOES.md)
- Ações por work item → [PENDENCIAS.md](../PENDENCIAS.md)
- Pessoas identificadas (Afonso Ueslei, Matheus Lázaro, Brito) → [PESSOAS.md](../PESSOAS.md)
