# Onboarding — Frente 2 (Knowledge Graph e Sistemas Legados)

**Data:** 11/09/2026
**Fonte:** relatório oficial da reunião (PDF `Relatorio_Reuniao_Onboarding_Frente_2-2.pdf`)
**Meu papel na frente:** Tech Lead com foco em pesquisa, alocado no grupo de construção do Knowledge Graph

## Contexto

Reunião inicial da Frente 2 do PDC 2. Objetivo: alinhar o problema de pesquisa antes de detalhar a ferramenta já implementada.

**Problema central:** usar agentes de IA na manutenção e evolução de sistemas legados sem perder contexto, padrões arquiteturais e regras de Engenharia de Software da organização. Sistemas reais estão distribuídos em múltiplos repositórios, microserviços, bancos, linguagens e contratos; despejar todo o código no agente não resolve (contexto insuficiente ignora dependências; contexto excessivo gera ruído e custo).

**Princípio norteador:** "Não queremos dar o máximo de contexto possível ao agente; queremos fornecer o contexto certo, para a tarefa certa, no momento certo."

## Arquitetura apresentada

| Camada | Responsabilidade |
|---|---|
| SDLC Orchestrator | Agentes especializados por etapa do ciclo (discovery, especificação, design, arquitetura, plano, implementação, testes, revisão). Geram artefatos Markdown consumidos por agentes de código (Codex, Claude Code etc.) |
| SDLC Context Platform | Ingestão de código/docs, indexação e embeddings, busca semântica, extração e governança de padrões, construção e consulta do Knowledge Graph, análise de aderência/violações, recuperação contextual, exposição via MCP |

## Knowledge Graph (meu grupo)

- **Nós:** funções/métodos, arquivos/classes, módulos/componentes, serviços e artefatos.
- **Arestas:** chamadas, dependências, relações de uso, relações semânticas inferidas.
- **Análise:** detecção de comunidades (Leiden) para identificar regiões funcionais; identificação de hubs.
- **Segunda camada:** enriquecimento com LLM (rótulos, descrições, relações semânticas não visíveis estaticamente).
- **Uso pelos agentes:** mapa do sistema consultado antes da alteração — componentes relacionados, quem chama, quem depende, áreas afetadas, arquivos a priorizar.
- **Aplicações futuras:** análise de impacto, seleção automática de contexto, estimativa de complexidade, redução de tokens.

## Extração e governança de padrões

- Determinístico primeiro (análise estática, parsing, bibliotecas) por ser mais barato e reproduzível; LLM só para padrões que exigem interpretação semântica.
- Ciclo de governança: identificado → aprovado / rejeitado / obrigatório.
- Objetivo de qualidade: a alteração gerada deve parecer feita pela própria equipe do sistema.

## Pesquisa científica

- Artigo 1: aceito na ICSME; posiciona o framework multiagente orientado por especificações para manutenção e evolução.
- Artigo 2: avaliação comparativa do framework; **em avaliação — não divulgar externamente**.

## Temas de estudo indicados

Knowledge Graphs (Leiden, enriquecimento semântico), sistemas legados (análise de impacto, modularidade), padrões de software (MVC, hexagonal, Factory, Repository), LLMs e contexto (RAG, embeddings, compactação), agentes de código, MCP, SDLC spec-driven, revisão de literatura.

## Organização

- Primeiro ciclo: onboarding, leitura, exploração dos repositórios, revisão de literatura, registro de dúvidas. Sem subfrentes ainda.
- Meta da primeira macroentrega: cada participante com uma contribuição pequena submetida e revisada em algum repositório.
- Comunicação no Discord (dúvidas e relatórios de estudo). Tarefas com responsável e prazo em GitHub Projects/Kanban.
- Reuniões semanais; possível intensificação no primeiro mês.

## Encaminhamentos

| Encaminhamento | Responsável | Observação |
|---|---|---|
| Compartilhar materiais de revisão de literatura | Coordenação | Início da próxima semana |
| Enquete sobre experiência com revisão de literatura | Participantes / coordenação | Via Discord |
| Liberar acesso de leitura aos repositórios | Responsáveis pelos repositórios | Para exploração |
| Manter dúvidas e relatos no Discord | Todos | |
| Estruturar tarefas com prazo | Coordenação | |
| Usar GitHub Projects/Kanban | Equipe | |
| Reuniões semanais no início | Equipe | Cadência reavaliada depois |
| Definir backlog da primeira macroentrega | Liderança técnica (inclui Danillo) | Foco inicial em entendimento |

## Propagação

- Ações → [PENDENCIAS.md](../PENDENCIAS.md)
- Decisões → [DECISOES.md](../DECISOES.md)
- Linha do tempo → [README.md](../README.md)
