# Documentação prévia

Item 3 do entregável da Etapa 4.

## Funcionalidades implementadas

| RF | Descrição | Onde |
|---|---|---|
| RF01 | Notificação num horário fixo pré-definido | `scheduler.py` (`CronTrigger`), `cli.py add --as` |
| RF02 | Recorrência dentro de uma janela de horário | `scheduler.py`, `cli.py add --entre/--a-cada` |
| RF03 | Ícone na bandeja com menu básico ("Sair") | `tray.py` |
| RF04 | Persistência local em SQLite, sem rede | `storage.py` |
| RF06 | Adicionar, editar, remover lembretes via CLI | `cli.py` (`add`, `edit`, `remove`, `on`, `off`, `list`) |

## Funcionalidades não implementadas

- **RF05 — Tarefas administrativas pré-cadastradas.** Não há dados nem
  comando de seed; a base de dados começa vazia.
- **RF08 — Arranque automático com o sistema operativo.** Não há registo no
  arranque do Windows (nem equivalente noutro SO); a aplicação só corre se
  for iniciada manualmente com `rememberme start`.
- **RF09 — Execução de comando arbitrário como ação de um lembrete.** Não
  implementado; `app.py` só suporta as ações fixas `abrir`, `som`, `popup`
  e `notificacao` (RF07). Sem RF09, o RNF05 (confirmação e log ao executar
  o comando) também não se aplica.
- **RF10 — Interface gráfica (PySide6).** Não implementada; só existe a
  CLI (`cli.py`) e a bandeja do sistema.

### RF07 — parcialmente implementado

A lógica de disparo por tipo de ação (notificação, som, popup, abrir
app/URL) existe em `app.py` (`ao_disparar`) e a base de dados já tem as
colunas `accao`/`accao_param` (`storage.py`). Mas nenhum comando do CLI
(`add` ou `edit`) expõe uma opção para definir essa ação — todo lembrete
criado fica com `accao = "notificacao"` por omissão. Por não ser
acionável ponta-a-ponta pelo utilizador, RF07 não entra no
[`plano-testes.md`](plano-testes.md).

## Guia de instalação

Pré-requisito: [`uv`](https://docs.astral.sh/uv/) instalado.

```bash
git clone <url-do-repositorio>
cd rememberme-lab2
uv sync
```

## Instruções de execução

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
rememberme start --debug   # corre em primeiro plano, para depuração
rememberme start           # corre em segundo plano
rememberme stop            # pede o encerramento
```

## Limitações conhecidas

- Menu da bandeja só tem "Sair" — não mostra os lembretes ativos, apesar
  de o RF03 prever essa opção.
- RF07 (ações por lembrete) não é configurável via CLI — ver acima.
- RF05 e RF08 não implementados.
- Sem testes automatizados (`pytest` ou equivalente) no repositório até
  esta etapa — o plano de testes desta etapa é manual.

## Melhorias futuras

- Expor `--accao`/`--accao-param` em `cli.py add`/`edit` para completar o RF07.
- Adicionar lembretes pré-carregados na primeira execução (RF05).
- Registar a aplicação no arranque do sistema operativo (RF08).
- Acrescentar "ver lembretes ativos" ao menu da bandeja (`tray.py`).
- Suportar execução de comando arbitrário como ação, com confirmação e log (RF09/RNF05).
- Interface gráfica em PySide6 como alternativa à CLI (RF10).
- Suite de testes automatizados para `storage.py` e `scheduler.py`.
