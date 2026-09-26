# Decisões — Noesis

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

As decisões **arquiteturais** vivem nos ADRs do repositório ([`docs/adr/`](https://github.com/dgolabs/noesis/tree/develop/docs/adr)) e não são duplicadas aqui. Este arquivo registra decisões de **produto, priorização e operação** minhas como criador e operador.

---

## 26/09/2026 — Sequência de execução pós-MVP

**Contexto:** Com #84 fechada, restavam 5 bugs críticos, 1 bloqueio de infraestrutura (#87) e 1 gate de qualidade (E10.2/#44) antes do backlog pós-MVP (E11). A ordem de ataque não era óbvia: alguns itens bloqueiam outros, alguns são independentes, e a POC do karol2 vinha consumindo ciclos sem relação direta com o backlog.

**Decisão:** Fixar a sequência: **#87 → #79 → #83 → #82 → #85 → #86 → E10.2 → E11**. #87 primeiro porque é bloqueio do Terminus e pré-condição para homologação remota. #79 antes de #86 porque sem propagação de consentimento o LLM real não roda. #83 antes de #82 porque afeta o Edge em homologação. E11 só após E10.2 passar.

**Consequências:** A bandeja passa a refletir ordem, não apenas lista. O Trantor executa na sequência fixada; desvios exigem revisão desta decisão.

---

## 25/09/2026 — Noesis vira frente própria no my-desk

**Contexto:** O Noesis era mencionado apenas como produto atendido pelo Terminus e consumido pelo Trantor, mas não tinha bandeja própria. A análise das 17 issues abertas revelou um épico E11 estruturado (7 sub-issues), 6 bugs críticos no núcleo e um gate de qualidade (E10.2/#44) bloqueando o pós-MVP. A complexidade do produto justifica acompanhamento dedicado.

**Decisão:** Criar a bandeja `dgolabs/noesis/`. A unidade de acompanhamento é o **épico** (`level/epic`), alinhado com a convenção do Trantor. As sub-issues de E11 são listadas em `PENDENCIAS.md` porque exigem orquestração pós-gate.

**Consequências:** Terminus segue responsável por release/deploy da imagem; Trantor executa as folhas; esta bandeja cuida do backlog de produto, priorização e registro de decisões humanas. O gate E10.2 (#44) é registrado como pendência explícita — sem ele, E11 não inicia.
