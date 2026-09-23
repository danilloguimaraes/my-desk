# Benchmarks — workflow_coding_review (fase de proposta)

**Data:** 22/09/2026
**Tipo:** nota de alinhamento da frente de benchmarks (assíncrono)
**Participantes:** Danillo, Wallisson, Heitor, Gabriel, Karol, Danilo Galvão

## Contexto

Pedido inicial: cada membro indica **um** benchmark para **um** agente do `workflow_coding_review`, para virar issue.

## Distribuição

| Membro | Benchmark | Agente-alvo | Fonte |
|---|---|---|---|
| Wallisson | SWE-bench Verified | `executor` + `implementation_validator` + loop | `SWE-bench/SWE-bench_Verified` (HF) |
| Heitor | SlopCodeBench | `coder` (qualidade/verbosidade) | scbench.ai |
| Gabriel | CodeJudgeBench (split CodeRepair) | `reviewer` (LLM-as-judge) | `mattymchen/codejudgebench` (HF) |
| Karol | BigCodeBench (split `complete`) | `coder` (bibliotecas reais) | `bigcode/bigcodebench` (HF) |
| Danilo Galvão | Testes | — | issue existente ([#373](https://github.com/PDC-ESIA/AI4ES/issues/373)) |

## Decisões

- Um benchmark por pessoa; nada de harness novo. Todos espelham `benchmarks/coding_review/humaneval/` e produzem `results/run_*/{report.json,report.md,metadata.json}`. Registrada em [DECISOES.md](../DECISOES.md).

## Ações

Propagadas para [PENDENCIAS.md](../PENDENCIAS.md).

- [ ] Aguardar receptividade das propostas.
- [ ] Consolidar as 4 issues (rascunho do SWE-bench já pronto).
- [ ] Comunicar o molde comum (`humaneval/`) aos quatro antes de começarem.
- [ ] Alinhar Wallisson x Danilo Galvão sobre `feature/benchmarks-agente-testes`: referência, não dependência.
