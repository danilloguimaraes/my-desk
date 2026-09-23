# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

**Autores:** Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.; Press, O.; Narasimhan, K.
**Ano:** 2023 (ICLR 2024)
**Fonte:** https://arxiv.org/abs/2310.06770
**Status:** A ler
**Relação com o projeto:** recomendado a Wallisson para a proposta de benchmark **SWE-bench Verified** (agente-alvo: `executor` + `implementation_validator` + loop) — ver [nota de propostas](../reunioes/2026-09-22-benchmarks-propostas.md). Atividade secundária; não bloqueia a conclusão.

## Do que trata

Resolução de issues reais do GitHub em repositórios Python; avalia se o patch gerado passa nos testes. A variante Verified (500 instâncias validadas por humanos) é a usada na proposta.

## Notas de leitura

_a preencher_

## O que quero entender

- Como o benchmark define sucesso/métrica e se isso se traduz para o agente-alvo do `workflow_coding_review`.
- Custo de execução (tamanho do dataset, necessidade de sandbox) para caber no molde `humaneval/`.
