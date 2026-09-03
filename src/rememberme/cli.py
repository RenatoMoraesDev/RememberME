"""Os comandos que se escrevem no terminal.

    rememberme add "Beber agua" --entre 08:00-14:00 --a-cada 60
    rememberme add "Ligar ao cliente" --as 09:30 --dias seg,qua
    rememberme list
    rememberme edit 3 --as 10:00
    rememberme remove 3
    rememberme on 3 / rememberme off 3
    rememberme start / rememberme stop

Os comandos que mexem em lembretes escrevem na base de dados e terminam. Nao
falam com o programa que esta' a correr: ele releh a base de dados sozinho.

Duas armadilhas do Typer, ja' encontradas e verificadas (notas/03-spike-cli.md):

1. Com UM SO' @app.command(), o Typer o trata como comando unico e recusa o
   nome do subcomando. So' com dois ou mais e' que `rememberme add` funciona.
2. Validar no `callback=` da opcao da' a mensagem com o nome da opcao;
   validar no corpo da funcao da' a mensagem nua. A regra cruzada entre --as e
   --entre TEM de ser no corpo, porque nenhuma das opcoes sabe da outra.
"""

import re
from typing import Optional

import typer

from rememberme import app as aplicacao
from rememberme import storage
from rememberme.models import DIAS, Lembrete

app = typer.Typer(help="Lembretes de tarefas recorrentes.")


# validacao partilhada 

def hora_valida(valor: Optional[str]) -> Optional[str]:
    """Aceita HH:MM. Usada no `callback=` das opcoes de hora."""
    if valor is None:
        return None
    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", valor):
        raise typer.BadParameter(f"'{valor}' nao e' uma hora no formato HH:MM")
    return valor


# lembretes

@app.command()
def add(
    texto: str = typer.Argument(..., help="O que o lembrete diz."),
    as_: Optional[str] = typer.Option(
        None, "--as", callback=hora_valida, help="Hora fixa: --as 08:30"),
    entre: Optional[str] = typer.Option(
        None, "--entre", help="Janela de horario: --entre 08:00-14:00"),
    a_cada: Optional[int] = typer.Option(
        None, "--a-cada", min=1, help="Minutos entre disparos, dentro da janela."),
    dias: str = typer.Option(
        ",".join(DIAS), "--dias", help="Dias: --dias seg,qua,sex"),
):
    """Acrescenta um lembrete.

    Ou `--as`, ou `--entre` **e** `--a-cada`. Nunca as duas formas.
    """
    # TODO (Felipe): validar a combinacao, construir o Lembrete,
    #                chamar storage.criar() e escrever o id ao utilizador.
    raise NotImplementedError("Felipe: preencher")


@app.command("list")
def listar():
    """Mostra os lembretes gravados."""
    # TODO (Felipe): storage.listar() e imprimir em tabela.
    raise NotImplementedError("Felipe: preencher")


@app.command()
def edit(id: int):
    """Altera um lembrete existente (RF06)."""
    # TODO (Felipe): storage.obter(), aplicar as opcoes, storage.atualizar().
    raise NotImplementedError("Felipe: preencher")


@app.command()
def remove(id: int):
    """Apaga um lembrete (RF06)."""
    # TODO (Felipe): storage.apagar(id) e dizer se apagou ou se nao existia.
    raise NotImplementedError("Felipe: preencher")


@app.command()
def on(id: int):
    """Ativa um lembrete."""
    raise NotImplementedError("Felipe: preencher")


@app.command()
def off(id: int):
    """Desativa um lembrete sem o apagar."""
    raise NotImplementedError("Felipe: preencher")


# o programa residente   [Renato] 

@app.command()
def start():
    """Arranca a bandeja e o agendador. Fica a correr ate' ao `stop`."""
    aplicacao.arrancar()


@app.command()
def stop():
    """Pede ao programa que esta' a correr para encerrar."""
    aplicacao.pedir_paragem()
    typer.echo("paragem pedida")
