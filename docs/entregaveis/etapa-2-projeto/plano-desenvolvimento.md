# RememberME — Plano de Desenvolvimento (rascunho para a Etapa 2)

> **Rascunho de trabalho.** Destina-se a ser reescrito pelo Renato antes de entrar em `docs/` do repositório do projeto.

---

## 1. Âmbito

O entregável da Etapa 2 lista sete itens. Quatro já estão cobertos no repositório:

| # | Item | Situação |
|---|---|---|
| 1 | Tecnologias escolhidas | Coberto — `docs/stack.md` |
| 2 | Justificação das tecnologias | Coberto — o enunciado pede "explicar de forma resumida o motivo de cada escolha", e o `stack.md` dá um motivo por tecnologia |
| 3 | Arquitetura da solução | Coberto — `01-arquitetura.d2` e `02-responsabilidades.d2` |
| 4 | Estrutura prevista do projeto | Secção 2 |
| 5 | Distribuição de responsabilidades | Secção 4 |
| 6 | Lista de tarefas | Secção 8 |
| 7 | Plano de desenvolvimento | Secções 7 e 9 |

**Nota sobre os itens 6 e 7.** O enunciado separa-os no entregável mas só descreve um deles ("Planeamento do trabalho"). A leitura adotada:

- **Item 6 — lista de tarefas:** *o quê* e *quem*. É o `docs/tasks.md`, com os cinco campos exigidos.
- **Item 7 — plano de desenvolvimento:** *em que ordem*, *o que bloqueia o quê*, *até onde*. É a sequência de fases, os milestones e o alinhamento com as etapas 3 a 5 do curso.

---

## 2. Estrutura prevista do projeto

O layout `src/` já adotado é o padrão da comunidade Python: impede que o interpretador importe o pacote a partir da raiz do repositório por acidente — erro que faz o programa funcionar na máquina de quem o escreveu e falhar depois de empacotado.

```
RememberME/
├── .gitignore              venv, __pycache__, dist/, build/, *.db
├── pyproject.toml          metadados + dependências mínimas
├── uv.lock                 versões exatas — vai para o repositório
├── README.md, LICENSE, logo.png
│
├── docs/
│   ├── tasks.md            quadro de tarefas (documento vivo)
│   ├── decisoes.md         registo de decisões (documento vivo)
│   └── entregaveis/        material de avaliação, uma pasta por etapa
│
├── src/rememberme/
│   ├── __init__.py         marca a pasta como pacote Python
│   ├── __main__.py         o que o `python -m rememberme` executa
│   ├── cli.py              comandos Typer                    Felipe
│   ├── app.py              liga as peças umas às outras       Renato
│   ├── models.py           dataclass Reminder — o contrato    Renato
│   ├── storage.py          SQLite                             Renato
│   ├── scheduler.py        APScheduler                        Renato
│   ├── notifications.py    plyer                              Niley
│   └── tray.py             ícone de bandeja + menu             Renato
│
└── tests/                  insumo da Etapa 4
```

Sete módulos, sem subpastas. Uma pasta `core/` a agrupar seis ficheiros não
organiza nada que a lista acima já não mostre, e custa imports mais longos a
quem está a aprender a linguagem.

### 2.1 Divisão em camadas

O enunciado pede a divisão entre frontend, backend e dados. Numa aplicação desktop sem servidor, lê-se assim:

| Camada | Módulos |
|---|---|
| Interface | `cli.py`, `tray.py`, e a GUI PySide6 se o RF10 avançar |
| Lógica | `scheduler.py`, `notifications.py`, `app.py` |
| Dados | `storage.py`, `models.py` |

### 2.2 Ficheiros de configuração

- **`pyproject.toml`** — declara as dependências e a versão mínima de cada uma.
- **`uv.lock`** — regista a versão **exata** de todas elas, incluindo as que vieram por arrasto, e vai para o repositório. É o que garante que os três correm rigorosamente o mesmo: `uv sync` reproduz o ambiente a partir daqui.
- **`.gitignore`** — sem ele, a primeira `venv` ou `__pycache__` que alguém commitar gera conflito em todas as branches em aberto. É o primeiro ficheiro a criar, antes de qualquer código.
- **Base de dados** — não vai para o repositório. Fica na pasta de dados do utilizador, resolvida por `typer.get_app_dir("RememberME")`, que devolve o caminho correto em Windows, macOS e Linux sem código condicional.

---

## 3. Modelo de dados

Um único registo, `lembrete`, sustenta o RF01 e o RF02:

| Campo | Tipo | Notas |
|---|---|---|
| `id` | INTEGER PK | |
| `texto` | TEXT | o que a notificação diz |
| `hora` | TEXT | `HH:MM` — **se estiver preenchido, é um lembrete de hora fixa** (RF01) |
| `janela_inicio` | TEXT | `HH:MM` (RF02) |
| `janela_fim` | TEXT | `HH:MM` (RF02) |
| `intervalo_min` | INTEGER | minutos entre disparos, dentro da janela (RF02) |
| `dias_semana` | TEXT | ex.: `seg,qua,sex` |
| `ativo` | INTEGER | 0/1 |

**Não há campo `tipo`.** Um lembrete é de hora fixa se `hora` estiver preenchida,
e recorrente caso contrário. Guardar o tipo *e* os campos que o determinam cria
duas fontes para a mesma verdade, que mais cedo ou mais tarde discordam.

**O que ficou deliberadamente de fora**, para o MVP não carregar peso que ainda
não precisa:

| Fora | Porquê |
|---|---|
| `accao`, `accao_param` | São o RF07, que é incremental. Acrescentar duas colunas quando o RF07 avançar custa um `ALTER TABLE`; carregá-las agora custa dois campos que ninguém sabe explicar na defesa. |
| `ultima_execucao` | Existia para decidir se um lembrete das 08:30 devia disparar quando a aplicação abre às 09:00. Essa política é dos problemas mais difíceis de agendamento, e o requisito não a pede: o programa notifica enquanto está aberto. |
| `titulo` separado de `mensagem` | O título é sempre `RememberME`. Um campo, não dois. |

Este é o **único ponto onde os três colidem**. Tem de estar definido, integrado e congelado antes de qualquer módulo começar.

### 3.1 Tabela `estado`

Uma segunda tabela, de duas colunas, guarda estado da aplicação que não pertence a
nenhum lembrete:

| Campo | Tipo | Notas |
|---|---|---|
| `chave` | TEXT PK | ex.: `paragem_pedida` |
| `valor` | TEXT | |

Serve hoje o pedido de paragem do `rememberme stop` (§ 5.4) e serve, sem alterações,
qualquer valor solto que venha a ser preciso guardar. Duas colunas evitam ter de
acrescentar uma tabela nova de cada vez que aparece uma definição.

---

## 4. Distribuição de responsabilidades

### 4.1 Critério

Duas restrições moldam a divisão:

1. **Evitar conflito de merge.** Se dois elementos partilham "backend", editam os mesmos ficheiros e cada integração vira conflito. Cada pessoa tem de ser dona de ficheiros distintos — o que também preserva o histórico Git individual, que o enunciado avalia como evidência de participação.
2. **Níveis de experiência diferentes.** O Renato coordena por ter mais experiência prévia; o Felipe e a Niley estão a começar. Uma divisão que exija dos três o mesmo tipo de decisão de desenho bloqueia dois deles.

A resposta às duas: **o Renato entrega o esqueleto com as assinaturas de função já definidas e a chamarem-se umas às outras, com corpos vazios.** O Felipe e a Niley preenchem corpos de função com contrato fixo, em vez de desenharem módulos do zero.

### 4.2 Atribuição

| Elemento | Ficheiros | Natureza do trabalho |
|---|---|---|
| **Renato** | `models.py`, `storage.py`, `scheduler.py`, `app.py`, `tray.py` | Contrato de dados, persistência, motor de agendamento, composição, bandeja. Mais coordenação, integração e documentação. |
| **Felipe** | `cli.py` | Preencher os comandos Typer (`add`, `list`, `edit`, `remove`, `on`, `off`), cada um a chamar uma função de `storage.py` que já existe. Trabalho linear, com muitos commits pequenos. |
| **Niley** | `notifications.py` | Preencher `notificar(mensagem)` — uma função, um contrato, sem decisões de arquitetura. Depois, se o RF07 avançar, as ações. |

### 4.3 Porque o `tray.py` fica com quem faz a integração

A bandeja é onde o modelo de threads da secção 5.3 se resolve: o `pystray` exige a
thread principal em macOS e bloqueia-a até o utilizador sair. Esse constrangimento
atravessa o `app.py` e o `scheduler.py`, que competem pelo mesmo fluxo.

O critério é concentrar o risco de threads num ponto só, junto de quem faz a
integração — o mesmo argumento que atribui o `app.py` e o `scheduler.py`. Dividir
esses três módulos por pessoas diferentes obrigava a coordenar, entre branches, a
decisão mais delicada do projeto.

O `cli.py` é, em contrapartida, o módulo com maior volume de trabalho visível: quatro
comandos independentes, cada um a chamar uma função que já existe.

### 4.4 Trabalho partilhado

| Item | Responsável |
|---|---|
| `.gitignore`, `pyproject.toml` | Renato, uma vez, antes de tudo |
| `models.py` | Renato escreve, **os três validam** antes de qualquer módulo começar |
| Testes | Cada um escreve os testes do seu módulo |
| Empacotamento PyInstaller | Felipe |
| Documentação das etapas | Renato, com contributo dos três |
| README de utilização e guião da demonstração | Felipe |
| Registo de decisões (`decisoes.md`) | Niley |

Os papéis podem alternar entre etapas, como o enunciado incentiva.

### 4.5 Equilíbrio da divisão

O enunciado avalia o **equilíbrio na divisão do trabalho** e trata o histórico do
repositório como evidência de participação individual. A concentração de módulos no
coordenador, justificada acima por razões técnicas, tem de ser compensada de forma
visível — caso contrário o histórico regista um projeto de uma pessoa.

Compensação, registada no `tasks.md` como tarefas com responsável:

- Testes: cada elemento escreve os do seu módulo.
- README de utilização, guião da demonstração e empacotamento: Felipe.
- Registo de decisões técnicas: Niley.

---

## 5. Decisões técnicas

### 5.1 Motor de agendamento — APScheduler

Decidido a 04/09/2026 com base num spike com código a correr, não em leitura de
documentação. O registo completo está em [`../../decisoes.md`](../../decisoes.md) (D3).

| Critério | `schedule` | **APScheduler** |
|---|---|---|
| Curva de aprendizagem | Muito baixa — `every(10).minutes.do(...)` | Média — exige perceber schedulers, jobs e triggers |
| RF01, hora fixa | `every().day.at("08:30")` | `CronTrigger(hour=8, minute=30)` |
| **RF02, janela 8h–14h** | Não suportado — exige um `if` dentro da tarefa a ignorar disparos fora da janela | `CronTrigger(hour="8-13", minute=0)` — a janela é o gatilho |
| **Ancoragem dos disparos** | **No arranque do programa** | **No relógio** |
| Dias da semana | Um método por dia; não aceita lista | `day_of_week="mon,tue,wed"` |
| Execução em segundo plano | Thread manual com `while True: run_pending(); sleep(1)` | `BackgroundScheduler()` gere a própria thread |
| Persistência de jobs | Não tem | Jobstores, inclusive SQLite |
| Dependências | Nenhuma | `tzlocal` |

**O que decidiu foi a ancoragem.** O `schedule` conta o intervalo a partir do momento
em que o programa arranca — um lembrete de hora a hora dispara em horários diferentes
a cada reinício. O APScheduler dispara sempre às horas certas, independentemente do
arranque. Para lembretes ligados ao horário da aula, isso é um defeito funcional, não
uma preferência de estilo.

O custo — mais uma dependência e mais conceitos a aprender — fica contido porque
`scheduler.py` expõe interface própria (`agendar(reminder)`, `remover(id)`,
`iniciar()`, `parar()`) e é o único ficheiro que conhece a biblioteca.

**Cuidado a fixar no `models.py`:** `hour="8-14"` inclui as 14h. É preciso decidir e
escrever se `janela_fim` é inclusivo ou exclusivo.

### 5.2 Notificações

O `plyer` mantém-se, e `notifications.py` expõe **uma função só**:
`notificar(mensagem)`.

Uma função em vez de chamadas ao `plyer` espalhadas pelo código dá o que
interessa: se o `plyer` se portar mal em Windows — recorre ao balão clássico,
que não permite ações nem fica no centro de notificações — troca-se o corpo
daquela função, num ficheiro, e mais nada muda. É a mesma proteção que uma
camada de abstração daria, sem a camada.

### 5.3 Thread principal

Três componentes querem controlar o fluxo: o `pystray` (que em macOS exige a thread principal), o motor de agendamento e o Typer.

```
Thread principal          →  pystray.Icon.run()   bloqueia até o utilizador sair
Thread secundária         →  scheduler em segundo plano
Processo de curta duração →  comandos Typer: escrevem no SQLite e terminam
```

O comando `rememberme start` arranca o modo residente, com bandeja e agendador. Os restantes comandos apenas alteram a base de dados e saem. Evita ter de sincronizar dois processos e mantém cada módulo testável em separado.

Validar este modelo é o objetivo da Fase 1.

### 5.4 Como o programa encerra

Os estados por que o processo passa estão em
[`03-ciclo-de-vida.d2`](03-ciclo-de-vida.d2).

O `rememberme start` deixa um processo a correr na bandeja. Para o parar de fora
existe o `rememberme stop` — um comando `start` sem `stop` é uma assimetria que
ninguém consegue explicar a quem usa o programa.

Os dois comandos são processos diferentes e não falam um com o outro
diretamente. Falam pela base de dados, na tabela `estado` (§ 3.1): o `stop`
escreve `paragem_pedida`, e o processo residente lê essa chave de cinco em cinco
segundos, num trabalho do próprio agendador, e desliga-se por sua iniciativa —
agendador primeiro, ícone depois.

A base de dados é o sítio certo porque o processo residente já lá vai de
qualquer forma, para apanhar lembretes criados enquanto corre. É o mesmo
caminho, e fica um só canal entre os comandos e o processo.

**Nunca se mata o processo.** Em Windows, terminá-lo à força deixa o ícone na
bandeja até alguém lhe passar o rato por cima: o programa morreu e continua a
parecer vivo.

O item "Sair" do menu da bandeja (RF03) e o `rememberme stop` são dois caminhos
para a mesma função `encerrar()`, em `app.py`. Duas saídas com código próprio é
como uma delas se esquece de limpar a tabela.

**O que não fazemos: impedir duas instâncias.** Chegou a estar planeado um
módulo que pedia ao sistema operativo um bloqueio exclusivo sobre um ficheiro,
com código diferente para Windows e Unix. Foi retirado: nenhum requisito o pede,
era a única parte do projeto com código dependente do sistema operativo, e só se
testa a matar processos. Se alguém correr `start` duas vezes ficam dois ícones —
inconveniente, não defeito. Resolve-se se algum dia incomodar.

---

## 6. Organização do trabalho no Git

### 6.1 Branches permanentes

| Branch | Papel |
|---|---|
| `master` | Só código estável e avaliável. Recebe merge de `develop` em reunião de grupo, no fecho de cada etapa. |
| `develop` | Onde o trabalho dos três se junta, nos pontos de integração agendados. |

### 6.2 Nomenclatura

```
<tipo>/<nome>-<descricao-curta>
```

| Tipo | Uso | Exemplo |
|---|---|---|
| `feat/` | Nova funcionalidade | `feat/niley-notificacoes` |
| `fix/` | Correção | `fix/felipe-cli-comando-remove` |
| `docs/` | Só documentação | `docs/renato-plano-etapa2` |
| `test/` | Só testes | `test/renato-storage` |
| `chore/` | Configuração, dependências | `chore/renato-gitignore` |
| `spike/` | Experiência descartável (Fase 0) | `spike/felipe-typer` |

A branch existente `felipe/feature` fica fora desta convenção e deve ser renomeada na próxima integração.

### 6.3 Pontos de integração

Não há integração automática nem pipeline de CI. As integrações em `develop` acontecem em **momentos agendados, um por fase, com os três presentes**.

Consequência a assumir: entre integrações, as branches divergem por mais tempo e `develop` não é uma referência atualizada. Com três pessoas em ficheiros distintos o risco é baixo — **exceto no `models.py`**, que por isso tem de estar em `develop` e congelado antes de a Fase 2 começar.

### 6.4 Fluxo

1. Atualizar `develop` antes de criar a branch.
2. Criar a branch segundo a convenção.
3. Commits pequenos e frequentes. O enunciado avalia o histórico como evidência de participação individual — um único commit grande no fim penaliza.
4. Merge direto em `develop`, no ponto de integração agendado (§ 6.3) — sem Pull Request, porque a divisão por ficheiro (§ 4.2) já evita o conflito que a revisão formal existiria para prevenir.
5. `develop` → `master` só por Pull Request, em reunião de grupo, no fecho de cada etapa.

### 6.5 Mensagens de commit

```
<tipo>: <descrição no imperativo>
```

Exemplos: `feat: adicionar CRUD de lembretes no storage`, `docs: plano de desenvolvimento da Etapa 2`, `fix: corrigir caminho da base de dados em Windows`.

---

## 7. Fases

### Fase 0 — Capacitação

**Porquê:** nenhum elemento do grupo conhece as bibliotecas escolhidas. O estudo não é preâmbulo do plano, é o caminho crítico dele.

Cada estudo termina num **spike**: um script curto, numa branch `spike/<nome>-<lib>`, que faz a biblioteca fazer uma coisa só.

Cada um estuda a biblioteca do módulo de que fica responsável (§ 4.2). Um spike serve
para quem vai escrever o código, não para quem vai ler o relatório.

| Quem | Spike | Módulo que vai escrever | O que fica a saber |
|---|---|---|---|
| Niley | `plyer` mostra uma notificação em Windows | `notifications.py` | Se a notificação nativa serve como está (risco R4) |
| Felipe | `Typer` corre um comando com opções e escreve na base de dados | `cli.py` | Como o Typer valida opções e devolve erros ao utilizador |
| Renato | `pystray` põe um ícone com menu "Sair" | `tray.py` | Como se comporta o bloqueio da thread principal (risco R3) |
| Renato | `schedule` **e** `APScheduler` numa janela de horário | `scheduler.py` | Fecha a decisão de 5.1 com dados, não com leitura |

O Renato leva dois spikes por lhe caberem os dois módulos onde os riscos técnicos se
concentram — a bandeja e o agendador. O desequilíbrio de horas daí resultante está
compensado na § 4.5.

Três ganhos: a decisão do agendador deixa de ser teórica; os riscos R3 e R4 aparecem na primeira semana em vez de na integração final; e os três têm commits reais desde o primeiro dia.

O código dos spikes é descartável, com **uma exceção deliberada**: o da Niley nasce
já com o contrato final, `notificar(mensagem)`, e passa a ser o `notifications.py`.
A razão é o critério de conclusão da Fase 1 — o esqueleto tem de disparar uma
notificação real. A alternativa era o coordenador escrever uma versão provisória
para a Niley reescrever depois, ou descer o milestone a um `print` no terminal —
adiando para a Fase 2 exatamente o risco (R3) que a Fase 1 existe para eliminar cedo.

> **Concluída quando:** os três spikes correm, e a decisão do agendador está registada em `docs/decisoes.md` — **feita a 04/09/2026, D3**.

### Fase 1 — Fundação e esqueleto

**Responsável:** Renato. **Depende de:** Fase 0. **Bloqueia:** tudo o resto.

- `.gitignore`, `pyproject.toml` e `uv.lock` com as versões fixadas
- `docs/decisoes.md` e `docs/tasks.md` atualizados
- Convenção de branches documentada no `README.md`
- Renomear a branch `felipe/feature`
- `models.py` — escrito pelo Renato, **validado pelos três**
- Os sete módulos criados, com assinaturas e docstrings, sem corpos
- `app.py` a arrancar bandeja e agendador com um lembrete fixo no código
- Integração do `notifications.py` entregue pela Niley na Fase 0

> **Concluída quando:** `rememberme start` mostra o ícone na bandeja e dispara uma notificação real; e os três executam `uv sync` sem erro na sua máquina.
>
> **Porquê antes de dividir:** se o modelo de threads da secção 5.3 estiver errado, é muito melhor descobri-lo agora do que com três módulos já escritos por cima.

### Fase 2 — MVP

**Depende de:** Fase 1, com o `models.py` congelado em `develop`.

| Trabalho | Quem | Requisitos |
|---|---|---|
| `storage.py` — schema, CRUD, lembretes pré-carregados | Renato | RF04, RF05 |
| `scheduler.py` — hora fixa e recorrência com janela | Renato | RF01, RF02 |
| `tray.py` — menu completo, ver lembretes ativos | Renato | RF03 |
| `cli.py` — `add`, `list`, `remove`, `run` | Felipe | RF06 |
| `notifications.py` — backend alternativo e afinação | Niley | RF01 |

> **Concluída quando:** o formador adiciona um lembrete pela linha de comandos, fecha o terminal, e recebe a notificação no horário configurado.

### Fase 3 — Incrementais e consolidação

**Depende de:** MVP estável. Por ordem de obrigatoriedade, não de visibilidade:

1. **Testes automáticos** em `tests/` — cada um os do seu módulo
2. **Empacotamento PyInstaller** — Felipe
3. **RF07** — ações: som, pop-up, abrir aplicação ou URL — Niley
4. **RF08** — arranque automático com o sistema operativo — Felipe
5. **RF09** — execução de comando arbitrário, com confirmação e log (RNF05) — Niley
6. **RF10** — interface gráfica PySide6 — a decidir

**Critério da ordem.** Os testes e o empacotamento são o objeto de avaliação da
Etapa 4; o RF07 e o RF08 estão marcados como incrementais desde a Etapa 1. Uma ordem
guiada pelo efeito na demonstração colocava-os primeiro — mas se o tempo faltar, e o
risco R9 admite que pode faltar, o que cai tem de ser o dispensável.

O orçamento reforça-o: 32 horas para as cinco etapas, das quais a última é
apresentação. A Fase 3 completa não cabe. A ordem acima é, na prática, a decisão
antecipada sobre o que fica de fora.

O RF10 é caro e a sua função está coberta pela CLI.

### 7.1 Alinhamento com as etapas do curso

As cinco etapas do curso são o ciclo de vida clássico da engenharia de software,
uma etapa por atividade:

| Etapa | Atividade do ciclo de vida | Fases nossas |
|---|---|---|
| Etapa 1 — Levantamento de Requisitos | Análise | — |
| Etapa 2 — Arquitetura, Tecnologias e Planeamento | Projeto (*design*) | — |
| Etapa 3 — Desenvolvimento Colaborativo e Controlo de Versões | Implementação | 0, 1, 2 |
| Etapa 4 — Validação, Testes e Demonstração | Verificação e validação | 3 (testes, empacotamento) |
| Etapa 5 — Entrega Final e Apresentação | Entrega | Consolidação da documentação e ensaio da demonstração |

Ler assim as etapas diz-nos o que cada uma vai pedir antes de o enunciado sair, e
diz-nos onde cada documento pertence: os requisitos não se reabrem na Etapa 3, e as
decisões de tecnologia não se tomam na Etapa 4.

**Onde o nosso trabalho não é cascata, e porquê.** O modelo pressupõe o projeto
fechado antes de haver código. A Fase 0 contraria isso de propósito: um projeto
desenhado sobre bibliotecas que ninguém experimentou é adivinhação — foi um spike,
não a leitura de documentação, que fechou a escolha do agendador (D3).

A consequência: algumas decisões desta etapa mudam durante a implementação, e isso
fica registado no `docs/decisoes.md` com data e motivo — a diferença entre um grupo
que reviu o projeto e um grupo que improvisou.

---

## 8. Lista de tarefas

A lista vive em [`docs/tasks.md`](../../tasks.md), com os cinco campos exigidos pelo
enunciado: descrição, responsável, estado, data prevista e dependências.

Fica fora deste documento por ser atualizada a cada tarefa concluída, ao longo de todo
o projeto. Duplicá-la aqui garantia que as duas cópias divergiam à primeira semana.
O estado à data de qualquer entrega recupera-se pela etiqueta Git correspondente.

---

## 9. Milestones

| # | Conteúdo | Critério de aceitação |
|---|---|---|
| **M1 — Grupo capacitado** | Fase 0 | Os três spikes correm e o agendador está decidido |
| **M2 — Esqueleto vivo** | Fase 1 | `rememberme start` mostra o ícone e dispara notificação real |
| **M3 — MVP funcional** | Fase 2, RF01–RF06 | Lembrete criado pela CLI dispara no horário, com o programa em segundo plano |
| **M4 — Produto demonstrável** | Fase 3, parcial | Executável empacotado, testes a passar, demonstração ensaiada |

O **M1** é o primeiro milestone a registar no GitHub, conforme o ponto 6 da Etapa 2.

---

## 10. Riscos

| # | Risco | Mitigação |
|---|---|---|
| R1 | Ausência de `.gitignore` faz commitar `venv/` ou `__pycache__` | Primeiro ficheiro da Fase 1, antes de qualquer código |
| R2 | Versões diferentes das bibliotecas entre os três | `pyproject.toml` com versões fixadas |
| R3 | Conflito de thread principal entre bandeja, agendador e CLI | Aparece no spike do `pystray`, feito pelo integrador (Fase 0); modelo validado na Fase 1 |
| R4 | `plyer` limitado em Windows | Aparece no spike do `plyer` (Fase 0); abstração com backend alternativo (5.2) |
| R5 | RF02 exigir lógica manual, se a escolha for `schedule` | Decisão informada pelo spike; lógica isolada atrás da interface própria |
| R6 | Curva de aprendizagem das bibliotecas maior que o previsto | Fase 0 mede-a antes de o cronograma depender dela |
| R7 | Divergência das branches entre pontos de integração | `models.py` congelado antes da Fase 2 — é o único ponto de colisão real |
| R8 | Participação desequilibrada no histórico Git | Ficheiros distintos por elemento (§ 4.2) + tarefas de compensação atribuídas no `tasks.md` (§ 4.5) |
| R9 | Falta de tempo para os requisitos incrementais | Ordem de prioridade fixada na Fase 3; RF07–RF10 já marcados como opcionais na Etapa 1 |
| R10 | Testes apenas em Windows | Já assumido e justificado na Etapa 1; manter documentado como limitação conhecida |
| R11 | O PyInstaller pode não empacotar o backend do `plyer`, que é importado dinamicamente e escapa à análise estática. Sintoma: corre em desenvolvimento, falha no executável | Verificar logo no primeiro empacotamento, não na véspera da entrega; mitigação conhecida é declarar `--hidden-import` |

---

## 11. Critérios de conclusão

Uma tarefa passa a `pronto` quando:

1. O código corre sem erros na máquina de quem o escreveu;
2. Está integrado em `develop` no ponto de integração agendado (§ 6.3);
3. O `docs/tasks.md` foi atualizado no mesmo commit ou no seguinte;
4. Se altera comportamento visível ao utilizador, o `README.md` reflete a mudança.
