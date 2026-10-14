# Convenções deste espaço

Repositório pessoal de organização de trabalho (não é código). Idioma: português.

O contrato de necessidades do sistema está em [VISAO.md](VISAO.md) (Documento de Visão). Mudanças de estrutura, convenção ou ferramenta devem ser avaliadas contra ele antes de aplicadas.

## Frentes e papéis

| Pasta | Projeto | Papel do Danillo |
|---|---|---|
| `simcaq/` | SimCAQ | Gestor e Tech Lead |
| `denodare/` | Denodare | Dev |
| `pdc-1/` | PDC 1 | Tech Lead e Pesquisador |
| `pdc-2/` | PDC 2 | Tech Lead e Pesquisador |
| `mestrado/` | Mestrado | Pesquisador |
| `dgolabs/terminus/` | Terminus (dgolabs) | Operador e mantenedor da IaC pessoal |
| `dgolabs/trantor/` | Trantor (dgolabs) | Criador e Operador do produto |
| `dgolabs/noesis/` | Noesis (dgolabs) | Criador e Operador do produto |
| `dgolabs/principles/` | Principles (dgolabs) | Criador e Operador do produto |
| `dgolabs/prisma/` | Prisma (dgolabs) | Criador e Operador do produto |
| `my-skills/` | my-skills | Criador e mantenedor de skills pessoais |

PDC 1 e PDC 2 são projetos independentes. `dgolabs/` agrupa projetos pessoais da rede dgolabs; Terminus é infraestrutura pessoal, não frente de trabalho externa; decisões arquiteturais ficam nos ADRs do próprio repositório, aqui só organização e operação. Trantor é o produto que absorve desenvolvimento de features e revisão de entregas; a unidade de acompanhamento na bandeja é o **épico** (`level/epic` no repo), não a sub-issue; release/deploy da imagem ficam em `dgolabs/terminus/`. Noesis é o produto de leitura científica → Zettelkasten; também acompanhado por épico, com gate de rigor (E10.2) bloqueando o pós-MVP; release/deploy ficam em `dgolabs/terminus/`.

## Onde cada coisa vai

| Tipo de conteúdo | Destino |
|---|---|
| Ata / notas de reunião | `<projeto>/reunioes/YYYY-MM-DD-assunto.md` |
| Mensagem, e-mail, texto em preparação | `<projeto>/rascunhos/YYYY-MM-DD-assunto.md` |
| Ação a fazer | `<projeto>/PENDENCIAS.md` (seção Urgente / Em aberto) |
| Decisão tomada | `<projeto>/DECISOES.md` (mais recente primeiro) |
| Pessoa nova ou mudança de papel | `<projeto>/PESSOAS.md` |
| Nota de paper / referência | `<projeto>/leituras/autor-ano-titulo-curto.md` + linha no índice |

## Regras ao registrar

1. **Toda reunião gera propagação.** Ao criar uma ata, extrair para os arquivos vivos: ações → `PENDENCIAS.md`, decisões → `DECISOES.md`, pessoas novas → `PESSOAS.md`, e adicionar linha na "Linha do tempo recente" do `README.md` do projeto.
2. **Links relativos** entre ata, rascunho e arquivos vivos (origem da pendência, fonte da decisão).
3. **Pendência encerrada não é apagada.** Concluída vai para "Concluídas" com `concluída em AAAA-MM-DD`; descartada vai para "Descartadas" com `descartada em AAAA-MM-DD — motivo: ...`.
4. **Datas** sempre `YYYY-MM-DD` em nomes de arquivo; `DD/MM/YYYY` no texto.
5. Não criar novas categorias de pasta sem necessidade; preferir arquivos datados nas pastas existentes.
6. **Agente altera pendências pelo `desk`, não pelo markdown.** Mudança pontual: `desk <verbo> <frente> <nº> --sim`. Várias mudanças: `desk triagem <frente> --exportar`, editar o buffer, mostrar ao usuário, `desk triagem <frente> --aplicar <arquivo>`. Edição direta de `PENDENCIAS.md` é saída de emergência.

## Estilo

- Tabelas para pessoas, ações e comparações; prosa curta para contexto.
- Rascunhos de mensagem mantêm o registro do canal e contexto no cabeçalho, com o texto pronto para copiar.
- Sem emojis.
