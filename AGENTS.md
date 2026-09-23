# Convenções deste espaço

Repositório pessoal de organização de trabalho (não é código). Idioma: português.

## Frentes e papéis

| Pasta | Projeto | Papel do Danillo |
|---|---|---|
| `simcaq/` | SimCAQ | Gestor e Tech Lead |
| `denodare/` | Denodare | Dev |
| `pdc-1/` | PDC 1 | Tech Lead e Pesquisador |
| `pdc-2/` | PDC 2 | Tech Lead e Pesquisador |
| `mestrado/` | Mestrado | Pesquisador |

PDC 1 e PDC 2 são projetos independentes.

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
2. **Painel raiz espelha o urgente.** Pendências marcadas como Urgente em qualquer projeto aparecem também em `README.md` da raiz; ao concluir, remover de ambos.
3. **Links relativos** entre ata, rascunho e arquivos vivos (origem da pendência, fonte da decisão).
4. **Pendência concluída** move para a seção "Concluídas" com data, não é apagada.
5. **Datas** sempre `YYYY-MM-DD` em nomes de arquivo; `DD/MM/YYYY` no texto.
6. Não criar novas categorias de pasta sem necessidade; preferir arquivos datados nas pastas existentes.

## Estilo

- Tabelas para pessoas, ações e comparações; prosa curta para contexto.
- Rascunhos de mensagem mantêm o registro do canal e contexto no cabeçalho, com o texto pronto para copiar.
- Sem emojis.
