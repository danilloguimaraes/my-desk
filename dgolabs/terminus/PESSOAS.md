# Pessoas — Terminus

Projeto de uma pessoa. A tabela registra atores (no vocabulário do `CONTEXT.md`) e os produtos atendidos, para saber quem depende de quem.

## Atores

| Nome | Papel | Observações |
|---|---|---|
| Danillo | Operador — único humano da rede; decide, aprova PRs e executa `apply` no Host | GitHub: org `dgolabs` |
| Agente (LLM) | Mantém o repositório: edita, valida, abre PR. Nunca executa no Host | Regras em `AGENTS.md` do repo (ADR-0005) |
| Runner (`karol1`) | Daemon systemd no Home que executa os workflows do Terminus | Distinto de Worker; ADR-0009 |

## Produtos atendidos

| Produto | Repositório | Dependência do Terminus |
|---|---|---|
| trantor | `dgolabs/trantor` | Imagem publicada em GHCR; Terminus fixa a tag |
| noesis | `dgolabs/noesis` | Aguarda workflow de publish (issue #87) — acompanhado em [noesis/](../noesis/) |
| prelecao | `dgolabs/prelecao` | Aguarda CI |
| principles | `dgolabs/principles` | Aguarda CI (api + web) |
| aurora | `dgolabs/aurora` | CI só builda |
