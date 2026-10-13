# Plano de Ações URGENTE - PDC1

---

## 📋 Resumo da Estratégia de Execução

1. **Fechar PRs de Benchmark**
   - Limpar e consolidar os Pull Requests do repositório `llm-definition-benchmark`.

2. **Avaliar Benchmarks Maduros & Poder de Decisão**
   - Filtrar as implementações de benchmark que entregam dados relevantes e comparações úteis para a tomada de decisão (ex.: HumanEval e Mbpp).

3. **Executar Benchmarks Selecionados**
   - Rodar o ciclo completo de execução apenas com as suítes e modelos selecionados que agregam valor real.

4. **Elaborar e Finalizar Relatório (Termo de Macroentrega)**
   - Preencher o Termo da Macro 3/4 com o que foi planejado vs. entregue.
   - Incluir dados do desenvolvimento dos agentes, inovações e gráficos comparativos com o estudo terciário da Macro 1.

5. **Elaborar e Finalizar Apresentação**
   - Construir os slides de finalização no modelo oficial, garantindo formato visual rico em figuras e gráficos de resultados.
   - Submeter o rascunho inicial para alinhamento e feedback da gestão (Ernesto / Mariana).

6. **Trabalhar na Confiança do Coder (Débitos Técnicos e Estabilidade)**
   - Anexar logs do servidor ao `ErrorReport` dos testes de interface.
   - Tratar exceções silenciosas/engolidas nas rotas.
   - Ajustar o *Context Engineer* (classificação técnica vs. homologação e flag `automatable`).
   - Expandir os testes de navegação para arestas de formulários.
   - Resolver problemas no sandbox (processos órfãos / porta 8000) e reparar testes unitários com falhas legadas.
