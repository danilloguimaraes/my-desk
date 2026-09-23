# PDC 1

**Meu papel:** Tech Lead e Pesquisador
**Status:** Fase de conclusão — pouco espaço para novas frentes; foco em fechamento

## Contexto

Projeto em fase de conclusão. Gestão de Mariana Crisostomo, coordenação de Renato Bulcão. Equipe de cinco pessoas dividida em duas frentes de desenvolvimento:

| Frente | Responsáveis | Situação |
|---|---|---|
| Testes em sistemas agênticos | Danilo Galvão | Primeira versão de PR em preparação, vinculada à issue [#373](https://github.com/PDC-ESIA/AI4ES/issues/373) (estratégia em 4 camadas, piloto no `workflow_coding_review`) |
| Benchmarks (conclusão) | Danillo | HumanEval pronto — falta executar com as LLMs definidas e gerar relatórios; MBPP a preparar. Referência: [documento do Ernesto](leituras/README.md) |
| Benchmarks (secundários) | Karol, Heitor, Gabriel, Wallisson | Um benchmark por pessoa (SWE-bench Verified, SlopCodeBench, CodeJudgeBench, BigCodeBench); ocupação, não entrega — não bloqueia a conclusão ([nota](reunioes/2026-09-22-benchmarks-propostas.md)) |

Objetivos indicados pela gestora para a fase de conclusão ([orientação de 22/09/2026](reunioes/2026-09-22-orientacao-gestora-objetivos.md)):

1. Documento de macro — identificar, mapear seções e atualizar.
2. Benchmark — apresentar HumanEval (pronto, falta executar) e MBPP (a preparar).
3. Compilado de tudo — escopo a esclarecer com a gestora.

Demandas paralelas às frentes:

- Publicar a versão atual em servidor (em contato com Danilo Ramos).
- Coletar feedback da equipe do ITA — depende da publicação.

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Quem é quem, papéis, contatos |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto, responsáveis, prazos |
| [DECISOES.md](DECISOES.md) | Registro de decisões |
| [reunioes/](reunioes/) | Atas datadas |
| [rascunhos/](rascunhos/) | Mensagens e textos em preparação |
| [leituras/](leituras/) | Notas de papers e referências |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 22/09/2026 | Contexto inicial registrado: equipe, frentes (testes agênticos e benchmarks) e demandas de fechamento |
| 22/09/2026 | Deploy: Danilo Ramos enviou arquivo da VPN e credenciais SSH. VPN conectou; SSH recusa a senha. Mensagem enviada ao Danilo Ramos pedindo a senha correta; aguardando resposta ([rascunho](rascunhos/2026-09-22-senha-ssh-servidor.md)) |
| 22/09/2026 | Testes agênticos: Danilo Galvão tem primeira versão de PR para discussão; pedido que vincule à issue [#373](https://github.com/PDC-ESIA/AI4ES/issues/373) já existente ([decisão](DECISOES.md)) |
| 22/09/2026 | Benchmarks: cada membro indicou um benchmark para um agente do `workflow_coding_review`; decidido molde comum em `humaneval/`, sem harness novo ([nota](reunioes/2026-09-22-benchmarks-propostas.md), [decisão](DECISOES.md)) |
| 22/09/2026 | Mariana orientou os três objetivos da conclusão: documento de macro, benchmark e "compilado de tudo" ([orientação](reunioes/2026-09-22-orientacao-gestora-objetivos.md)) |
| 22/09/2026 | Refinamento: benchmarks da apresentação são HumanEval e MBPP; propostas dos integrantes são secundárias. Documento do Ernesto guardado como referência ([decisão](DECISOES.md)) |
| 22/09/2026 | Indexados os 4 papers-fonte dos benchmarks recomendados à frente (SWE-bench, SlopCodeBench, BigCodeBench, CodeJudgeBench) em [leituras/](leituras/README.md) |
