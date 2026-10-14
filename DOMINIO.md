# My Desk — Modelo de Domínio

Criado em 13/10/2026. Acordo conceitual do sistema: vocabulário, classificação, ciclo de vida e invariantes dos quais derivam todos os formatos de dados. Este documento não descreve arquivos nem gramáticas — descreve o acordo do qual eles derivam; a materialização vem nos passos de arquitetura e solução e deve obedecê-lo.

**Natureza deste documento**: definição do projeto, não operação. Muda apenas por decisão deliberada do usuário.

## Regra fundamental: nada é ad hoc

Todo artefato do sistema é **instância de um conceito deste modelo**, com estrutura definida. Texto livre existe — mas apenas como **valor de um campo definido** dentro de uma instância (o contexto de uma decisão, o corpo de uma ata). Não existem documentos cuja forma não corresponda a nenhum conceito: aquilo que o modelo não conhece, não tem lugar no sistema.

Escopo da regra: o sistema operacional (as frentes e seus artefatos). Os documentos de definição do projeto (`VISAO.md`, `REQUISITOS.md`, este) estão fora do sistema modelado.

## Conceitos

**Fontes** — existem exatamente uma vez, dentro de uma frente:

| Conceito | O que é | Campos estruturados | Texto livre (como campo) |
|---|---|---|---|
| **Frente** | Unidade de trabalho contínua com papel e contexto próprios | identificador (nome da pasta), papel do usuário, situação (`ativa`/`pausada`/`arquivada`), estado resumido (uma linha) | contexto atual |
| **Pendência** | Item de trabalho que exige execução futura | descrição, situação (`aberta`/`concluída`/`descartada`), prioridade (`urgente`/`normal`), responsável, prazo (opcional), origem (link, quando houver), crítica (`sim`/`não`), data de encerramento (conclusão ou descarte), motivo do descarte | — |
| **Decisão** | Escolha registrada com sua razão | data, frente | contexto, decisão, consequências |
| **Ata** | Ocorrência datada de uma frente (reunião, checkpoint) | data, assunto | corpo — a prosa legítima da sessão; as ações e decisões dela nascem como Pendências/Decisões com `origem` apontando para cá |
| **Rascunho** | Mensagem em preparação | data, frente, canal, destinatário | contexto, texto pronto para copiar |
| **Pessoa** | Stakeholder de uma frente | nome, papel, frente | observações |
| **Nota de leitura** | Fichamento de referência (frentes de pesquisa) | referência, data | fichamento |

**Derivados** — existem por geração, nunca por manutenção:

| Projeção | Derivada de | Regra |
|---|---|---|
| **Painel de frentes** | Frentes com situação `ativa` | Nome, papel, estado resumido, próxima ação crítica |
| **Quadro de urgentes** | Pendências `aberta` + `urgente` de todas as frentes | Cada linha identifica a frente de origem |
| **Próxima ação crítica** (de uma frente) | A única Pendência `aberta` com `crítica = sim` | É a descrição dessa pendência, não texto independente |
| **Linha do tempo** | Atas e Decisões da frente, por data | Regenerada a cada registro |

## Ciclo de vida

- **Pendência**: `aberta` → `concluída` (com data) **ou** `aberta` → `descartada` (com data e motivo). Prioridade e o papel de crítica podem mudar enquanto aberta. Concluída e descartada são terminais: permanecem como histórico, nunca reaparecem e nunca são apagadas.
- **Frente**: `ativa` ⇄ `pausada` → `arquivada`. Frete arquivada sai das projeções e fica como histórico.

## Invariantes (a verificar, não a esperar)

1. Toda urgência existe exatamente uma vez, e é na sua frente; projeções a reproduzem por derivação.
2. Pendência encerrada (concluída ou descartada) não aparece como pendente em nenhuma projeção.
3. Toda frente ativa tem exatamente uma Pendência aberta marcada como crítica; pendência encerrada não carrega a marca.
4. A lista de frentes ativas é o conjunto de pastas contendo ficha com `situação = ativa` — não existe registro paralelo do conjunto de frentes.
5. Toda referência de `origem` é válida: o alvo existe.
6. Todo artefato corresponde a um conceito deste modelo (a regra fundamental, operacionalizada).
7. Nenhum derivado é editado à mão.

## Decisões resolvidas neste modelo

- **"Próxima ação crítica" é um papel** desempenhado por uma Pendência (`crítica = sim`), não um campo de texto da frente. Motivo: campo independente dessincroniza da realidade (a pendência morre e o campo continua); papel deriva, e a invariante 3 é verificável.
- **O conjunto de frentes tem o filesystem como fonte**: pasta + ficha com `situação`. Frente fantasma (Preleção) e frente não registrada (grupo_pesquisa) tornam-se impossíveis por construção. Consequência direta: a tabela de frentes do `AGENTS.md` e o espelho de urgentes do `README.md` são projeções e passam a ser geradas ou eliminadas — nunca mantidas.
- **Descarte é uma situação própria, não uma conclusão.** Motivo: a Visão (necessidade 3) promete que nada some até ser "resolvido ou descartado por mim"; sem a situação, descartar exigia concluir mentindo ou apagar a linha — as duas ferem a necessidade 2. O motivo é obrigatório para que o descarte não seja relitigado (necessidade 6). Aprovado em 13/10/2026.

## Ajuste aplicado a requisito aprovado

- **RF-N1.4** (critério de aceitação): alterado de "a consulta exige abrir exatamente um **documento**" para "a consulta usa exatamente um **ponto de consulta** (documento ou comando)". Motivo: a forma de apresentação pertence à solução; o compromisso da necessidade é o ponto único. Aprovado em 13/10/2026 e aplicado a `REQUISITOS.md`.
