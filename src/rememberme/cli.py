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
    if as_ and entre:
        raise typer.BadParameter(
            "use --as ou --entre, mas nao os dois"
        )

    if as_ and a_cada is not None:
        raise typer.BadParameter(
            "--a-cada so pode ser usado com --entre"
        )

    if entre and a_cada is None:
        raise typer.BadParameter(
            "--entre exige --a-cada"
        )

    if not as_ and not entre:
        raise typer.BadParameter(
            "indique --as ou --entre"
        )

    janela_inicio = None
    janela_fim = None

    if entre:
        partes = entre.split("-")

        if len(partes) != 2:
            raise typer.BadParameter(
                "--entre deve estar no formato HH:MM-HH:MM"
            )

        janela_inicio, janela_fim = partes

        hora_valida(janela_inicio)
        hora_valida(janela_fim)

    lembrete = Lembrete(
        texto=texto,
        hora=as_,
        janela_inicio=janela_inicio,
        janela_fim=janela_fim,
        intervalo_min=a_cada,
        dias_semana=dias,
    )

    lembrete_criado = storage.criar(lembrete)

    typer.echo(f"Lembrete criado com ID {lembrete_criado.id}")    


@app.command("list")
def listar():
    """Mostra os lembretes gravados."""
    lembretes = storage.listar()

    if not lembretes:
        typer.echo("Nenhum lembrete encontrado.")
        return

    linhas = []
    for lembrete in lembretes:
        if lembrete.e_hora_fixa:
            tipo = "hora"
            agenda = lembrete.hora
        else:
            tipo = "janela"
            agenda = f"{lembrete.janela_inicio}-{lembrete.janela_fim} ({lembrete.intervalo_min} min)"

        linhas.append([
            str(lembrete.id),
            lembrete.texto,
            tipo,
            agenda,
            lembrete.dias_semana,
            "sim" if lembrete.ativo else "nao",
        ])

    headers = ["ID", "Texto", "Tipo", "Agenda", "Dias", "Ativo"]
    largura = []
    for i in range(len(headers)):
        largura.append(max(len(headers[i]), *(len(linha[i]) for linha in linhas)))

    def format_row(row):
        return " | ".join(str(row[i]).ljust(largura[i]) for i in range(len(row)))

    

    typer.echo(format_row(headers))
    typer.echo("-+-".join("-" * largura[i] for i in range(len(headers))))
    for linha in linhas:
        typer.echo(format_row(linha))
    

@app.command()
def edit(id: int):
    """Altera um lembrete existente (RF06)."""
    # TODO (Felipe): storage.obter(), aplicar as opcoes, storage.atualizar().
    raise NotImplementedError("Felipe: preencher")

@app.command()
def remove(id: int):
    """Apaga um lembrete (RF06)."""
    apagou = storage.apagar(id)
    if apagou:
        typer.echo(f"Lembrete {id} apagado.")
    else:
        typer.echo(f"Lembrete {id} não encontrado.")



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
