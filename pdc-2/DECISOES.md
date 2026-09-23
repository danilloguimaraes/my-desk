# Decisões — PDC 2

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

---

## 2026-09-11 — Primeiro ciclo dedicado a onboarding, sem divisão em subfrentes

**Contexto:** grupo recém-formado, ferramenta já parcialmente implementada, arquitetura complexa (Orchestrator + Context Platform). Fonte: [onboarding 11/09](reunioes/2026-09-11-onboarding-frente-2.md).
**Decisão:** o primeiro ciclo é de leitura, estudo e exploração dos repositórios; o backlog detalhado de P&D vem depois que o grupo tiver visão comum. Meta da primeira macroentrega: uma contribuição pequena revisada por participante.
**Consequências:** não tentar alterar a implementação antes de entender a arquitetura; produzir fichamentos e registrar dúvidas.

## 2026-09-11 — Princípio norteador: contexto certo, não máximo

**Contexto:** barreira de contexto em sistemas legados distribuídos; contexto excessivo gera ruído e custo.
**Decisão:** a frente busca fornecer "o contexto certo, para a tarefa certa, no momento certo", via Knowledge Graph, busca semântica, padrões governados e MCP.
**Consequências:** orienta escolhas de design do grafo (seleção de região relevante, hubs, comunidades) e métricas (redução de tokens, aderência).

## 2026-09-11 — Extração determinística antes de LLM

**Contexto:** extração de padrões de software (arquitetura, nomenclaturas, convenções).
**Decisão:** sempre que uma regra puder ser obtida por análise estática/parsing, usar abordagem determinística; LLM apenas para padrões que exigem interpretação semântica. Candidatos passam por governança (identificado / aprovado / rejeitado / obrigatório).
**Consequências:** custo menor e reprodutibilidade; a camada LLM do grafo é enriquecimento, não base.

## 2026-09-11 — Canais e cadência

**Contexto:** necessidade de acompanhar dúvidas e lacunas de conhecimento do grupo.
**Decisão:** dúvidas e relatórios de estudo no Discord; tarefas com responsável e prazo em GitHub Projects/Kanban; reuniões semanais, possivelmente mais frequentes no primeiro mês.
**Consequências:** manter registros de estudo no Discord além dos fichamentos locais.

## 2026-09-11 — Confidencialidade do segundo artigo

**Contexto:** artigo comparativo do framework ainda em avaliação.
**Decisão:** não divulgar externamente.
**Consequências:** fichamento em `leituras/` pode existir, mas sem compartilhar o PDF ou conteúdo fora do grupo.
