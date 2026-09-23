# CodeJudgeBench: Benchmarking LLM-as-a-Judge for Coding Tasks

**Autores:** Jiang, H.; Chen, Y.; Cao, Y.; Lee, H.; Tan, R. T.
**Ano:** 2025
**Fonte:** https://arxiv.org/abs/2507.10535
**Status:** A ler
**Relação com o projeto:** recomendado a Gabriel para a proposta de benchmark **CodeJudgeBench (split CodeRepair)** (agente-alvo: `reviewer` (LLM-as-judge)) — ver [nota de propostas](../reunioes/2026-09-22-benchmarks-propostas.md). Atividade secundária; não bloqueia a conclusão.

## Do que trata

Avalia LLMs como juízes de código em geração, reparo e teste unitário (comparações pareadas). Split CodeRepair é o relevante para o `reviewer`.

## Notas de leitura

_a preencher_

## O que quero entender

- Como o benchmark define sucesso/métrica e se isso se traduz para o agente-alvo do `workflow_coding_review`.
- Custo de execução (tamanho do dataset, necessidade de sandbox) para caber no molde `humaneval/`.
