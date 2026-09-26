# Pessoas — Noesis

Projeto de uma pessoa. A tabela registra atores no vocabulário do repositório e os repositórios que consomem ou são consumidos pelo Noesis.

## Atores

| Nome | Papel | Observações |
|---|---|---|
| Danillo | Operador — define épicos, homologa rigor científico, usa o produto na pesquisa | GitHub: `danilloguimaraes`, org `dgolabs` |
| Worker (S1–S4) | Pipeline de domain workers: Triagem, Evidência, Dialética, Curadoria | Event-sourced; cada S consome comandos e emite fatos |
| LLM Gateway | Abstração de provedores (Copilot, OpenRouter, Ollama futuro) | Cache de prompts; consentimento granular por estágio |
| Gatekeeper | Máquina de gates humanos entre estágios | Guided (manual), Delegated (autônomo), Deep (supervisionado) |
| Vault Adapter | Persistência no Obsidian via filesystem | Sync com o Operador; gera notas atômicas Zettelkasten |

## Repositórios relacionados

| Repositório | Relação | Observações |
|---|---|---|
| `dgolabs/noesis` | Este produto | Código-fonte e issues |
| `dgolabs/trantor` | Executor de issues | Trantor executa folhas do Noesis; incidente #91 ocorreu aqui |
| `dgolabs/terminus` | Infraestrutura | Aguarda imagem publicada no GHCR para homologação |
| vault Obsidian | Destino das notas | Sync manual com o Operador; estratégia de sync pendente (#87) |
| `pat-pesquisa` (skill) | Processo de leitura | Skill do my-skills que o Noesis automatiza |
