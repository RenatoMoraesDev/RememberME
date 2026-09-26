# Plano de testes

Item 1 do entregável da Etapa 4. Cobre RF01, RF02, RF03, RF04 e RF06 —
os requisitos MVP implementados e utilizáveis via CLI (ver
[`documentacao.md`](documentacao.md) para RF05, RF07, RF08, RF09 e RF10).

**Resultado obtido** e **Estado** ficam em branco até cada teste ser
executado. Estado: `Passou` / `Falhou`. A coluna **Vídeo** aponta para o
ficheiro em [`videos/`](videos/) — em branco até ser gravado (convenção de
nome em [`videos/README.md`](videos/README.md)).

## RF01 — Lembrete de hora fixa

| Teste | Pré-condições | Passos | Resultado esperado | Resultado obtido | Estado | Vídeo |
|---|---|---|---|---|---|---|
| T01 | Aplicação instalada, base de dados vazia | `rememberme add "Beber água" --as 08:30` | Lembrete gravado; `rememberme list` mostra tipo `hora`, agenda `08:30` |Lembrete criado com sucesso e verificado na lista |Passou |[T01.mp4](videos/T01.mp4)|
| T02 | — | `rememberme add "Sem horário"` (sem `--as` nem `--entre`) | Erro: "indique --as ou --entre" | Erro : indique --as ou --entre|Passou| [T02.mp4](videos/T02.mp4)|
| T03 | Aplicação instalada | `rememberme add "Hora inválida" --as 25:99` | Erro de formato: "'25:99' nao e' uma hora no formato HH:MM" |  Invalid value for '--as': '25:00' nao e' uma hora no formato HH:MM |Passou | [T03.mp4](videos/T03.mp4)|
T04 |Ciar um Lembrete a correr (`rememberme start --debug`) | Aguardar a hora configurada | Notificação de sistema aparece com o texto do lembrete | Notificação exibida com sucesso na hora configurada | Passou | [T04.mp4](videos/T04.mp4) |
## RF02 — Lembrete recorrente numa janela

| Teste | Pré-condições | Passos | Resultado esperado | Resultado obtido | Estado | Vídeo |
|---|---|---|---|---|---|---|
| T05 | Base de dados vazia | `rememberme add "Levantar" --entre 08:00-14:00 --a-cada 60` | Lembrete gravado; `rememberme list` mostra tipo `janela`, agenda `08:00-14:00 (60 min)` | Lembrete gravado e exibido em `list` como tipo janela | Passou | [T05.mp4](videos/T05.mp4) |
| T06 | — | `rememberme add "Sem intervalo" --entre 08:00-14:00` (sem `--a-cada`) | Erro: "--entre exige --a-cada" | Erro exibido: "--entre exige --a-cada" | Passou | [T06.mp4](videos/T06.mp4) |
| T07 | — | `rememberme add "Intervalo sem janela" --as 08:00 --a-cada 30` | Erro: "--a-cada so pode ser usado com --entre" | Erro exibido: "--a-cada so pode ser usado com --entre" | Passou | [T07.mp4](videos/T07.mp4) |
| T08 | — | `rememberme add "Janela malformada" --entre 08:00 --a-cada 30` | Erro: "--entre deve estar no formato HH:MM-HH:MM" |  Invalid value: --entre deve estar no formato HH:MM-HH:MM  | Passou | [T08.mp4](videos/T08.mp4) |
| T09 | Lembrete T05 criado, aplicação a correr dentro da janela | Aguardar um disparo | Notificação aparece no minuto esperado, dentro da janela 08:00–14:00 | Notificação exibida com sucesso dentro da janela configurada | Passou | [T09.mp4](videos/T09.mp4) |

## RF03 — Ícone na bandeja do sistema

| Teste | Pré-condições | Passos | Resultado esperado | Resultado obtido | Estado | Vídeo |
|---|---|---|---|---|---|---|
| T10 | Nenhum processo `rememberme` a correr | `rememberme start` | Ícone azul aparece na bandeja do sistema; comando devolve a consola | Ícone azul exibido na bandeja do sistema e consola devolvida com sucesso | Passou | [T10.mp4](videos/T10.mp4) |
| T11 | Ícone visível (T10) | Clique direito → "Sair" | Ícone desaparece da bandeja; processo em segundo plano termina | Ícone removido da bandeja e processo em segundo plano encerrado com sucesso | Passou | [T11.mp4](videos/T11.mp4) |
| T12 | Processo a correr em segundo plano | `rememberme stop` | Processo termina sem intervenção na bandeja; ícone desaparece | | | |

> Nota: o menu da bandeja só tem "Sair" — a opção "ver lembretes ativos"
> prevista no requisito não está implementada. Ver limitação em
> [`documentacao.md`](documentacao.md).

## RF04 — Persistência local (SQLite)

| Teste | Pré-condições | Passos | Resultado esperado | Resultado obtido | Estado | Vídeo |
|---|---|---|---|---|---|---|
| T13 | Lembrete criado (T01) | `rememberme stop`, depois `rememberme start --debug` novamente | `rememberme list` continua a mostrar o lembrete; volta a disparar na hora certa | | | |
| T14 | — | Verificar a pasta de dados do utilizador (`rememberme.db`) | Ficheiro SQLite existe fora da pasta do repositório, sobrevive ao encerramento do processo | | | |

## RF06 — CRUD de lembretes via CLI

| Teste | Pré-condições | Passos | Resultado esperado | Resultado obtido | Estado | Vídeo |
|---|---|---|---|---|---|---|
| T15 | Base de dados vazia | `rememberme list` | "Nenhum lembrete encontrado." | | | |
| T16 | Lembrete T01 criado (ID conhecido) | `rememberme edit <id> --as 10:00` | "Lembrete <id> atualizado."; `list` mostra a nova hora | | | |
| T17 | — | `rememberme edit 999 --as 10:00` (ID inexistente) | "Lembrete 999 não encontrado." | | | |
| T18 | — | `rememberme edit <id>` sem nenhuma opção | Erro: "indique pelo menos uma alteracao: --texto, --as, --entre, --a-cada ou --dias" | | | |
| T19 | Lembrete existente, ativo | `rememberme off <id>` | "Lembrete <id> desativado."; `list` mostra `Ativo = nao` | | | |
| T20 | Lembrete desativado (T19) | `rememberme on <id>` | "Lembrete <id> ativado."; `list` mostra `Ativo = sim` | | | |
| T21 | Lembrete existente | `rememberme remove <id>` | "Lembrete <id> removido."; deixa de aparecer em `list` | | | |
| T22 | — | `rememberme remove 999` (ID inexistente) | "Lembrete 999 nao existe." | | | |
