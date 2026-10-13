# My Desk — Documento de Visão

Criado em 13/10/2026. Este documento é o contrato do sistema: o contexto, as necessidades do usuário em ordem de valor e as restrições que delimitam qualquer solução. Toda mudança no my-desk é avaliada contra ele com uma pergunta: qual necessidade isso contempla, e com que sinal?

**Natureza deste documento**: definição do projeto, não operação. Ele não participa do fluxo diário de registro (reuniões, pendências, decisões) e não é atualizado por ele; muda apenas por decisão deliberada do usuário, quando as necessidades, as restrições ou o escopo mudam.

## Contexto

O my-desk é um sistema pessoal de **gestão, não de operação**. Sua função é ser o guia que o usuário consulta **antes** de entrar nos detalhes de cada frente: onde cada uma está, o que pede atenção, o que vem a seguir. A execução do trabalho vive nos repositórios das frentes, não aqui.

O usuário é uma pessoa só, com ~12 frentes simultâneas em papéis distintos (gestor, tech lead, dev, pesquisador, operador). O trabalho em cada frente é mediado por agentes LLM, o que faz do agente um **segundo consumidor** do sistema: sessões de trabalho começam com o agente lendo o estado do desk.

## Necessidades do usuário (ordem de valor)

As três primeiras são **primárias** — o sistema existe por elas. As demais são **amplificadoras**: multiplicam o valor das primárias, mas nenhuma, sozinha, sustenta o produto.

| # | Necessidade (voz do usuário) | O que o usuário ganha | Sinal de atendimento |
|---|---|---|---|
| 1 | "Em dois minutos, quero saber onde cada frente está e o que pede minha atenção hoje." | Orientação antes dos detalhes | Abrir um único lugar e sair sabendo a próxima ação de cada frente, sem abrir nenhum projeto |
| 2 | "Quero poder acreditar no que vejo sem precisar conferir." | Confiança que torna a necessidade 1 habitável | O usuário nunca descobre, por acidente, que o quadro estava desatualizado ou mentia |
| 3 | "Nada que foi combinado se perde: ação, decisão ou urgência fica visível até ser resolvida ou descartada por mim." | Zero compromissos evaporando em silêncio | Nenhuma surpresa do tipo "isso já estava decidido/pendente há semanas" |
| 4 | "Quero retomar uma frente depois de semanas e estar dentro do contexto em minutos — eu ou o agente que me auxilia." | Hiato entre sessões deixa de custar arqueologia | A primeira sessão após um hiato não começa reconstituindo o passado |
| 5 | "Escrevo uma vez; o sistema distribui para todos os lugares onde isso precisa aparecer." | Registrar não é um segundo trabalho | Após registrar uma reunião, nenhum espelho, índice ou painel exige edição manual |
| 6 | "Quero saber por que cada decisão foi tomada, não só qual foi." | Decisões não são re-litigadas por falta de memória da razão | O usuário nunca reabre uma decisão fechada por ter esquecido seus motivos |
| 7 | "Quero um lugar para preparar a comunicação pendente das minhas frentes." | Mensagens difíceis saem da cabeça para o papel | Nenhuma conversa delicada fica sem rascunho |

Lógica da ordenação: 1 é a promessa do produto; 2 impede que 1 vire decoração; 3 é a falha silenciosa que corrói 2 por dentro (compromisso que some é mentira por omissão).

## Restrições não-funcionais

- **Manutenção desprezível**: no dia em que o my-desk virar a décima terceira frente de trabalho, ele falhou no propósito.
- **Legível por humano e por LLM**, versionado, sem infraestrutura a operar.

## O que o sistema não contempla

- Execução operacional das frentes (vive nos repositórios delas).
- Gerência de prazos com alertas (isso seria um gerente de projetos, não um guia).
- Compartilhamento (sistema de um único usuário).
