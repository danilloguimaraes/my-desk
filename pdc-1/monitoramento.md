# Planejamento

## llm-definition-benchmark
Selecionei os seguintes LLMs e executei até o momento 2 benchmarks (HumanEval e Mbpp): 
- anthropic/claude-haiku-5.5
- deepseek/deepseek-v4-flash-0731
- openai/gpt-6-luna
- qwen/qwen3.7-flash

## Revisar entrega e selecionar benchmark 
Após integração no github, verificar se algum desses benchmarks pode agregar na apresentação de finalização. 
Se alguma dessas implementações de benchmark estiver madura, e entregar valor à apresentação, então, verificar a possibilidade 
de executar o ciclo completo com todos LLMs selecionados. 

## Preenchimento de artefatos para finalização 
Penso que os artefatos de finalização são: 
- Apresentação 
- Relatórios 

Elaborar a primeira versão de apresentação e mostrar para o Ernesto para colher seu feedback. 

## Melhorar resultado do coding review
Seguem as anotações que tirei de um esforço passado: 
```
A branch seguiu oito objetivos, apresentados aqui na ordem em que surgiram. Os pontos em aberto, que não chegaram a ser implementados, estão no fim.

## 1. Medir e reduzir o consumo de tokens
- **Medição:** o contador passou a separar os tokens servidos do cache (`cached`), e criei um painel lateral de tokens no Claude Code (fora do repositório).
- **Contexto enxuto do coder (`AI4ES_CODER_CONTEXTO_ENXUTO`):**
  - a task atual vai no state (`current_task`) e o turno abre com um evento curto;
  - coder, executor e revisor rodam com `include_contents="none"`;
  - o prompt diz "implemente só esta task" e avisa, sem bloquear, quando um arquivo sai do escopo.
- **Teto de chamadas de LLM configurável** (`AI4ES_MAX_LLM_CALLS`), passado ao `RunConfig` do orchestrator.
- **Resultado medido:** o coder caiu de ~59k para ~19k tokens por chamada, o executor de ~62k para ~6k e o revisor de ~218k para ~39k.

## 2. Feedback rápido sem fixar o ambiente
- **Trilhas (`AI4ES_TRILHAS`):**
  - a trilha `python-web` usa Python 3.12 via uv, com constraints de dependências pinadas e notas de armadilhas conhecidas da stack no prompt;
  - a trilha `python-generic` fixa só o interpretador;
  - stacks fora das trilhas continuam livres.
- **Verificação rápida antes do harness (`AI4ES_VERIFICACAO_RAPIDA`):**
  - com trilha: venv em cache, `compileall`, import do módulo de entrada e `pytest --collect-only`;
  - sem trilha: revisão por LLM, que só bloqueia com confiança alta.

## 3. Critérios de aceite que decidem de verdade (aceite independente)
- **Autor de aceite independente (`AI4ES_ACEITE_INDEPENDENTE`):**
  - um agente separado escreve `tests/acceptance/test_aceite_<TASK>.py` a partir dos critérios;
  - o vínculo com o critério sai do nome do teste (`test_CA_NN_*`), e o mapa fica fora do alcance do coder;
  - o coder não pode editar esses testes.
- **Harness decide critério** (`atendido` / `nao_atendido`), e o validador reprova quando há critério não atendido.
- **Robustez operacional:**
  - testes protegidos rodam isolados, numa cópia limpa do projeto;
  - falhas já aceitas não reprovam as tasks seguintes (linha de base);
  - task travada em teste protegido é encerrada por um teto de rodadas;
  - `exit_loop` só encerra o loop com veredito aprovado;
  - a saída do pytest ficou legível para o coder (`-p no:warnings --tb=short -rfE`).
- **O autor roda o próprio teste** antes de entregar.
- **Regras de prompt:** afirmar só comportamento observável; resolver o caminho citado no critério a partir de `MEDIA_DIR`.

## 4. Testar o produto integrado (jornada)
- **Autor da jornada (`AI4ES_JORNADA`):** escreve o teste de ponta a ponta a partir das HUs, executado contra o produto subido pelo `run.json`.
- **Falha da jornada vira task de integração** (TASK-901…), limitada por `AI4ES_JORNADA_MAX_RODADAS`.
- **Jornada web pelo navegador (Playwright):**
  - um conftest protegido reprova respostas 4xx/5xx e erros de JavaScript;
  - ficam proibidos atalhos que pulam a interface: HTTP direto, `evaluate` e injeção de scripts;
  - `goto` só pode abrir "/".

## 5. Critério de aceite como homologação (o frontend é o aceite em web_app)
- **Toda task web_app tem homologação pela interface:**
  - os critérios não técnicos são testados pelo navegador em `test_interface_<TASK>.py`;
  - uma task web sem critério de homologação é recusada ao salvar.
- **Técnico só anota, nunca reprova nem gera retrabalho:**
  - a marca `tecnico` e a suíte do próprio coder ficam fora da nota e do status e aparecem como `notas_tecnicas`;
  - essas notas saem do ErrorReport enviado ao coder.

## 6. Testes de interface robustos (sem travas falsas)
- **Localizadores:** só identificador único (`data-testid`); em listas, filtrar pelo conteúdo; ordem só quando o critério pedir.
- **Lint determinístico ao salvar** recusa:
  - `lambda` em asserção;
  - `.first`, `.last` e `.nth`;
  - `try/except` e `if ...count()`;
  - seletor por classe CSS;
  - `to_have_url` e `page.url`;
  - `assert` com leitura imediata.
- **Inventário de identificadores existentes**, e recusa de identificador novo equivalente a um já usado.
- **Reparo pelo autor:**
  - erro do próprio teste volta ao autor, no máximo 2 vezes por task;
  - a rodada com esse erro não conta para o teto.
- **Helpers determinísticos no conftest** (`nome_unico`, `imagens`), convenção única de identificador (`app/ids.py`) e regra contra exigir formato que o critério não pede.

## 7. Visão do produto inteiro (big picture)
- **Quadro do produto (`AI4ES_QUADRO_PRODUTO`):** resumo determinístico, inspirado no repo map do Aider, que entra no prompt antes de cada task.
  - Camada genérica: o que já foi homologado, os testes de regressão, os `data-testid` e os arquivos.
  - Camada python-web: rotas, modelos e templates, extraídos por `ast`.

## 8. Top-down a partir do design (web_app)
- **Contrato de interface (`AI4ES_CONTRATO_WEB`), derivado do design antes da 1ª task:**
  - telas com marcador e `data-testid` por elemento;
  - rotas com formato e campos;
  - mapa de navegação, design system, decisões e suposições.
- **Validação determinística do contrato.** Coder e autor de aceite trabalham presos a ele; teste com identificador fora do contrato é recusado.
- **Teste de navegação gerado do contrato, sem LLM,** percorrendo as arestas por link.
- **`identificadores_ausentes` no ErrorReport.**
- **Conformidade com o design, só anotada:** aderência dos elementos, estilo referenciado, rotas e alcance das telas.
- **Trilha python-web:** esqueleto (`app/ids.py` e o CSS do design) e conferência das rotas.

## Lições e pontos em aberto (não implementados)
- **Diagnóstico de defeito real (16ª execução):**
  - anexar o log do servidor, coletado depois do teste, à falha do teste de interface;
  - proibir engolir exceções nas rotas.
- **Context engineer:** classifica mal o que é técnico e o que é homologação, e às vezes marca homologação como `automatable: false`.
- **Arestas de navegação por envio de formulário** não são cobertas pelo teste gerado.
- **Infraestrutura:**
  - processos de serviço do sandbox ficam órfãos quando a execução é interrompida (porta 8000 presa);
  - 14 testes unitários já falhavam antes da branch.
- **Padrão observado:** a cada execução surgia um contorno novo dos agentes, e a correção caso a caso escalou. O contrato top-down ataca a causa: agentes decidindo partes da interface isoladamente. Vale começar o projeto novo por ele.
```