# Decisões — my-skills

## 25/09/2026 — Criar skill `desk-sync` como ponte stateless entre projetos e my-desk

**Contexto.** Trabalhar em múltiplas frentes exige trânsito manual entre o repo do projeto e o my-desk para (a) retomar o estado e (b) registrar o que aconteceu. Fricção alta, especialmente no fechamento de sessão. Descartada a alternativa de instalar arquivos por projeto (invasiva ao `.gitignore` de cada repo).

**Decisão.** Skill global `desk-sync` que:
- É stateless — usuário nomeia o projeto explicitamente na invocação (`atualiza desk do projeto X`), sem `desk-map.json` nem inferência por git remote.
- Mora em `skill/desk-sync/SKILL.md` (versionada neste repo, carregada globalmente pelo opencode).
- Fecha sessão: lê git log do cwd, pergunta o que ficou fora de commit, propõe diff no my-desk seguindo o `AGENTS.md` do desk, mostra `git diff`, **não commita**.
- Abre sessão: entrega briefing curto (status, próxima ação, urgentes, timeline recente) só leitura.
- `DESK_ROOT` hardcoded no topo da skill.

**Consequências.**
- Zero mudança nos repos de trabalho.
- Usuário mantém controle editorial (aprova o diff, escreve o commit).
- Skill imune a monorepos e worktrees porque não infere projeto.
- Fica dependente do usuário lembrar o nome exato da pasta no desk — aceitável, o custo é baixo.
- `DESK_ROOT` hardcoded exige edição manual se o my-desk mudar de path/máquina.
