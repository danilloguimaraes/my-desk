# Sessão 22/09/2026 — Dores: versão por ambiente, catálogo e implantação dirigida

**Canal:** sessão de trabalho individual
**Insumo:** estado do repo `dgolabs/terminus` em `main` e `develop`, workflows, runs do `deploy.yml`, tags dos produtos

## Dores declaradas

1. Saber qual versão de qual produto está rodando em determinado ambiente.
2. Conhecer o catálogo de versões de cada produto.
3. Implantar versões em ambientes específicos.

## O que foi verificado no repositório

### Dor 1 — versão rodando

| Fonte | O que diz | Limite |
|---|---|---|
| `apps/<p>/compose.homolog.yml` em `develop` | Versão **declarada** para Homologação | Declarado ≠ rodando já aconteceu: em 21/09 o deploy do trantor v0.7.0 terminou verde sem aplicar (bug de pathspec, corrigido no PR #29) |
| Mesmo arquivo em `main` | `main` reservada, sem Host | Está em v0.7.0 enquanto `develop` está em v0.9.0 |
| `docker ps` no Host | Versão efetivamente rodando | Exige SSH; não fica registrado |
| Runs do `deploy.yml` | Histórico de aplicações | Não confirma a tag que subiu |
| `docs/inventory.md` | Produtos e bloqueios | Não registra versão corrente |

Não há fonte de verdade para "o que está rodando"; só para "o que foi pedido".

### Dor 2 — catálogo

Tags em cada repo de produto (trantor: v0.3.0-mvp … v0.9.0; noesis: v0.4.0 … v0.8.1), imagens no GHCR. Nada consolidado. Já existem, sem serem usados como catálogo: PRs com label `release` merged no terminus (o que foi promovido) e `repos/<p>/tags` (o que foi publicado).

### Dor 3 — ambientes

Existe um ambiente: Homologação, no Home, refletindo `develop` (ADR-0008). Produção está reservada para `main` mas não tem Host, compose nem workflow. Nome do arquivo (`compose.homolog.yml`) e `deploy.yml` (gatilho em `develop`, path fixo) amarram tudo a esse único ambiente. "Ambiente" não é conceito no repo.

## Registro

As três dores foram para `PENDENCIAS.md` como demandas em aberto, sem solução escolhida.
