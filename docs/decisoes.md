# Registo de decisões técnicas

Uma entrada por decisão: o que se decidiu, quando, e porquê. Serve para não voltar a
discutir o mesmo e para justificar as escolhas na apresentação final.

**Responsável pela manutenção:** Niley.

---

## D1 — Layout `src/` para o código-fonte

**Data:** 02/09/2026 · **Estado:** aplicado

O pacote fica em `src/rememberme/` e não na raiz. Com o código na raiz, o Python
importa-o a partir do diretório de trabalho e o programa funciona sem estar
verdadeiramente instalado — o erro só aparece depois de empacotado, noutra máquina.
O layout `src/` obriga a instalar antes de correr, pelo que se testa o que se entrega.

## D2 — Base de dados fora do repositório

**Data:** 02/09/2026 · **Estado:** aplicado

O ficheiro SQLite fica na pasta de dados do utilizador, obtida por
`typer.get_app_dir("RememberME")`, que devolve o caminho correto em Windows, macOS e
Linux sem código condicional. Versionar a base de dados geraria conflitos a cada
execução e exporia dados de quem usa a aplicação.

## D3 — Motor de agendamento: APScheduler

**Data:** 04/09/2026 · **Estado:** decidido

Comparadas as duas candidatas com código a correr (`spikes/agendador/`). Ambas
cumprem o RF01 e o RF02; a diferença que decidiu foi a ancoragem dos disparos.

O `schedule` conta o intervalo a partir do momento em que o programa arranca: uma
recorrência de hora a hora iniciada às 08:07 dispara às 09:07, 10:07, e muda a cada
reinício do computador. O APScheduler ancora no relógio e dispara às 08:00, 09:00,
independentemente do arranque. Para lembretes ligados ao horário da aula, horários
imprevisíveis são um defeito funcional.

Soma-se que a janela de horário do RF02 se exprime diretamente no gatilho
(`CronTrigger(hour="8-13", minute=0)`), enquanto no `schedule` teria de ser
verificada à mão dentro de cada tarefa — 13 linhas a mais de lógica de calendário
escrita por nós, que é onde nascem os erros.

**Custo aceite:** uma dependência a mais (`tzlocal`) e mais conceitos a aprender
(*scheduler*, *job*, *trigger*). Fica contido pela decisão D4.

**Consequências:** desbloqueia o `pyproject.toml` e o `scheduler.py`. Atenção ao
limite da janela — `hour="8-14"` inclui as 14h; definir no `models.py` se
`janela_fim` é inclusivo ou exclusivo.

## D4 — Interface própria para o agendador

**Data:** 02/09/2026 · **Estado:** aceite

Seja qual for a biblioteca escolhida, o `scheduler.py` expõe funções próprias —
`agendar()`, `remover()`, `iniciar()`, `parar()`. A biblioteca fica isolada num
ficheiro e pode ser trocada sem tocar no resto do projeto.

## D5 — Notificação com backend selecionável

**Data:** 02/09/2026 · **Estado:** aceite

O `notifications.py` expõe apenas `notificar(titulo, mensagem)`. O backend é interno:
`plyer` por omissão, `pystray.Icon.notify()` como alternativa. O requisito é notificar
o formador, não usar uma biblioteca específica.

## D6 — Nome do comando e do pacote: `rememberme`

**Data:** 02/09/2026 · **Estado:** decidido

O executável instalado chama-se `rememberme` e o pacote em `src/` também. Antes o
pacote chamava-se `remember`, o que daria duas grafias para a mesma coisa
(`python -m remember` mas `rememberme` na consola) sem qualquer motivo.

`remember` é ainda uma palavra genérica: um executável com esse nome no `PATH`
tem hipóteses reais de colidir com outra coisa na máquina de quem instala.

**Consequências:** renomear `src/remember/` para `src/rememberme/` antes de haver
código lá dentro — hoje o custo é zero, na Fase 2 obrigaria a mexer em todos os
`import`. No `pyproject.toml`:

```toml
[project.scripts]
rememberme = "rememberme.cli:app"
```

## D7 — Paragem pela tabela `estado`; instância única fica de fora

**Data:** 02/09/2026 · **Estado:** decidido · **Revisto a 02/09/2026**

O `rememberme start` deixa o programa a correr na bandeja, logo tem de haver
forma de o parar de fora: `rememberme stop`. Um comando `start` sem `stop` é uma
assimetria que ninguém consegue explicar a quem usa o programa.

**Como funciona.** Uma tabela `estado(chave TEXT PRIMARY KEY, valor TEXT)`. O
`stop` escreve `paragem_pedida = 1`; o processo residente lê-a de cinco em cinco
segundos, num trabalho do próprio agendador, e desliga-se por sua iniciativa.

A base de dados é o sítio certo porque o processo residente vai ter de a reler
de qualquer forma, para apanhar lembretes criados pelo `add` enquanto corre.
Quando isso acontecer, a leitura do pedido de paragem não custa nada — é o mesmo
caminho, e fica um só canal entre os comandos e o processo.

O "Sair" do menu da bandeja e o `stop` chamam a mesma função `encerrar()`. Duas
saídas com código próprio é como uma delas se esquece de limpar a tabela. E
nunca se mata o processo: em Windows isso deixa o ícone na bandeja até alguém
lhe passar o rato por cima.

### O que esta decisão deixou cair

A versão anterior desta entrada acrescentava um segundo mecanismo, para impedir
duas instâncias em simultâneo: um ficheiro sobre o qual o `start` pedia ao
sistema operativo um **bloqueio exclusivo**, com `msvcrt.locking` em Windows e
`fcntl.flock` em Unix. O argumento continua correto — um bloqueio não fica
obsoleto quando o processo morre, ao contrário de um PID guardado numa tabela,
que o sistema operativo mais tarde reutiliza.

**Retirado mesmo assim, e o motivo é de âmbito, não técnico.** Nenhum requisito
pede instância única; apareceu como bónus do `stop`. Em troca era a única parte
do projeto com código dependente do sistema operativo, num grupo que está a
aprender Python, e a única que só se testa a matar processos à força.

O custo de a retirar: quem correr `start` duas vezes fica com dois ícones na
bandeja e notificações repetidas. É um incómodo visível e reversível — fecha-se
um dos dois. O custo de a manter seria um módulo a mais no caminho crítico da
Fase 1. Se algum dia incomodar, o argumento acima fica aqui à espera.

## D8 — Pull Request apenas de `develop` para `master`

**Data:** 02/09/2026 · **Estado:** decidido

O trabalho diário integra-se em `develop` por merge direto da branch de cada um. O
`master` só recebe código por Pull Request, um por etapa, no momento da entrega.

**Porquê.** O Pull Request passa a marcar a fronteira entre trabalhar e entregar. O
histórico de `master` fica com um commit por entrega, cada um etiquetado
(`etapa-3`, `etapa-4`), em vez de dezenas de integrações intermédias — o que torna
o repositório legível para quem o avalia sem ler o log todo.

Exigir Pull Request a cada tarefa, num grupo de três pessoas que trabalham em
ficheiros distintos por desenho (§4.2 do plano de desenvolvimento), acrescentaria
uma espera por revisão sem prevenir conflitos que a divisão de ficheiros já previne.

**O que isto custa, assumidamente.** Deixa de haver revisão cruzada registada no
GitHub a cada tarefa. O plano de desenvolvimento prometia-a e foi corrigido: não
faz sentido entregar um documento a descrever um mecanismo que o repositório vai
desmentir. A participação individual continua visível pelo histórico de commits e
pela divisão de responsabilidades do `tasks.md`.

## D9 — `uv` para gerir o ambiente e as dependências

**Data:** 02/09/2026 · **Estado:** decidido

O ambiente e as dependências são geridos pelo [uv](https://docs.astral.sh/uv/).
Um comando — `uv sync` — descarrega o Python se faltar, cria o `.venv/`, instala
as dependências e o próprio projeto em modo editável. Correr é `uv run rememberme`,
sem ativar ambiente nenhum.

**Porquê.** O que decide é o `uv.lock`, que fica no repositório e regista a versão
exata de todas as dependências, incluindo as indiretas. Os três passam a correr
rigorosamente o mesmo código: um erro que só aparece na máquina de uma pessoa é dos
mais caros de diagnosticar num grupo, e mais ainda num grupo que está a aprender a
linguagem. Com `pip` e `venv`, essa garantia depende de alguém manter pins à mão.

Em segundo lugar, encurta o arranque: deixa de ser necessário explicar ambientes
virtuais, ativação — cuja sintaxe muda com o terminal — e a diferença entre ter o
projeto instalado ou não.

**Custo.** Mais uma ferramenta a instalar, uma vez por máquina. O projeto continua
a ser um pacote Python normal: `pip install -e .` funciona na mesma, apenas sem a
garantia do lock.

**Consequência no `pyproject.toml`:** as dependências passaram de `==` para `>=`.
As duas coisas dizem coisas diferentes — o `pyproject` diz *"funciona a partir
de"*, o lock diz *"é isto que estamos os três a usar"*. Atualizar é
`uv lock --upgrade`, e o lock alterado entra num commit.

