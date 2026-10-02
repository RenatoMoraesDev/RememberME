# RememberME

![RememberME](logo.png)

Aplicação desktop que roda em segundo plano e lembra o formador de executar tarefas administrativas recorrentes durante a aula — fechar sessão, fazer a chamada, entre outras rotinas — por meio de notificações configuráveis por horário fixo ou recorrente.

## Sobre o projeto

Projeto final do curso IEFP — Programação, Nível 5 (formador: CID).

**Grupo:** Felipe Ribeiro, Niley Barros, Renato Moraes

## Status

**Versão 1.0** — as cinco etapas do curso estão concluídas. O código está congelado
nesta versão; a entrega final reúne o [relatório](docs/entregaveis/etapa-5-entrega/RelatorioFinal-UC00615.pdf)
e o [vídeo demonstrativo](docs/entregaveis/etapa-5-entrega/video-demonstrativo/RememberME.mp4).

O que a aplicação faz, hoje:

- cria lembretes com **hora fixa** ou **recorrência dentro de uma janela de horário**;
- notifica no ecrã, com a ação escolhida por lembrete (pop-up, som, abrir aplicação ou endereço);
- corre em segundo plano, com ícone na **bandeja do sistema**, e pode arrancar com o Windows;
- é usada pela **linha de comandos** (`rememberme add`, `list`, `edit`, `remove`, …) ou pela **janela gráfica** (`rememberme gui`).

## Instalar (Windows)

A forma mais simples, sem instalar Python nem mais nada. Na
[página da versão 1.0](https://github.com/RenatoMoraesDev/RememberME/releases/tag/v1.0)
há dois ficheiros:

| Ficheiro | Para quê |
|---|---|
| `RememberME-Setup-v1.0.exe` | Instalador: acrescenta a aplicação ao menu Iniciar e permite arrancar com o Windows |
| `RememberME-Portable-v1.0.exe` | Executável único, sem instalação: corre onde estiver |

O Windows pode avisar que o editor é desconhecido, porque o executável não está
assinado. Escolher **Mais informações → Executar mesmo assim**.

### Limitações conhecidas

- Só existe para Windows 64 bits.
- Os intervalos de recorrência acima de 60 minutos não são suportados: o lembrete
  fica guardado mas não dispara. Os intervalos que não dividem a hora (45 minutos,
  por exemplo) dão disparos irregulares.
- A janela de horário só considera a hora inteira: `08:30-14:00` começa às 08:00 e
  inclui a hora das 14:00. Janelas que atravessam a meia-noite não funcionam.
- O menu da bandeja não mostra os lembretes ativos.
- Os lembretes pré-carregados (RF05) não estão implementados.

A lista completa, com as melhorias previstas, está em
[`documentacao.md`](docs/entregaveis/etapa-4-testes/documentacao.md#limitações-conhecidas).

## Desenvolver

O projeto usa o [**uv**](https://docs.astral.sh/uv/) para gerir o ambiente e as
dependências. É assim que se corre o código-fonte, para desenvolver ou para experimentar.

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
git clone https://github.com/RenatoMoraesDev/RememberME.git
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

Ou, em alternativa, abrir a janela gráfica:

```bash
uv run rememberme gui
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
| [Plano e resultados dos testes](docs/entregaveis/etapa-4-testes/plano-testes.md) | Etapa 4 — 22 testes, 22 aprovados |
| [Relatório final](docs/entregaveis/etapa-5-entrega/RelatorioFinal-UC00615.pdf) | Etapa 5 |
| [Vídeo demonstrativo](docs/entregaveis/etapa-5-entrega/video-demonstrativo/RememberME.mp4) | Etapa 5 |
| [Quadro de tarefas](docs/tasks.md) | Estado atual do trabalho |
| [Decisões técnicas](docs/decisoes.md) | O que se decidiu e porquê |
| [Enunciados](docs/enunciados/) | Documentos do formador |

## Stack

Decidida na Etapa 2 e ajustada na Etapa 4 (interface gráfica e instalador). As versões
das dependências estão fixadas no `uv.lock`, para que os três instalem exatamente o mesmo.

| Área | Tecnologia |
|---|---|
| Linguagem | Python |
| Linha de comandos | Typer |
| Bandeja do sistema | pystray |
| Notificações | plyer |
| Agendamento e recorrência | APScheduler |
| Base de dados | SQLite3 |
| Empacotamento | PyInstaller (`--onefile`) |
| Instalador | Inno Setup |
| Interface gráfica | Tkinter (prevista em PySide6; ver [D11](docs/decisoes.md#d11--interface-gráfica-em-tkinter-em-vez-de-pyside6)) |

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

Merge direto em `develop`, nos pontos de integração agendados. `develop` → `master` só por Pull Request, em reunião de grupo.

## Contribuidores

Alguns commits aparecem no GitHub sob mais do que uma conta, por terem sido feitos
de máquinas com configurações diferentes.

| Nome | GitHub |
|---|---|
| Felipe Ribeiro | [@felipe-g-ribeiro](https://github.com/felipe-g-ribeiro) |
| Niley Barros | [@nileysacramento](https://github.com/nileysacramento) e [@sacramentoniley-hub](https://github.com/sacramentoniley-hub) |
| Renato Moraes | [@hexemeister](https://github.com/hexemeister) e [@RenatoMoraesDev](https://github.com/RenatoMoraesDev) |
