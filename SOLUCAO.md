# My Desk - Solução

Criado em 13/10/2026. Materialização concreta de [ARQUITETURA.md](ARQUITETURA.md): tecnologia, comandos, gramáticas e portão. É o documento que a implementação obedece e que o `AGENTS.md` referencia.

**Natureza deste documento**: definição do projeto. Mudanças de comando ou de gramática exigem atualizar aqui primeiro e depois a implementação.

## Tecnologia

Python 3 (>= 3.10), stdlib apenas, com `desk.py` como motor e um wrapper `desk` na raiz. A UX final é `desk <comando>`, com testes em `test_desk.py`, `test_escrita.py` e `test_triagem.py`, executados com `python3 -m unittest`.

## Referência rápida

| Comando | O que faz | Quando usar |
|---|---|---|
| `desk` | Mostra o painel consolidado das frentes ativas, com a próxima ação crítica de cada uma e a lista de urgentes | No início da sessão, para decidir onde olhar primeiro |
| `desk painel` | Mostra o mesmo painel de `desk` | Quando quiser explicitar o modo de painel |
| `desk frente <id>` | Mostra uma frente específica com ficha, pendências abertas e últimos registros | Quando você vai trabalhar em uma frente e quer contexto local |
| `desk check` | Verifica as invariantes do sistema e aponta inconsistências | Antes de commitar ou quando o painel parecer suspeito |
| `desk add` | Coleta os campos e escreve uma pendência no formato canônico | Quando você quer registrar algo sem editar o arquivo na mão |
| `desk feito\|descartar\|urgente\|normal\|critica <frente> [nº\|trecho]` | Muda a situação, a prioridade ou a crítica de uma pendência | Quando uma pendência muda de situação, prioridade ou crítica |
| `desk triagem <frente>` | Revisa as pendências de uma frente de uma vez, num buffer de editor | No fechamento de sessão ou para revisar a frente de uma vez |

`<frente>` aceita o id completo ou só o último segmento, quando ele é único (`noesis` -> `dgolabs/noesis`).

## Comandos

### `desk`

Exibe a tabela de frentes ativas com `Projeto`, `Meu papel`, `Status` e `Próxima ação crítica`, e depois o quadro consolidado de urgentes.

Regras do painel:
- o comando roda a verificação antes de exibir a saída;
- se houver inconsistências, a contagem aparece no topo;
- a saída tenta ficar curta o suficiente para leitura rápida, e avisa quando cresce demais.

Exemplo:

```text
desk
```

### `desk frente <id>`

Mostra uma única frente com:
- ficha resumida;
- pendências abertas, numeradas;
- últimos registros;
- inconsistências locais, se houver.

O número exibido em cada pendência aberta é o usado pelos verbos de transição e pela triagem, e vale para a versão atual do arquivo `PENDENCIAS.md`.

Exemplo:

```text
desk frente dgolabs/noesis
```

### `desk check`

Aplica as invariantes de [DOMINIO.md](DOMINIO.md) e retorna falhas legíveis. O comando falha com exit diferente de zero quando encontra qualquer inconsistência.

Use quando:
- quiser validar o estado inteiro do repositório;
- estiver antes de commitar;
- estiver ajustando uma frente migrada ou um arquivo legado.

### `desk add`

Fluxo assistido para registrar uma pendência em formato canônico.

O assistente pergunta, em ordem:
- frente;
- descrição;
- responsável;
- urgente? [s/N];
- crítica da frente? [s/N];
- prazo AAAA-MM-DD (vazio = nenhum);
- origem: caminho relativo ou URL (vazio = nenhuma).

Ele escreve a linha em `PENDENCIAS.md` da frente escolhida e já usa a gramática canônica.

Exemplo:

```text
desk add
Frente: dgolabs/noesis
Descrição: Abrir issue para escapes de impasse
Responsável (nome): Danillo
Urgente? [s/N]: s
Crítica da frente? [s/N]: n
Prazo AAAA-MM-DD (vazio = nenhum):
Origem: caminho relativo ou URL (vazio = nenhuma):
```

### Verbos de transição

Mudam uma pendência existente sem reescrever a linha à mão.

Forma:

```text
desk <verbo> <frente> [nº | trecho do texto...] [--sim] [--motivo TEXTO]
```

Verbos:
- `feito`: concluir a pendência;
- `descartar`: descartar a pendência (exige `--motivo`);
- `urgente`: move a pendência para `## Urgente`;
- `normal`: move a pendência para `## Em aberto`;
- `critica`: transfere a marca de crítica da frente para a pendência escolhida.

Seleção:
- `nº` casa com a numeração de `desk frente`;
- `trecho` casa sem diferenciar maiúsculas de minúsculas;
- um só resultado é usado diretamente; vários resultados abrem um menu (com `--sim`, o comando falha pedindo o nº).

Confirmação: o comando mostra o antes e o depois e pede confirmação; `--sim` pula a confirmação.

Crítica: ao concluir ou descartar a pendência crítica de uma frente ativa, é preciso escolher a sucessora. Com `--sim`, o comando falha orientando a usar `desk critica`.

Motivo: `--motivo` não pode conter ` — `, porque esse separador pertence ao formato da linha.

Validação: a mudança é recusada, sem gravar, se criar uma inconsistência nova.

### `desk triagem <frente>`

Revisa de uma vez as pendências abertas de uma frente.

Uso humano: abre `$VISUAL` ou `$EDITOR` (padrão `vi`) com o buffer de triagem. Erros voltam ao editor como linhas `# ! ...` no topo. Um buffer sem itens, ou um editor com erro, cancela a triagem.

Uso por agente: `desk triagem <frente> --exportar > buf.md`, editar `buf.md`, e então `desk triagem <frente> --aplicar buf.md` (ou `--aplicar -` para ler da entrada padrão). A versão no cabeçalho recusa um buffer cujo arquivo já foi alterado.

Formato do buffer:

```text
# desk triagem dgolabs/noesis — versão 3f9a1c07
# Marcas: [ ] aberta · [x] concluir hoje · [-] descartar (exige '— motivo: ...')
# Mover a linha para a outra seção muda a prioridade. '— crítica' marca a crítica da frente.
# Linha sem número = pendência nova (exige @responsável). Apagar linha numerada é erro.
# Remover todas as linhas de item cancela. Linhas iniciadas por '#' são ignoradas.

## Urgente
1 [ ] Reconciliar status de **E10.2 #44** — @Danillo — 2026-09-26 — crítica

## Em aberto
# ### Bloqueio de infraestrutura (Terminus)
2 [ ] **#87** Publicar imagem multi-arch no GHCR — workflow de publish no repo do produto — @Danillo — sem prazo
```

Regras:
- o número é a chave do item nesta versão do arquivo;
- mover a linha para outra seção muda a prioridade;
- subseções `###` aparecem como comentário e não são reordenadas;
- pendências encerradas entram no topo de `Concluídas` ou `Descartadas`;
- a versão é o início do SHA-256 do arquivo.

## Gramática de pendência

Uma linha = uma pendência em `PENDENCIAS.md`, dentro da seção da sua prioridade:

```text
## Urgente | ## Em aberto | ## Concluídas | ## Descartadas

- [ ] Descrição da ação — @Responsável — AAAA-MM-DD — origem: <ref> — crítica
- [x] Descrição — @Responsável — concluída em AAAA-MM-DD — origem: <ref>
- [-] Descrição — @Responsável — descartada em AAAA-MM-DD — motivo: <texto>
```

Regras:
- `[ ]` = aberta; `[x]` = concluída; `[-]` = descartada.
- A seção onde a linha vive define sua prioridade.
- Campos são separados por ` — `.
- Os marcadores aceitos são: `@` para responsável, data ISO para prazo, `origem: <ref>` para vínculo, `crítica` para a pendência crítica da frente, `concluída em AAAA-MM-DD` para itens concluídos, e `descartada em AAAA-MM-DD` com `motivo: <texto>` para itens descartados.
- Responsável é obrigatório.
- Datas de dado são sempre ISO (`AAAA-MM-DD`).
- Pendência encerrada não carrega `crítica`.
- Lista numerada (`1. [ ]`) não é pendência; o `desk check` a denuncia.
- `motivo` não pode conter ` — `.

## Exemplo de arquivo de pendências

```text
# Pendências - Noesis

## Urgente

- [ ] Reconciliar status de E10.2 #44 — @Danillo — 2026-09-26 — crítica

## Em aberto

- [ ] Abrir issue para escapes de impasse — @Danillo — sem prazo — origem: simulação P6/P7

## Concluídas

- [x] E10.2 #44 Homologar hipótese de rigor — @Danillo — concluída em 2026-09-26
```

## Ficha da frente

Topo de `<frente>/README.md`:

```text
# <Nome da frente>

| campo | valor |
|---|---|
| situacao | ativa |
| papel | <papel do usuário> |
| estado | <estado resumido, uma linha> |

<contexto livre...>
```

`situacao` pode ser `ativa`, `pausada` ou `arquivada`.

## Portão

Hook em `.githooks/pre-commit` executando `./desk.py check`.

O hook fica em `.githooks/pre-commit` e é criado numa tarefa posterior.

Instalação uma vez por clone:

```text
git config core.hooksPath .githooks
```

## Erros comuns

| Sintoma | Causa provável | Como corrigir |
|---|---|---|
| `ficha ausente` | `README.md` sem tabela `| campo | valor |` | Criar o topo canônico da frente |
| `pendência concluída sem 'concluída em AAAA-MM-DD'` | Item fechado sem data no formato esperado | Trocar para `concluída em AAAA-MM-DD` |
| `pendência concluída fora de 'Concluídas'` | Item `[x]` fora da seção certa | Mover a linha para `## Concluídas` |
| `frente ativa precisa de exatamente 1 pendência aberta crítica` | A frente ativa não tem uma crítica aberta, ou tem mais de uma | Deixar exatamente uma linha aberta marcada com `crítica` |
| `origem inexistente` | Origem não aponta para arquivo local existente nem URL | Corrigir o caminho ou usar uma URL |
| `pendência em lista numerada` | Pendência escrita como `1. [ ]` | Trocar por `- [ ]` |
| `pendência descartada sem 'motivo: ...'` | Descarte sem motivo | Acrescentar `— motivo: ...` |
| `... sumiram do buffer` | Linha numerada apagada na triagem | Encerrar com `[x]` ou `[-]`, não apagar |
| `motivo não pode conter ' — '` | Separador no motivo | Reescrever o motivo sem ` — ` |

## Próximos passos

1. Manter `desk.py`, `desk_escrita.py`, `desk_triagem.py` e os testes como referência viva.
2. Usar `desk check` como portão.
3. Atualizar este documento antes de mudar gramática ou comandos.

