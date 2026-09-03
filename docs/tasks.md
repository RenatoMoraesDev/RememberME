# Quadro de tarefas

Item 6 do entregável da Etapa 2. Atualizado a cada tarefa concluída — o estado numa
data passada recupera-se pela etiqueta Git da entrega correspondente.

**Estados:** `pendente` · `em-desenvolvimento` · `pronto`

## Calendário

As aulas de setembro são a **2, 4, 7, 9, 14, 22, 24, 28 e 30**. O grupo trabalha
fora desse horário, mas **entregas e pontos de integração caem sempre num dia de
aula**, para que haja o grupo todo e o formador presentes quando algo é dado por
fechado. As datas abaixo respeitam essa regra.

Há duas descontinuidades a ter em conta: de 9 para 14 e, sobretudo, de **14 para
22 — oito dias sem aula**. Esse intervalo é o maior bloco de trabalho contínuo do
mês e está atribuído à Fase 2 (MVP), que é a fase mais pesada. As datas de outubro
ainda não são conhecidas; a Fase 3 fecha dentro de setembro para não depender delas.

## Etapa 2 — Arquitetura, Tecnologias e Planeamento

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| Organização inicial do repositório | Renato | pronto | 02/09/2026 | — |
| Reorganizar a documentação por etapa | Renato | em-desenvolvimento | 03/09/2026 | — |
| Plano de desenvolvimento (item 7) | Renato | em-desenvolvimento | 03/09/2026 | — |
| Nomenclatura de branches no README | Renato | pendente | 03/09/2026 | — |
| Renomear a branch `felipe/feature` | Felipe | pendente | 03/09/2026 | convenção definida |
| Criar o milestone M1 no GitHub | Renato | pendente | 03/09/2026 | plano |
| Fechar a escolha do motor de agendamento | Renato | pronto | 04/09/2026 | comparação técnica |
| Entrega da Etapa 2 | Todos | pendente | 04/09/2026 | itens acima |

## Fase 0 — Capacitação

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| Estudo do `plyer` + entregar `notificar(titulo, mensagem)` | Niley | em-desenvolvimento | 07/09/2026 | contrato da função |
| Estudo do `pystray`: ícone com menu "Sair" | Renato | em-desenvolvimento | 07/09/2026 | — |
| Estudo do `Typer`: comando que escreve na base de dados | Felipe | em-desenvolvimento | 07/09/2026 | — |
| Comparação `schedule` vs APScheduler com janela de horário | Renato | pronto | 04/09/2026 | — |
| Reunião: validar a escolha do agendador | Todos | pendente | 04/09/2026 | comparação e spikes |
| Plano de comandos do CLI (casos de uso) | Renato | em-desenvolvimento | 07/09/2026 | — |
| Validar o plano de comandos com o grupo | Todos | pendente | 09/09/2026 | plano de comandos |

## Fase 1 — Fundação e esqueleto

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| Criar `.gitignore` | Renato | pendente | 07/09/2026 | — |
| Criar `pyproject.toml` e fixar versões com `uv lock` | Renato | pendente | 07/09/2026 | escolha do agendador |
| Renomear `src/remember/` para `src/rememberme/` | Renato | pendente | 07/09/2026 | — |
| Cada elemento instala o `uv`, corre `uv sync` e valida | Todos | pendente | 07/09/2026 | `pyproject.toml` |
| Definir `models.py` | Renato | pendente | 08/09/2026 | — |
| Validar `models.py` com o grupo e congelar | Todos | pendente | 09/09/2026 | `models.py` |
| Esqueleto: sete módulos com assinaturas e docstrings | Renato | pendente | 09/09/2026 | `models.py` |
| Ligar bandeja + agendador + notificação a correr | Renato | pendente | 09/09/2026 | esqueleto |
| Ponto de integração 1 em `develop` | Todos | pendente | 09/09/2026 | tudo o acima |

## Fase 2 — MVP

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| `storage.py`: schema, CRUD e tabela `estado` (RF04) | Renato | pendente | 14/09/2026 | Fase 1 |
| `storage.py`: lembretes pré-carregados (RF05) | Renato | pendente | 14/09/2026 | CRUD |
| `scheduler.py`: hora fixa (RF01) | Renato | pendente | 14/09/2026 | Fase 1 |
| `scheduler.py`: recorrência com janela (RF02) | Renato | pendente | 22/09/2026 | RF01 |
| `tray.py`: menu e lembretes ativos (RF03) | Renato | pendente | 22/09/2026 | Fase 1 |
| `cli.py`: comandos do MVP (RF06) | Felipe | pendente | 22/09/2026 | `storage.py`, plano de comandos |
| `cli.py`: `start` e `stop` | Renato | pendente | 22/09/2026 | `app.py` |
| `notifications.py`: afinação da notificação em Windows | Niley | pendente | 22/09/2026 | Fase 1 |
| Ponto de integração 2 em `develop` — MVP fechado | Todos | pendente | 22/09/2026 | todos os módulos |

## Fase 3 — Validação e incrementais

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| Testes de `storage.py` e `scheduler.py` | Renato | pendente | 24/09/2026 | MVP estável |
| Testes de `cli.py` | Felipe | pendente | 24/09/2026 | MVP estável |
| Testes de `notifications.py` | Niley | pendente | 24/09/2026 | MVP estável |
| Empacotamento com PyInstaller | Felipe | pendente | 24/09/2026 | MVP estável |
| RF07: som, pop-up, abrir aplicação/URL | Niley | pendente | 28/09/2026 | MVP estável |
| RF08: arranque com o sistema operativo | Felipe | pendente | 28/09/2026 | MVP estável |

## Documentação e apresentação

| Descrição | Responsável | Estado | Data prevista | Dependências |
|---|---|---|---|---|
| Registo de decisões técnicas (`decisoes.md`) | Niley | pendente | contínuo | — |
| README de utilização | Felipe | pendente | 28/09/2026 | MVP estável |
| Guião da demonstração | Felipe | pendente | 30/09/2026 | executável |
| Documentação das etapas | Renato | contínuo | por etapa | — |
