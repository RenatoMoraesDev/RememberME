# Tecnologias a utilizar
- Linguagens de programação: Python (Linguagem mais aderente ao projeto - cli/desktop multiplataforma - win/linux/mac)
- Frameworks: Typer (Abstração e padronização de interface de comandos de linha entre sistemas operativos)
- Bibliotecas: PyInstaller (Simplificar a instalação do programa para utilizadores leigos)
- Base de dados: Sqlite3 (Abstrair estrutura de dados e geri-los localmente)
- API: nenhum
- Tecnologia de frontend: PySide6 (Agilidade e padronização de interfaces gráficas), pystray (Padronização de acesso ao sistema em múltiplos sistemas operativos)
- Tecnologia de backend: APScheduler (Agendamentos ancorados no relógio e janelas de horário expressas no próprio gatilho — ver justificação abaixo), plyer (Padronização de notificações)
- Ambiente de desenvolvimento: Vscode, git e github

# Âmbito de cada tecnologia

O projeto tem requisitos de MVP e requisitos incrementais, e nem todas as tecnologias
acima entram nos dois. Distinguir isto agora evita que a entrega final divirja do que
foi projetado nesta etapa:

| Tecnologia | Âmbito |
|---|---|
| Python, SQLite3, Typer, APScheduler, plyer, pystray, PyInstaller | Núcleo — entram no MVP |
| PySide6 | **Condicional ao RF10**, que é incremental. Só entra se houver tempo depois de o MVP estar testado e empacotado |

O RF10 (interface gráfica) é o último da lista de incrementais e o primeiro a cair se
o orçamento de horas apertar. Fica declarado como escolha de tecnologia — se o RF10
avançar, é com PySide6 — mas não como compromisso de entrega.

# Links
- Pystray: [https://github.com/moses-palmer/pystray](https://github.com/moses-palmer/pystray)
- PyInstaller: [https://pyinstaller.org/en/stable/](https://pyinstaller.org/en/stable/)
- SQLite3: [https://sqlite.org/](https://sqlite.org/)
- PySide6: [https://wiki.qt.io/Qt_for_Python](https://wiki.qt.io/Qt_for_Python)
- APScheduler: [https://apscheduler.readthedocs.io/](https://apscheduler.readthedocs.io/)
- Plyer: [https://github.com/kivy/plyer](https://github.com/kivy/plyer)
- Typer: [https://typer.tiangolo.com/](https://typer.tiangolo.com/)
- uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

# Justificações

## Escolha do motor de agendamento

Foram comparadas as duas candidatas com código a correr, em
`spikes/agendador/` no repositório — ambas implementam corretamente o RF01
e o RF02. A diferença que decidiu foi **onde os disparos são ancorados**:

| | `schedule` | APScheduler |
|---|---|---|
| Ancoragem | No momento em que o programa arranca | No relógio |
| Janela de horário (RF02) | Verificada à mão dentro de cada tarefa | É o próprio gatilho: `CronTrigger(hour="8-13", minute=0)` |
| Dias da semana | Um método por dia, não aceita lista | `day_of_week="mon,tue,wed"` |
| Thread de segundo plano | Escrita por nós | `BackgroundScheduler` |
| Dependências | Nenhuma | `tzlocal` |

O RF02 pede "a cada hora, das 8h às 14h". Com o `schedule`, se a aplicação arrancar
às 08:07 os avisos saem às 09:07, 10:07…, e mudam sempre que o computador reinicia.
Com o APScheduler saem às 08:00, 09:00, 10:00, independentemente do arranque.
Num programa cuja função é lembrar de tarefas ligadas ao horário da aula, horários
imprevisíveis são um defeito, não uma preferência.

O custo aceite é uma dependência adicional (`tzlocal`) e uma curva de aprendizagem
maior. Fica contido pelo `scheduler.py`, que expõe funções próprias
(`agendar`, `remover`, `iniciar`, `parar`) e é o único ficheiro que conhece a
biblioteca — ver decisão D4.

## Porquê o uv e não o `pip` com `venv`

| | `python -m venv` + `pip` | `uv sync` |
|---|---|---|
| Passos até correr o projeto | criar venv, ativar, instalar | um |
| Ativar o ambiente | obrigatório, e a sintaxe muda com o terminal | não é preciso |
| Versões iguais nas três máquinas | só se alguém mantiver os pins à mão | garantido pelo `uv.lock` |
| Python em falta | instalar à parte | o uv descarrega-o |

O que decide é a terceira linha. O `uv.lock` regista a versão exata de **todas** as
dependências, incluindo as que vieram por arrasto, e vai para o repositório: os
três correm rigorosamente o mesmo. Um erro que só aparece na máquina de uma pessoa
é das coisas mais caras de resolver num trabalho de grupo.

Para atualizar uma dependência, altera-se o mínimo no `pyproject.toml` e corre-se
`uv lock --upgrade`. O `uv.lock` muda, entra num commit, e os outros apanham-no no
`uv sync` seguinte.

### Sem uv

O projeto continua a ser um pacote Python normal. Quem preferir:

```bash
pip install -e .
```

Mas aí as versões instaladas são as que o `pip` resolver nesse dia, não as do
`uv.lock`.
