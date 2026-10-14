# My Desk - Solucao

Criado em 13/10/2026. Materializacao concreta de [ARQUITETURA.md](ARQUITETURA.md): tecnologia, comandos, gramaticas e portao. E o documento que a implementacao obedece e que o `AGENTS.md` referencia.

**Natureza deste documento**: definicao do projeto. Mudancas de comando ou de gramática exigem atualizar aqui primeiro e depois a implementacao.

## Tecnologia

Python 3 (>= 3.10), stdlib apenas, com `desk.py` como motor e um wrapper `desk` na raiz. A UX final e `desk <comando>`, com testes em `test_desk.py` usando `unittest`.

## Referencia rapida

| Comando | O que faz | Quando usar |
|---|---|---|
| `desk` | Mostra o painel consolidado das frentes ativas, com a proxima acao critica de cada uma e a lista de urgentes | No inicio da sessao, para decidir onde olhar primeiro |
| `desk painel` | Mostra o mesmo painel de `desk` | Quando quiser explicitar o modo de painel |
| `desk frente <id>` | Mostra uma frente especifica com ficha, pendencias abertas e ultimos registros | Quando voce vai trabalhar em uma frente e quer contexto local |
| `desk check` | Verifica as invariantes do sistema e aponta inconsistencias | Antes de commitar ou quando o painel parecer suspeito |
| `desk add` | Coleta os campos e escreve uma pendencia no formato canonico | Quando voce quer registrar algo sem editar o arquivo na mao |

## Comandos

### `desk`

Exibe a tabela de frentes ativas com `Projeto`, `Meu papel`, `Status` e `Proxima acao critica`, e depois o quadro consolidado de urgentes.

Regras do painel:
- o comando roda a verificacao antes de exibir a saida;
- se houver inconsistencias, a contagem aparece no topo;
- a saida tenta ficar curta o suficiente para leitura rapida, e avisa quando cresce demais.

Exemplo:

```text
desk
```

### `desk frente <id>`

Mostra uma unica frente com:
- ficha resumida;
- pendencias abertas;
- ultimos registros;
- inconsistencias locais, se houver.

Exemplo:

```text
desk frente dgolabs/noesis
```

### `desk check`

Aplica as invariantes de [DOMINIO.md](DOMINIO.md) e retorna falhas legiveis. O comando falha com exit diferente de zero quando encontra qualquer inconsistência.

Use quando:
- quiser validar o estado inteiro do repositório;
- estiver antes de commit;
- estiver ajustando uma frente migrada ou um arquivo legado.

### `desk add`

Fluxo assistido para registrar uma pendencia em formato canonico.

O assistente pergunta, em ordem:
- frente;
- descricao;
- responsavel;
- urgente? [s/N];
- critica da frente? [s/N];
- prazo AAAA-MM-DD (vazio = nenhum);
- origem: caminho relativo ou URL (vazio = nenhuma).

Ele escreve a linha em `PENDENCIAS.md` da frente escolhida e ja usa a gramática canônica.

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

## Gramática de pendencia

Uma linha = uma pendencia em `PENDENCIAS.md`, dentro da seção da sua prioridade:

```text
## Urgente | ## Em aberto | ## Concluidas

- [ ] Descricao da acao — @Responsavel — AAAA-MM-DD — origem: <ref> — critica
- [x] Descricao — @Responsavel — concluida em AAAA-MM-DD — origem: <ref>
```

Regras:
- `[ ]` = aberta; `[x]` = concluida.
- A seção onde a linha vive define sua prioridade.
- Campos sao separados por ` — `.
- Os marcadores aceitos sao: `@` para responsavel, data ISO para prazo, `origem: <ref>` para vinculo, `critica` para a pendencia critica da frente e `concluida em AAAA-MM-DD` para itens fechados.
- Responsavel e obrigatorio.
- Datas de dado sao sempre ISO (`AAAA-MM-DD`).

## Exemplo de arquivo de pendencias

```text
# Pendencias - Noesis

## Urgente

- [ ] Reconciliar status de E10.2 #44 — @Danillo — 2026-09-26 — critica

## Em aberto

- [ ] Abrir issue para escapes de impasse — @Danillo — sem prazo — origem: simulação P6/P7

## Concluidas

- [x] E10.2 #44 Homologar hipotese de rigor — @Danillo — concluida em 2026-09-26
```

## Ficha da frente

Topo de `<frente>/README.md`:

```text
# <Nome da frente>

| campo | valor |
|---|---|
| situacao | ativa |
| papel | <papel do usuario> |
| estado | <estado resumido, uma linha> |

<contexto livre...>
```

`situacao` pode ser `ativa`, `pausada` ou `arquivada`.

## Portao

Hook em `.githooks/pre-commit` executando `./desk.py check`.

Instalacao uma vez por clone:

```text
git config core.hooksPath .githooks
```

## Erros comuns

| Sintoma | Causa provavel | Como corrigir |
|---|---|---|
| `ficha ausente` | `README.md` sem tabela `| campo | valor |` | Criar o topo canonico da frente |
| `pendencia concluida sem 'concluida: AAAA-MM-DD'` | Item fechado sem data no formato esperado | Trocar para `concluida em AAAA-MM-DD` |
| `pendencia concluida fora de 'Concluidas'` | Item `[x]` fora da secao certa | Mover a linha para `## Concluidas` |
| `frente ativa precisa de exatamente 1 pendencia aberta critica` | A frente ativa nao tem uma critica aberta, ou tem mais de uma | Deixar exatamente uma linha aberta marcada com `critica` |
| `origem inexistente` | Origem nao aponta para arquivo local existente nem URL | Corrigir o caminho ou usar uma URL |

## Proximos passos

1. Manter `desk.py` e `test_desk.py` como referencia viva da implementacao.
2. Usar `desk check` como portao de consistencia antes de commit.
3. Atualizar este documento primeiro sempre que a gramática ou os comandos mudarem.
