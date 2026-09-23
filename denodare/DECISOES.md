# Decisões — Denodare

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

---

## 22/09/2026 — Ordem de ataque dos 4 work items

**Contexto:** Quatro work items atribuídos em paralelo (#126, #207, #217, #154), chegando de forma difusa (comunicação, continuação de branch, débito técnico). Necessidade de priorizar sem deixar os demais parados.

**Decisão:** #126 (multi-tenant) é o foco. Os outros três avançam por passos curtos e desbloqueadores, não por entrega completa:

1. #207 — uma pergunta a Afonso para fechar o que restou dos 3 bloqueantes; depois um MR único.
2. #217 — uma sub-issue por MR (#226–#230), na ordem em que estão listadas.
3. #154 — começar por 12.2 (só código); pedir acesso ao Grafana desde já para destravar 12.1.

**Consequências:** Cada work item tem um "próximo passo" explícito no [README](README.md) e em [PENDENCIAS.md](PENDENCIAS.md); revisar a ordem quando #126 tiver parecer entregue.
