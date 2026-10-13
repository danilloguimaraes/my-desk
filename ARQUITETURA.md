# My Desk — Arquitetura

Criado em 13/10/2026. Decide como os conceitos de [DOMINIO.md](DOMINIO.md) se materializam em componentes e fluxos. Sintaxe concreta de formatos, nomes de comandos e mecanismos de execução ficam para o passo 3 (solução).

**Natureza deste documento**: definição do projeto, não operação. Muda apenas por decisão deliberada do usuário.

## Componentes

| Componente | Papel | Fronteira |
|---|---|---|
| **Estado** | Arquivos markdown por conceito-fonte, em layout fixo por frente | Editável por humano e LLM; nunca escrito por ferramenta |
| **Ingestão** | Experiência desenhada em duas vias — conversada (despejo livre estruturado pelo agente) e assistida (comando que pergunta os campos e escreve a linha canônica) — convergindo para a Verificação; edição direta é saída de emergência | A gramática nunca é carga do usuário |
| **Verificação** | Comando `desk check` (nome provisório) que aplica as invariantes do modelo; portão obrigatório de persistência | Somente leitura sobre o estado; falha produz relatório e bloqueia o commit |
| **Derivação** | Cálculo das projeções no momento da consulta | Nunca materializa resultado em arquivo, nunca é commitada |
| **Apresentação** | CLI de leitura: painel, urgentes, frente individual | O único ponto de consulta (RF-N1.4); não conhece escrita |

## Layout do estado

```
<frente>/
  README.md      # ficha da Frente: seção estruturada (campos) + contexto livre abaixo
  PENDENCIAS.md  # coleção de Pendências, uma gramática por linha
  DECISOES.md    # coleção de Decisões
  PESSOAS.md     # coleção de Pessoas
  reunioes/      # Atas: YYYY-MM-DD-assunto.md
  rascunhos/     # Rascunhos de mensagem
  leituras/      # Notas de leitura (frentes de pesquisa)
```

## Fluxos

- **Leitura do dia**: o usuário roda o comando → Derivação lê o Estado → Apresentação exibe painel/urgentes/frente.
- **Sessão de ingestão**: via conversada ou assistida → `desk check` como portão de commit (AD-6) → verde, o estado vira oficial.
- **Agente LLM**: mesmo fluxo da ingestão; `AGENTS.md` é seu contrato (gramáticas + comandos), conforme AD-5.

## Decisões arquiteturais

- **AD-1 · Projeções são sob demanda, nunca materializadas.** Alternativa descartada: gerar o painel como arquivo commitado (o README.md raiz atual). Motivo: projeção materializada é dessincronização adiada — depende de regeneração disciplinada, exatamente o modo de falha do sistema atual; projeção sem estado próprio não pode dessincronizar. Consequência: o README.md raiz deixa de ser painel e vira ficha estática do repositório; a seção "Pendências urgentes" e a tabela de frentes morrem como artefatos mantidos.
- **AD-2 · Ingestão é uma experiência desenhada em duas vias, com edição direta como escape.** **Via conversada** (a principal): o usuário despeja em texto livre o que aconteceu, e o agente estrutura conforme o contrato — UX de falar, revisar, aprovar. **Via assistida**: para entidades atômicas (pendência, decisão, pessoa), um comando pergunta campo a campo e escreve a linha canônica — a gramática some atrás das perguntas. A edição direta dos arquivos permanece possível por construção, mas deixa de ser o caminho projetado e vira saída de emergência. Alternativa descartada: captura por flags (`desk add --frente x ...`) — engaiola o texto livre que o modelo preserva como campo e transfere a gramática para o usuário.
- **AD-3 · Código no próprio repositório, stdlib apenas.** Sem instalação externa, sem serviço, sem dependências: o verificador/consulta viaja junto com o estado e roda em qualquer máquina com Python. Consequência direta da restrição de manutenção desprezível.
- **AD-4 · A ficha da frente é o README.md da própria frente**, com uma seção estruturada (campos da Frente) no topo e o contexto livre abaixo. Alternativa descartada: arquivo separado (`FRENTE.md`) — reusa o que já existe em todas as frentes e reduz a migração.
- **AD-5 · AGENTS.md muda de papel.** Deixa de registrar o conjunto de frentes (a fonte é o filesystem, por decisão do modelo) e passa a registrar as gramáticas de ingestão e o contrato do agente. A tabela de frentes sai dele.
- **AD-6 · O estado só pode ser persistido válido.** `desk check` deixa de ser comando eventual e vira **portão obrigatório de commit** (hook local de pre-commit): estado inválido não entra no repositório. Motivo: o estado tem múltiplos canais de escrita (humano, LLM, merge, edição direta), e validação na entrada de um único canal nunca garante os demais — a consistência só é garantível no ponto onde o estado se torna oficial. Se um dia houver repositório remoto, a CI repete o mesmo check.

## Cobertura dos requisitos de N1

RF-N1.1–N1.3 ← Derivação + Apresentação · RF-N1.4 ← ponto único de consulta (CLI) · RF-N1.5 ← responsabilidade da Apresentação (saída enxuta).

## Migração pendente (não executada neste passo)

Ao aplicar esta arquitetura ao estado atual: normalizar as fichas das frentes; remapear os artefatos da Família B (denodare, pdc-1, pdc-2, mestrado, grupo_pesquisa) para conceitos do modelo; decidir o destino de `grupo_pesquisa` (frente formal ou remoção) e de Preleção (criar a pasta ou abandonar a frente); decidir o `PESSOAS.md` do trantor; converter as pendências existentes para a gramática canônica. Os dois primeiros itens de decisão são seus e bloqueiam a migração.

## Fora deste passo (vai para a Solução)

Sintaxe das gramáticas (pendência, ficha, decisão), formato da seção estruturada da ficha, nomes e comportamento exato dos comandos, instalação do hook de pre-commit.
