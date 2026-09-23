# Decisões — PDC 1

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

---

## 22/09/2026 — Conclusão apresenta HumanEval e MBPP; benchmarks dos integrantes são secundários

**Contexto.** Após a distribuição de benchmarks à frente (SWE-bench Verified, SlopCodeBench, CodeJudgeBench, BigCodeBench), foi esclarecido o papel desses esforços na fase de conclusão. HumanEval já está implementado em `benchmarks/coding_review/humaneval/`. Ernesto desenvolveu a ideia dos benchmarks em [documento de referência](https://docs.google.com/document/d/1WNm1pLd5HGaMF8S3ljRa62f8wEwOJw1b/edit?usp=sharing&ouid=112129898684263745413&rtpof=true&sd=true).

**Decisão.** Os benchmarks da apresentação final são **HumanEval e MBPP**. As atividades atribuídas aos integrantes servem para mantê-los ocupados; resultados positivos são bem-vindos, mas a conclusão não conta com eles.

**Consequências.** Caminho crítico da frente de benchmarks: executar HumanEval com as LLMs definidas, coletar dados e gerar relatórios; preparar MBPP. As issues dos integrantes seguem, mas fora do caminho crítico. Ações em [PENDENCIAS.md](PENDENCIAS.md).

---

## 22/09/2026 — Um benchmark por pessoa, sem harness novo, espelhando `humaneval/`

**Contexto.** A frente de benchmarks (Wallisson, Heitor, Gabriel, Karol) precisava indicar benchmarks para os agentes do `workflow_coding_review`. Cada membro propôs um: SWE-bench Verified (`executor` + `implementation_validator` + loop), SlopCodeBench (`coder`, qualidade/verbosidade), CodeJudgeBench split CodeRepair (`reviewer`, LLM-as-judge) e BigCodeBench split `complete` (`coder`, bibliotecas reais). Detalhes na [nota](reunioes/2026-09-22-benchmarks-propostas.md).

**Decisão.** Um benchmark por pessoa, cada um virando uma issue. Nenhum harness novo: todos espelham a estrutura de `benchmarks/coding_review/humaneval/` e produzem `results/run_*/{report.json,report.md,metadata.json}`.

**Consequências.** Quatro issues a consolidar (rascunho do SWE-bench pronto). O molde comum precisa ser comunicado aos quatro antes de começarem. A branch `feature/benchmarks-agente-testes` (Danilo Galvão) serve de referência, não de dependência. Ações em [PENDENCIAS.md](PENDENCIAS.md).

---

## 22/09/2026 — Frente de testes agênticos usa a issue #373 como referência

**Contexto.** Danilo Galvão informou ter uma primeira versão de PR para discussão sobre testes em sistemas agênticos. Já existia no repositório a issue [PDC-ESIA/AI4ES#373 — "Coder: Reestruturação de Testes Agênticos"](https://github.com/PDC-ESIA/AI4ES/issues/373) (aberta em 10/08/2026, atribuída a ele), que propõe uma estratégia em 4 camadas (infraestrutura determinística, trace assertion, LLM-as-a-Judge, sandbox Docker) usando o pipeline `workflow_coding_review` como piloto.

**Decisão.** O trabalho da frente e o PR devem ser vinculados à issue #373, em vez de abrir issue nova ou PR solto.

**Consequências.** Discussão do PR concentrada em um único lugar já contextualizado; a issue passa a ser o registro oficial da frente. Ações em [PENDENCIAS.md](PENDENCIAS.md).
