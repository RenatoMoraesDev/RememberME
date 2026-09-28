# Documentação prévia

Item 3 do entregável da Etapa 4.

## Funcionalidades implementadas

| RF | Descrição | Onde |
|---|---|---|
| RF01 | Notificação num horário fixo pré-definido | `scheduler.py` (`CronTrigger`), `cli.py add --as` |
| RF02 | Recorrência dentro de uma janela de horário | `scheduler.py`, `cli.py add --entre/--a-cada` |
| RF03 | Ícone na bandeja com menu "Abrir" (clique simples abre a janela) e "Sair" (encerra o serviço e fecha a janela) | `tray.py` |
| RF04 | Persistência local em SQLite, sem rede | `storage.py` |
| RF06 | Adicionar, editar, remover lembretes via CLI | `cli.py` (`add`, `edit`, `remove`, `on`, `off`, `list`) |
| RF08 | Arranque automático com o sistema operativo (opcional, no instalador) | `RememberME.iss` (tarefa "Iniciar com o Windows": atalho com `--start` em Arranque) |
| RF10 | Interface gráfica (parcial, Tkinter) | `gui.py`: criar, editar, apagar, ativar/desativar lembretes; iniciar/parar o agendador |
| — | Distribuição: executável portátil e instalador | `RememberME.spec`, `RememberME.iss`, `build.ps1` |

## Funcionalidades não implementadas

- **RF05 — Tarefas administrativas pré-cadastradas.** Não há dados nem
  comando de seed; a base de dados começa vazia.

- **RF09 — Execução de comando arbitrário como ação de um lembrete.** Não
  implementado; `app.py` só suporta as ações fixas `abrir`, `som`, `popup`
  e `notificacao` (RF07). Sem RF09, o RNF05 (confirmação e log ao executar
  o comando) também não se aplica.

### RF10 — parcialmente implementado

Existe uma interface gráfica em Tkinter (`gui.py`), em vez do PySide6
previsto nos requisitos. Cobre a gestão de lembretes e o arranque/paragem
do agendador. Não mostra os lembretes ativos em tempo real (é preciso usar
"Atualizar lista").

### RF07 — parcialmente implementado

A lógica de disparo por tipo de ação (notificação, som, popup, abrir
app/URL) existe em `app.py` (`ao_disparar`) e a base de dados já tem as
colunas `accao`/`accao_param` (`storage.py`). Mas nenhum comando do CLI
(`add` ou `edit`) expõe uma opção para definir essa ação — todo lembrete
criado fica com `accao = "notificacao"` por omissão. A GUI expõe o campo
«Tipo de aviso», mas só com a opção «Popup»: os lembretes criados na GUI
ficam com `accao = "popup"`, e os criados na CLI com `"notificacao"`. Por não ser
acionável ponta-a-ponta pelo utilizador, RF07 não entra no
[`plano-testes.md`](plano-testes.md).

## Guia de instalação

### Utilizador final (Windows 64 bits)

- **Instalador:** `RememberME-Setup-v1.0.exe`. Instala em `C:\Program Files\RememberME`
  (pede administrador), cria atalhos no menu Iniciar e, opcionalmente, no ambiente de
  trabalho e no arranque do Windows.
- **Portátil:** `RememberME-Portable-v1.0.exe`. Não instala nada; pode ser copiado para
  qualquer pasta.

Em ambos os casos os lembretes ficam em `%APPDATA%\RememberME\rememberme.db`.

### Desenvolvimento

Pré-requisito: [`uv`](https://docs.astral.sh/uv/) instalado.

```bash
git clone https://github.com/RenatoMoraesDev/RememberME.git
cd RememberME
uv sync
```

### Gerar os executáveis

Pré-requisito adicional: Inno Setup 6 (`winget install JRSoftware.InnoSetup`).

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1 -Versao 1.0
```

Gera em `dist\` o portátil e o instalador.

## Instruções de execução

### Executável (portátil ou instalado)

| Como | O que faz |
|---|---|
| duplo clique | arranca o serviço na bandeja (se ainda não estiver a correr) e abre a janela |
| `RememberME.exe --start` | só o serviço (bandeja + agendador), sem janela |
| `RememberME.exe --gui` | só a janela |
| `RememberME.exe --stop` | pede o encerramento do serviço e espera até 15 s |

### CLI (desenvolvimento)

```bash
# sem instalar (útil em desenvolvimento)
uv run python -m rememberme <comando>

# ou, depois de `uv sync`, com o comando instalado
rememberme <comando>
```

Exemplos:

```bash
rememberme add "Beber água" --as 08:30
rememberme add "Levantar" --entre 08:00-14:00 --a-cada 60
rememberme list
rememberme gui             # abre a janela
rememberme start --debug   # corre em primeiro plano, para depuração
rememberme start           # corre em segundo plano
rememberme stop            # pede o encerramento
```

## Limitações conhecidas

- O menu da bandeja não mostra os lembretes ativos, apesar de o RF03
  prever essa opção.
- RF07 (ações por lembrete) não é configurável via CLI — ver acima.
- RF05 não implementado.
- O executável só existe para Windows 64 bits.
- O portátil e a versão instalada, no mesmo computador, partilham os
  mesmos lembretes.
- Ao escolher «Sair» na bandeja, a janela fecha em até 2 s e uma edição
  por guardar perde-se.
- O executável de ficheiro único arranca mais devagar (extrai-se para
  `%TEMP%`) e alguns antivírus podem desconfiar dele.
- Sem testes automatizados (`pytest` ou equivalente) no repositório até
  esta etapa — o plano de testes desta etapa é manual.

## Melhorias futuras

- Expor `--accao`/`--accao-param` em `cli.py add`/`edit` para completar o RF07.
- Adicionar lembretes pré-carregados na primeira execução (RF05).
- Acrescentar "ver lembretes ativos" ao menu da bandeja (`tray.py`).
- Suportar execução de comando arbitrário como ação, com confirmação e log (RF09/RNF05).
- Completar a GUI (RF10): lista de ações do RF07 além de «Popup», lembretes
  ativos em tempo real.
- Suite de testes automatizados para `storage.py` e `scheduler.py`.
