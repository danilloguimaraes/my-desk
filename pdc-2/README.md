# PDC 2

**Meu papel:** Tech Lead e Pesquisador
**Status:** Onboarding (primeiro ciclo)
**Alocação:** Frente 2 — Knowledge Graph e Sistemas Legados; grupo de construção do Knowledge Graph

## Contexto

Projeto de pesquisa e desenvolvimento sobre uso de agentes de IA na manutenção e evolução de sistemas legados, preservando arquitetura, padrões e regras de Engenharia de Software da organização. Princípio norteador: fornecer ao agente "o contexto certo, para a tarefa certa, no momento certo".

Arquitetura em duas camadas:

| Camada | Papel |
|---|---|
| SDLC Orchestrator | Agentes especializados por etapa do ciclo de desenvolvimento, gerando artefatos Markdown para agentes de código |
| SDLC Context Platform | Ingestão, embeddings, busca semântica, extração/governança de padrões, Knowledge Graph, exposição via MCP |

Meu grupo atua no Knowledge Graph: representação do código como grafo (nós = funções, arquivos, módulos, serviços; arestas = chamadas, dependências, relações semânticas), detecção de comunidades (Leiden) e enriquecimento com LLM.

Repositório: [CEIA-PDC2-ESIA/sdlc-context-platform](https://github.com/CEIA-PDC2-ESIA/sdlc-context-platform) (privado, TypeScript, branch `main`). Organização GitHub: CEIA-PDC2-ESIA. Não há repositório separado do Orchestrator visível na organização até o momento.

Base científica: um artigo aceito na ICSME e um segundo em avaliação (confidencial). Canais: Discord (dúvidas e estudos) e GitHub Projects/Kanban (tarefas). Reuniões semanais.

_A preencher: instituição/cliente, período, entregáveis formais._

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

- 18/09/2026 — Reunião semanal (não participei; conteúdo a recuperar com Karol).
- 22/09/2026 — Sem acesso ao GitHub Projects; comunicado à gestora Daniela.
- 22/09/2026 — Recebidos e fichados os dois papers do projeto em [leituras/](leituras/README.md); dúvidas sobre o grafo (Graphify, g(x,G), ausência de comunidades) registradas nos fichamentos.
- 11/09/2026 — [Onboarding da Frente 2](reunioes/2026-09-11-onboarding-frente-2.md): problema, arquitetura (Orchestrator + Context Platform), Knowledge Graph, governança de padrões; primeiro ciclo dedicado a estudo.
