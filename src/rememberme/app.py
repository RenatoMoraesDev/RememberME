"""Onde as pecas se ligam umas as outras.   [dono: Renato]

Modelo de threads (verificado no spike):

    thread principal    -> tray.arrancar()   bloqueia ate' encerrar
    thread do agendador -> dispara lembretes e a vigia da paragem
"""

from rememberme import notifications, scheduler, storage, tray
from rememberme.models import Lembrete

#: Chave na tabela `estado` onde o `rememberme stop` escreve o pedido.
PARAGEM = "paragem_pedida"

#: De quantos em quantos segundos se pergunta se alguem pediu para parar.
INTERVALO_VIGIA = 5


def ao_disparar(lembrete: Lembrete) -> None:
    """Chamada pelo agendador quando chega a hora de um lembrete."""
    notifications.notificar(lembrete.texto)


def vigiar_paragem() -> None:
    """Lê a tabela `estado`; se o `stop` pediu paragem, encerra.

    Corre dentro do proprio agendador, de `INTERVALO_VIGIA` em
    `INTERVALO_VIGIA` segundos. E' o canal entre o comando `stop`, que e' outro
    processo, e este.
    """
    if storage.ler_estado(PARAGEM) == "1":
        encerrar()


def encerrar() -> None:
    """A UNICA forma de o programa acabar.

    Tanto o `rememberme stop` como o "Sair" do menu passam por aqui. Duas
    saidas com codigo proprio e' como uma delas se esquece de limpar a tabela.

    Nunca se mata o processo a bruta: em Windows isso deixa o icone na bandeja
    até passar o rato por cima.
    """
    storage.guardar_estado(PARAGEM, "0")
    scheduler.parar()
    tray.parar()  # desbloqueia o arrancar() la' em baixo


def arrancar() -> None:
    """O `rememberme start`. So' regressa quando o programa encerrar."""
    storage.guardar_estado(PARAGEM, "0")  # limpa pedidos antigos

    scheduler.iniciar(ao_disparar)
    for lembrete in storage.listar(apenas_ativos=True):
        scheduler.agendar(lembrete)

    # TODO (Renato): pedir ao agendador que chame vigiar_paragem() de
    # INTERVALO_VIGIA em INTERVALO_VIGIA segundos.

    tray.arrancar(ao_sair=encerrar)  # bloqueia aqui


def pedir_paragem() -> None:
    """O `rememberme stop`. Corre noutro processo: so' escreve o pedido."""
    storage.guardar_estado(PARAGEM, "1")
