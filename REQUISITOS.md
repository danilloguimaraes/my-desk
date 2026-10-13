# My Desk — Requisitos

Criado em 13/10/2026. Requisitos do sistema, derivados das necessidades de [VISAO.md](VISAO.md), uma seção por necessidade. Cada requisito é numerado, livre de solução e acompanhado de critério de aceitação verificável contra o sinal de atendimento da visão.

**Natureza deste documento**: definição do projeto, não operação. Soluções (como implementar) não moram aqui; são escolhidas depois e registradas como decisões do projeto. IDs de requisitos são `RF-N<x>.<n>`, estáveis, e não são reutilizados se removidos.

## Necessidade 1 — Orientação antes dos detalhes

> "Em dois minutos, quero saber onde cada frente está e o que pede minha atenção hoje."
>
> Sinal de atendimento (visão): abrir um único lugar e sair sabendo a próxima ação de cada frente, sem abrir nenhum projeto.

### Cenários de uso (base da derivação)

- **C1 — Planejamento do dia**: início da sessão de trabalho; decidir para onde a atenção vai, olhando todas as frentes de uma vez.
- **C2 — Preparação para uma frente**: daqui a pouco vou trabalhar na frente X (ou tenho reunião dela); quero chegar situado, sem abrir o projeto.
- **C3 — Checagem de atenção**: janela curta livre; saber o que está urgente em qualquer frente para escolher um item e atacar.

### Requisitos funcionais

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RF-N1.1 | Apresentar, em um único lugar, todas as frentes ativas com o estado atual resumido de cada uma | Em uma única abertura, vejo todas as frentes com estado; a contagem bate com a realidade — sem frente faltando, sem frente fantasma |
| RF-N1.2 | Apresentar, para cada frente ativa, a próxima ação crítica | Nenhuma frente ativa aparece sem próxima ação identificada |
| RF-N1.3 | Apresentar, no mesmo lugar, a lista consolidada de pendências urgentes de todas as frentes, cada uma identificada com sua frente | Toda urgência aponta a qual frente pertence; nenhuma urgência de frente fica de fora |
| RF-N1.4 | Permitir a consulta de RF-N1.1 a RF-N1.3 sem navegar por pastas nem abrir arquivos das frentes | A consulta inteira usa um único ponto de consulta (documento ou comando) |
| RF-N1.5 | Manter a visão consolidada legível em aproximadamente dois minutos | A seção consolidada tem no máximo ~40 linhas |

Rastreabilidade: C1 ← RF-N1.1, RF-N1.2, RF-N1.4, RF-N1.5 · C2 ← RF-N1.2, RF-N1.4 · C3 ← RF-N1.3, RF-N1.4.

**Fora do escopo desta seção** (por pertencer a outra necessidade): garantir que o conteúdo apresentado esteja atualizado e sem itens obsoletos — isso serve à necessidade 2 (confiança), não à 1. Necessidade 1 é sobre o quadro existir e ser consultável; sua fidelidade é cobrada em N2.

### Soluções adotadas

_(a preencher quando houver; as alternativas consideradas viram decisões do projeto)_

## Próximas seções

As seções das necessidades 2–7 serão criadas na mesma estrutura (cenários → requisitos → critérios), conforme o projeto avançar.
