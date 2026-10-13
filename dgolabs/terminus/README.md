# Terminus (dgolabs)

| campo | valor |
|---|---|
| situacao | ativa |
| papel | Operador e mantenedor do repositório |
| estado | Ativo — refundado (PR #36, ADR-0010): Pool Nomad com Plataforma, Produção e Ambientes Efêmeros; trantor v0.11.0 e noesis 0.8.1 em `jobs/prod/` |

**Meu papel:** Operador (único humano do Pool dgolabs) e mantenedor do repositório
**Status:** Ativo — refundado (PR #36, ADR-0010): Pool Nomad com Plataforma, Produção e Ambientes Efêmeros; trantor v0.11.0 e noesis 0.8.1 em `jobs/prod/`

## Contexto

[`dgolabs/terminus`](https://github.com/dgolabs/terminus) é a infraestrutura como código da rede dgolabs: um Pool de cinco máquinas na Tailnet (`coxinha`/`karol1` — mesma máquina —, `feijoada`, `tapioca`, `garapa`, `guarana`), cinco produtos, um operador. Criei o repositório porque implantações e acompanhamento de versões vinham sendo feitos à mão, sem registro nem repetibilidade. O repo é a "Enciclopédia": permite recriar o Pool do zero e trocar a versão de um produto por PR.

Modelo de trabalho: **Agente edita e abre PR; Operador aplica.** Nada no Pool muda sozinho — todo `nomad job run`, `tofu apply` ou `ansible-playbook` é humano.

### Camadas

| Camada | Ferramenta | Dir | Estado |
|---|---|---|---|
| Provisão | OpenTofu | `provision/` | vazio (workers de burst são futuro) |
| Configuração | Ansible | `configure/` | roles base, tailscale, docker, platform, app, runner |
| Plataforma | Nomad Jobs | `jobs/platform/` | kafka, kafka-topics, postgres, caddy (fixados em `coxinha`) |
| Produção | Nomad Jobs | `jobs/prod/` | trantor, noesis (tag via variável, nunca `latest`) |
| Ambientes Efêmeros | Nomad Jobs | `jobs/ephemeral/` | vazio; depende de CI de branch nos Produtos |
| Segredos | sops+age (at-rest), Nomad Variables (runtime) | `secrets/` | em claro só no Host ou na minha máquina |

### Pool Nomad (ADR-0010, proposto)

- 3 Servers para quorum (`coxinha`, `feijoada`, `tapioca`), todos também Clients; `garapa` e `guarana` são Clients apenas.
- Roteamento: Caddy job com Consul template; `*.dgolabs.com.br` → IP Tailnet do `coxinha`.
- Kafka com dois listeners: `PLAINTEXT://kafka:9092` (rede docker do `coxinha`) e `EXTERNAL://100.93.169.123:9094` (Tailnet).
- ADRs 0001–0009 viraram legado em `docs/adr/legacy/`.

### Produtos e situação de release (26/09/2026)

| Produto | Domínio | Maturidade | Imagem publicada | Situação no Pool |
|---|---|---|---|---|
| trantor | Orquestração de agentes (Issues → PRs) | MVP | `ghcr.io/dgolabs/trantor` + `trantor-worker` | Em `jobs/prod/trantor.nomad`, tag v0.11.0; fixado em `coxinha` (~8 GB de estado local + binário opencode do host) |
| noesis | Leitura científica → Zettelkasten | MVP | `ghcr.io/dgolabs/noesis` | Em `jobs/prod/noesis.nomad`, tag 0.8.1; produto usado para validar a distribuição no Pool |
| prelecao | Gestão de pelada | Protótipo v0 | não | Fora do Pool — sem CI no repo do produto |
| principles | Finanças pessoais | Protótipo v0 | não | Fora do Pool — sem CI (2 imagens: api, web) |
| aurora | Briefing diário em áudio | Pré-MVP | não | Fora do Pool — CI só builda; TTS/Telegram/scheduler são stubs |

### Fluxo de release (pós-refundação)

- Branch `release/<produto>-<tag>` troca o `default` da variável `tag` em `jobs/prod/<produto>.nomad.hcl`; PR para `develop`.
- Merge não dispara deploy automático: o Operador aplica com `nomad job run` quando decidir.
- Imagem deve ser multi-arch (`linux/arm64` + `linux/amd64`), tag de release publicada no GHCR — nunca `latest`.

### Restrições operacionais

- Bind só na Tailnet; nada em `0.0.0.0`. Segredos só em sops+age ou Nomad Variables.
- Quorum de 3 Servers: se duas de `coxinha`/`feijoada`/`tapioca` caírem, o Pool para de agendar (Jobs continuam rodando).
- Enquanto a Plataforma estiver fixada em `coxinha` por `constraint`, essa máquina continua ponto único de falha.
- Zero build no Pool; builds de Produto só em CI externo. Tópicos Kafka prefixados `<produto>.*`; um database por Produto por ambiente.

### Referências no repositório

- `CONTEXT.md` — vocabulário (Operador, Agente, Pool, Máquina, Job, Produto, Ambiente Efêmero)
- `AGENTS.md` — regras, permissões e validação para agentes
- `docs/adr/` — ADR-0010 (Pool Nomad); 0001–0009 em `docs/adr/legacy/`
- `legacy/` — artefatos do modelo anterior (compose, `apps/`, ADRs antigos)

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Quem é quem (aqui, atores e produtos) |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto |
| [DECISOES.md](DECISOES.md) | Decisões locais desta bandeja (as arquiteturais ficam nos ADRs do repo) |
| [reunioes/](reunioes/) | Notas de sessões de trabalho/operação |
| [rascunhos/](rascunhos/) | Issues, PRs e textos em preparação |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 26/09/2026 | Briefing + sync do desk: bandeja reescrita para refletir a refundação Nomad; issue #1 continua aberta no GitHub e vira pendência de fechamento |
| 24/09/2026 | Refundação: Pool Nomad para Plataforma, Produção e Ambientes Efêmeros (PR #36, ADR-0010; ADRs 0001–0009 legados); release trantor v0.10.0 → v0.11.0 (PR #37); fix syncthing restaurando o cofre do noesis após a distribuição |
| 23/09/2026 | Release trantor v0.9.0 → v0.10.0 (PR #35) |
| 22/09/2026 | Registradas as três dores de operação (versão rodando, catálogo, ambientes) como demandas em aberto ([nota](reunioes/2026-09-22-dores-versoes-ambientes.md), [pendências](PENDENCIAS.md)) |
| 22/09/2026 | Bandeja montada a partir do estado do repositório (README, CONTEXT, inventário, ADRs, issue #1, histórico de releases) |
| 22/09/2026 | Release trantor v0.8.0 → v0.9.0 (PR #34) |
| 21/09/2026 | Releases trantor v0.7.0 → v0.7.1 → v0.8.0 (PRs #31, #32); fixes no `deploy.yml`: pathspec `apps/` e falha quando vazio (#29), build do worker antes do deploy (#33) |
| 21/09/2026 | Deploy do trantor v0.7.0 (PR #28) terminou verde sem aplicar — origem do fix #29 |
| 21/09/2026 | Promoção `develop → main`: workflows passam a rodar no runner self-hosted `karol1` (ADR-0008/0009, PR #30) |
| 19/09/2026 | Release noesis 0.8.0 → 0.8.1 (PR #14/#15) |
| 18/09/2026 | Release trantor v0.5.1 → v0.6.0 (PR #11/#12); script `deploy_homolog.sh` para implantação direta |
| 16/09/2026 | Issue #1 aberta: migrar `apps/trantor/compose.homolog.yml` para o Trantor Go (api + worker) — **resolvida pela refundação (#36), falta fechar** |
