# RememberME

![RememberME](logo.png)

Aplicação desktop que roda em segundo plano e lembra o formador de executar tarefas administrativas recorrentes durante a aula — fechar sessão, fazer a chamada, entre outras rotinas — por meio de notificações configuráveis por horário fixo ou recorrente.

## Sobre o projeto

Projeto final do curso IEFP — Programação, Nível 5 (formador: CID).

**Grupo:** Felipe Ribeiro, Niley Barros, Renato Moraes

## Status

Etapa 1: Definição do Problema e Análise de Requisitos. - Concluída
Etapa 2: Definição do projecto. - Entrega a **04/09/2026**.

## Como começar

O projeto usa o [**uv**](https://docs.astral.sh/uv/) para gerir o ambiente e as
dependências. Enquanto não houver uma versão empacotada, é assim que se instala e
se corre o RememberME — tanto para desenvolver como para simplesmente usar.

### 1. Instalar o uv

Uma vez por máquina. No PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Fecha e reabre o terminal, e confirma:

```bash
uv --version
```

### 2. Obter o projeto

```bash
git clone https://github.com/<utilizador>/RememberME.git
```

```bash
cd RememberME
```

### 3. Preparar o ambiente

```bash
uv sync
```

Um comando só, e faz tudo: descarrega o Python 3.11 se não o tiveres, cria o
ambiente virtual em `.venv/`, instala as dependências **exatamente** nas versões
do `uv.lock` e instala o próprio RememberME em modo editável — o código passa a
correr onde está, e uma alteração num ficheiro tem efeito sem reinstalar nada.

Não é preciso ativar o ambiente. O `uv run` trata disso.

### 4. Correr

```bash
uv run rememberme --help
```

```bash
uv run rememberme add "Beber água" --entre 08:00-14:00 --a-cada 60
```

```bash
uv run rememberme list
```

E para o pôr a correr na bandeja do sistema, e depois parar:

```bash
uv run rememberme start
```

```bash
uv run rememberme stop
```

> O `start` fica a correr até ao `stop` ou até se escolher **Sair** no menu da
> bandeja. Não o mates à força: em Windows o ícone fica lá a fingir que o programa
> está vivo.

## Documentação

| Documento | |
|---|---|
| [Entregáveis por etapa](docs/entregaveis/) | Material submetido a avaliação |
| [Análise de requisitos](docs/entregaveis/etapa-1-analise/01-analise-requisitos.md) | Etapa 1 |
| [Plano de desenvolvimento](docs/entregaveis/etapa-2-projeto/plano-desenvolvimento.md) | Etapa 2 |
| [Quadro de tarefas](docs/tasks.md) | Estado atual do trabalho |
| [Decisões técnicas](docs/decisoes.md) | O que se decidiu e porquê |
| [Enunciados](docs/enunciados/) | Documentos do formador |

## Stack

Em avaliação, decisão formal prevista para a Etapa 2 (Arquitetura, Tecnologias e Planeamento). Cogitado até agora:

| Área | Tecnologia |
|---|---|
| Linguagem | Python |
| Linha de comandos | Typer |
| Bandeja do sistema | pystray |
| Notificações | plyer |
| Agendamento e recorrência | APScheduler |
| Base de dados | SQLite3 |
| Empacotamento | PyInstaller |
| Interface gráfica | PySide6 — **condicional ao RF10**, que é incremental |

Justificação de cada escolha em [`stack.md`](docs/entregaveis/etapa-2-projeto/stack.md),
e o registo das decisões com o respetivo motivo em [`decisoes.md`](docs/decisoes.md).

## Organização do trabalho

### Branches

`master` só recebe código estável, por merge de `develop` decidido em reunião de grupo.
`develop` é onde o trabalho se junta, nos pontos de integração agendados.

As restantes seguem a convenção `<tipo>/<nome>-<descrição>`:

| Tipo | Uso | Exemplo |
|---|---|---|
| `feat/` | Nova funcionalidade | `feat/niley-notificacoes` |
| `fix/` | Correção | `fix/felipe-cli-comando-remove` |
| `docs/` | Documentação | `docs/renato-plano-etapa2` |
| `test/` | Testes | `test/renato-storage` |
| `chore/` | Configuração e dependências | `chore/renato-gitignore` |
| `spike/` | Experiência descartável | `spike/felipe-typer` |

### Commits

`<tipo>: <descrição no imperativo>` — por exemplo, `feat: adicionar comando remove na CLI`.

### Integração

Pull Request para `develop`, revisto por outro elemento antes do merge.

## Contribuidores

| Nome | GitHub | Responsabilidades |
|---|---|---|
| Felipe Ribeiro | [@felipe-g-ribeiro](https://github.com/felipe-g-ribeiro) | Linha de comandos, empacotamento, documentação de utilização |
| Niley Barros | [@sacramentoniley-hub](https://github.com/sacramentoniley-hub) | Notificações, ações do utilizador, registo de decisões |
| Renato Moraes | [@RenatoMoraesDev](https://github.com/RenatoMoraesDev) | Coordenação, integração, persistência e agendamento |

Os papéis alternam ao longo das etapas e a revisão de código é cruzada.