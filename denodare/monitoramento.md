# Planejamento

## Multi-tenant
workitem: https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/126

A implementação inicial proposta continha 7 fases: 
F0 — ADRs + POC + decisões §12
F1 — Módulo tenants/, select-tenant, RBAC tenant-aware e Tenant Admin API
F2 — tenant_id em 33–37 entidades, migrations e inventário SQL bruto
F3 — MinIO prefix, filtro no Elasticsearch, tenantId no chaincode, filas e crons
F4 — Frontend multi-tenant (TenantProvider, SelectTenantPage, interceptor, TenantSwitcher)
F5 — E2E zero-leak, whitelabel, load test e tracing
F6 — Cutover (tenant default em produção, dual-read off, runbook)

Já implementamos F0 e F1, contudo o Afonso fez algumas considerações em https://gitlab.com/daurora-fakenews/fakenews-bff/-/merge_requests/425#note_3971044842. 

Adicionalmente ele propos um SDD para abordarmos a evolução da issue. O sdd está versionado no seguinte commit (https://gitlab.com/daurora-fakenews/fakenews-bff/-/merge_requests/425/diffs?commit_id=e2b510ffd4337cf46d8f9165012f4e4078c4a48f).

Os próximos passos são: 
- Analisar o sdd 
- Analisar proposta de sdd

### Sobre a abordagem SDD. 

Segue relatório: 

### Relatório de Acompanhamento - Fase F1 (Isolamento Multi-Tenant - Issue #126)

---

#### **Planejamento Inicial**
- **Objetivo:** Implementar isolamento multi-tenant na plataforma dEnodare usando estratégia modularizada em fases (F1-F6), com critérios de aceite claros para evitar regressões.
- **Definições chave:**
  - Separação entre tenants de plataforma e tenants M2M.
  - Isolamento por `tenant_id` sem uso de Row-Level Security (RLS).
  - Revisão em escopo inicial de documentação (`feature-spec`, `plano-implementacao`) e código (`RBAC`, decorators `@TenantScoped`).

---

#### **Acompanhamento Atual**

##### **Concluído**
1. Revisão inicial e alinhamento de especificações/documentação (`README`, `feature-spec`, `plano-implementacao`).
2. Revisão parcial de código relacionado ao RBAC e a estratégias de tenant scoping.
3. Mapeamento inicial de lacunas e contradições entre estado do código (branch `poc/126-multitenant`) e a documentação.

##### **Em Progresso**
- **Validação do estado atual:**
  - Análise das saídas salvas específicas (ex. `/tmp/h2.txt`, `/tmp/n.txt`) e difs da branch vinculada à MR `!425`.
  - Mapeamento e confirmação de todas as entidades marcadas como `@TenantScoped`.
- **Consolidação de estratégia:**
  - Estrutura modularizada de F1 a F6 com base em critérios do `feature-spec` para planejamento das próximas fases e mitigação de riscos.

##### **Impedimentos**
1. Estado instável do código devido à falta de sincronismo em branches/documentação e inconsistências nas saídas de logs.
2. Divergências nas entidades `@TenantScoped`, dependência de inventário completo, e confirmação real de escopo.

---

#### **Próximas Frentes**
1. **Finalizar Fase F1:**
   - Conferir saídas completas dos testes/mapeamentos (`/tmp/*.txt`) e alinhar tenant scoping atual.
   - Revisar documentação e atualizar o acompanhamento do progresso em `docs/issue-126-acompanhamento.md`.

2. **Iniciar planejamento Fase F2-F6:**
   - Divisão clara em tarefas com priorização (retrofit, dual-read, cutover) e riscos organizados.
   - Alinhar estratégia e prioridades com stakeholders, garantindo que escopo seja restrito à plataforma.

3. **Correções Bloqueantes:**
   - Remover incongruências entre branch `poc/126-multitenant`, MR `!425` e documentação.
   - Investigar divergências nos testes (ex: `multitenant-*`) para validação completa do comportamento esperado.

---

Este acompanhamento reflete os avanços, bloqueios identificados e ações necessárias para garantir sucesso da entrega da F1 e continuidade segura da evolução no isolamento multi-tenant.

--- 

Para avaliar se estamos prontos para finalizar a Fase F1, precisamos garantir que os seguintes pontos estejam atendidos:

---

### **Checklist para Concluir a Fase F1**

1. **Revisão Completa do Estado Atual do Código:**
   - Verificar a implementação do isolamento por `tenant_id` em todas as entidades marcadas com `@TenantScoped`.
   - Garantir que as alterações relacionadas já estão presentes na branch `poc/126-multitenant` e revisadas.
   - Testar e revisar a integração com o RBAC e autenticação.

2. **Validação das Saídas Salvas (Logs e Testes):**
   - Confirmar se as saídas salvas em `/tmp/zk_full.txt`, `/tmp/h2.txt` e outros logs pendentes refletem o comportamento funcional esperado.
   - Executar novamente os testes que verificam o isolamento multi-tenant na solução proposta e revisar resultados.

3. **Conformidade com o Documento de Especificação (`feature-spec`)**
   - Garantir que os critérios de aceitação da Fase F1 definidos no documento foram atendidos, incluindo:
     - Implementação base de isolamento para tenants.
     - Isolamento em linha por `tenant_id` sem dependência de RLS.
     - Sem impacto regressivo no funcionamento atual da plataforma.

4. **Atualização na Documentação**
   - Consolidar o progresso da Fase F1 no SDD/`docs/issue-126-acompanhamento.md`.
   - Ajustar qualquer ponto relacionado ao planejamento e tarefas posteriores (F2–F6).

---

### **Identificados Pontos Pendentes**

Com base no estado atual:
1. **Conferência de Implementação Atual:**
   - Codificação do decorador `@TenantScoped` foi parcialmente revisada, mas deverá ser 100% mapeada nos testes e no código.
   - Falta validar a consistência com o que foi descrito no `feature-spec` e verificar se **todas as entidades** relevantes estão decoradas.

2. **Logs e Outputs:**
   - Está pendente certificar se as saídas salvas previamente foram conferidas para esclarecer discrepâncias no código. Isso inclui rodar novamente comandos necessários e validar os logs.

3. **MR !425:**
   - O estado da MR deve ser conferido: se já foi revisado e aprovado, podemos avançar. Caso contrário, será necessário documentar o que impede a aprovação.

---

### **Plano para Concluir a Fase F1**
Se os pontos acima forem os únicos pendentes, podemos seguir o seguinte plano:

1. **Revisar Implementação Atual:**
   - Mapear e revisar todas as entidades com `@TenantScoped` (Confirmar o funcionamento esperado).
   - Verificar o estado completo da branch `poc/126-multitenant` e executar testes existentes.

2. **Conferir Saídas dos Testes:**
   - Reler ou reexecutar os comandos cujas saídas foram salvas em `/tmp/*.txt` para verificar estabilidade e conformidade com o esperado.

3. **Validar MR!:**
   - Confirmar status da MR `!425`, analisando comentários e ajustes necessários. Atualizar o conteúdo, caso necessário.

4. **Realizar Ajustes e Atualizar Documentação:**
   - Ajustar funcionalidades faltantes/melhorias.
   - Atualizar detalhes da Fase F1 no arquivo de acompanhamento.

---

Se concordar com os ajustes e validações pendentes, posso começar a execução imediata para tentar fechar a F1 com base nesses passos. Como podemos proceder?
