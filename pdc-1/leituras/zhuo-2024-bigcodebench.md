# BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions

**Autores:** Zhuo, T. Y.; Vu, M. C.; Chim, J.; Hu, H.; Yu, W.; Widyasari, R. et al.
**Ano:** 2024
**Fonte:** https://arxiv.org/abs/2406.15877
**Status:** A ler
**Relação com o projeto:** recomendado a Karol para a proposta de benchmark **BigCodeBench (split `complete`)** (agente-alvo: `coder` (bibliotecas reais)) — ver [nota de propostas](../reunioes/2026-09-22-benchmarks-propostas.md). Atividade secundária; não bloqueia a conclusão.

## Do que trata

Geração de código com chamadas a bibliotecas reais e instruções complexas; 1.140 tarefas, 139 bibliotecas. Split `complete` parte da docstring completa.

## Notas de leitura

_a preencher_

## O que quero entender

- Como o benchmark define sucesso/métrica e se isso se traduz para o agente-alvo do `workflow_coding_review`.
- Custo de execução (tamanho do dataset, necessidade de sandbox) para caber no molde `humaneval/`.
