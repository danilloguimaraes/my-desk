# My Desk — Solução

Criado em 13/10/2026. Materialização concreta de [ARQUITETURA.md](ARQUITETURA.md): tecnologia, gramáticas, comandos e portão. É o documento que a implementação obedece e que o `AGENTS.md` referencia.

**Natureza deste documento**: definição do projeto. Mudanças de gramática ou de comando exigem alterar aqui primeiro (contrato), depois a implementação.

## Tecnologia

Python 3 (≥ 3.10), **stdlib apenas**, com `desk.py` como motor e um wrapper `desk` na raiz — a UX final é `desk <comando>`, com testes em `test_desk.py` usando `unittest`. Sem pip, sem venv, sem dependências.

## Comandos

| Comando | O que faz | Pureza |
|---|---|---|
| `desk` | Painel: tabela de frentes ativas (nome, papel, estado, próxima ação crítica) + quadro de urgentes consolidado. Antes de exibir, roda a verificação e anexa a contagem de inconsistências (não oculta a projeção). Se a saída passar de ~40 linhas, avisa | Leitura |
| `desk frente <id>` | Visão de uma frente: ficha, urgentes, crítica, últimos registros | Leitura |
| `desk check` | Aplica as invariantes de [DOMINIO.md](DOMINIO.md); relatório legível das falhas, exit ≠ 0 se houver qualquer uma | Verificação |
| `desk add` | Via assistida: pergunta campo a campo (`frente`, entidade pendência/decisão/pessoa, seus campos) e escreve a linha canônica no arquivo certo | Escrita assistida |

## Gramática de pendência

Uma linha = uma Pendência, em `PENDENCIAS.md`, dentro da seção da sua prioridade:

```
## Urgente | ## Em aberto | ## Concluídas

- [ ] Descrição da ação — @Responsável — AAAA-MM-DD — origem: <ref> — crítica
- [x] Descrição — @Responsável — concluída: AAAA-MM-DD — origem: <ref>
```

- Situação: `[ ]` aberta, `[x]` concluída. Prioridade: a seção onde a linha vive. 
- Campos após a descrição são separados por ` — `, identificados por forma, em qualquer ordem: `@` = responsável; data = prazo; `origem: <ref>` = vínculo (caminho relativo ou URL); `crítica` = marca a Pendência como a crítica da frente; `concluída: AAAA-MM-DD` só em `[x]`.
- Opcionais: prazo, origem, crítica. Responsável é obrigatório por ser curto demais para esquecer.
- Datas no dado sempre ISO (`AAAA-MM-DD`), como nos nomes de arquivo; o `DD/MM/AAAA` da casa continua valendo para prosa.

## Ficha da frente

Topo de `<frente>/README.md`: tabela de campos + contexto livre em prosa abaixo.

```
# <Nome da frente>

| campo | valor |
|---|---|
| situacao | ativa |
| papel | <papel do usuário> |
| estado | <estado resumido, uma linha> |

<contexto livre…>
```

`situacao ∈ {ativa, pausada, arquivada}`. O conjunto de frentes ativas é o das pastas com `situacao = ativa` (invariante 4).

## Portão

Hook em `.githooks/pre-commit` do repo executando `./desk.py check`; recusa o commit se falhar. Instalação (uma vez por clone): `git config core.hooksPath .githooks`.

## Próximos passos (execução, não mais decisão)

1. Implementar `desk.py` + `test_desk.py`.
2. Reescrever `AGENTS.md`: sai a tabela de frentes, entram gramática, comandos e o fluxo (via conversada com `desk check` no fim).
3. Migrar o estado atual (lista em [ARQUITETURA.md](ARQUITETURA.md)); bloqueios seus: destino de `grupo_pesquisa` e de Preleção.
