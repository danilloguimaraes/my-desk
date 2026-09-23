# My Desk

Espaço pessoal de organização das minhas frentes de atuação. Cada frente tem uma pasta autocontida; este arquivo é o painel consolidado.

## Frentes

| Projeto | Meu papel | Status | Próxima ação crítica |
|---|---|---|---|
| [SimCAQ](simcaq/) | Gestor e Tech Lead | Crítico | Definir as 2 bolsas mantidas — **24/09/2026** |
| [Denodare](denodare/) | Dev | Ativo — 4 work items em paralelo | Parecer sobre o plano multi-tenant (#126); confirmar bloqueantes restantes da #207 com Afonso |
| [PDC 1](pdc-1/) | Tech Lead e Pesquisador | Em conclusão | Publicar versão atual em servidor (com Danilo Ramos) |
| [PDC 2](pdc-2/) | Tech Lead e Pesquisador | Onboarding | Ler os 2 artigos da Frente 2 e explorar repositórios quando liberados |
| [Mestrado](mestrado/) | Pesquisador | _a preencher_ | — |

## Pendências urgentes (todas as frentes)

- [ ] **SimCAQ** — Definir quem fica com as 2 bolsas — 24/09/2026
- [ ] **SimCAQ** — Restabelecer contato com Leonardo — imediato
- [ ] **Denodare** — #126: ler `plano-multitenant-daurora.md` e registrar parecer na issue — esta semana
- [ ] **Denodare** — #207: confirmar com Afonso quais dos 3 bloqueantes seguem abertos após !401 — esta semana

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
