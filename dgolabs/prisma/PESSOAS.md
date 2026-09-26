# Pessoas — Prisma

Projeto de uma pessoa. A tabela registra atores no vocabulário do repositório e os repositórios que interagem com o Prisma.

## Atores

| Nome | Papel | Observações |
|---|---|---|
| Danillo | Criador e Operador — define épicos, homologa gates, usa o produto na própria especialização | GitHub: `danilloguimaraes`, org `dgolabs` |
| Administrador | Eixo design-time: conduz S0–S10, configura trilha, audita gates | Persona do produto |
| Autodidata | Eixo run-time: executa a trilha, registra evidências e dúvidas | Persona do produto |
| Agente OpenCode | Executor de tasks via `/issue N` e `/epic N` | HITL: abre PR draft, aguarda merge humano |

## Repositórios relacionados

| Repositório | Relação | Observações |
|---|---|---|
| `dgolabs/prisma` | Este produto | Código-fonte, issues, Project V2 #11 |
| `dgolabs/trantor` | Não consome | Prisma é executado via agente OpenCode direto (não usa Trantor como executor) |
| `dgolabs/terminus` | Infraestrutura (futura) | Quando houver release, deploy via Terminus — ainda não aplicável |
