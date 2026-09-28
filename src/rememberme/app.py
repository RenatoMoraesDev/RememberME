"""Onde as pecas se ligam umas as outras.   [dono: Renato]

Modelo de threads (verificado no spike):

    thread principal    -> tray.arrancar()   bloqueia ate' encerrar
    thread do agendador -> dispara lembretes e a vigia da paragem

"""

import os
import subprocess
import sys

from rememberme import notifications, scheduler, storage, tray
from rememberme.models import Lembrete

#: Chave na tabela `estado` onde o `rememberme stop` escreve o pedido.
PARAGEM = "paragem_pedida"

#: Chave onde o "Sair" do tray pede a GUI (outro processo) que feche.
FECHAR_GUI = "fechar_gui"

#: De quantos em quantos segundos se pergunta se alguem pediu para parar.
INTERVALO_VIGIA = 5


def ao_disparar(lembrete: Lembrete) -> None:
    """Chamada pelo agendador quando chega a hora de um lembrete."""
    if lembrete.accao == "abrir":
        #abrir URL ou app
        import webbrowser
        webbrowser.open(lembrete.accao_param)

    elif lembrete.accao =="som":
        #tocar som
        import winsound
        winsound.PlaySound(lembrete.accao_param, winsound.SND_FILENAME)

    elif lembrete.accao == "popup":
        #: janelinha no canto do ecra, tipo balao antigo
        notifications.popup_canto(lembrete.accao_param or lembrete.texto)

    else:
        notifications.notificar(lembrete.texto)


def vigiar_paragem() -> None:
    """Lê a tabela `estado`; se o `stop` pediu paragem, encerra.

    Corre dentro do proprio agendador, de `INTERVALO_VIGIA` em
    `INTERVALO_VIGIA` segundos. E' o canal entre o comando `stop`, que e' outro
    processo, e este.
    """
    if storage.ler_estado(PARAGEM) == "1":
        encerrar()


def _caminho_lock():
    """Ficheiro que guarda o PID do servico, para nao arrancar dois de seguida."""
    return storage.caminho_bd().parent / "servico.pid"


def servico_ativo() -> bool:
    """True se ja houver um `arrancar()` a correr noutro processo."""
    caminho = _caminho_lock()
    if not caminho.exists():
        return False

    try:
        pid = int(caminho.read_text().strip())
    except ValueError:
        return False

    if sys.platform == "win32":
        import ctypes

        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False

    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


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
    _caminho_lock().unlink(missing_ok=True)


def sair_tudo() -> None:
    """O "Sair" do tray: encerra o servico e pede a GUI aberta que feche.

    O "Parar" da GUI e o `--stop` usam so' o encerrar(): parar o agendador nao
    deve fechar a janela onde o utilizador esta' a trabalhar.
    """
    storage.guardar_estado(FECHAR_GUI, "1")
    encerrar()


def arrancar() -> None:
    """O `rememberme start`. So' regressa quando o programa encerrar."""
    storage.guardar_estado(PARAGEM, "0")  # limpa pedidos antigos
    _caminho_lock().write_text(str(os.getpid()))

    scheduler.iniciar(ao_disparar)
    for lembrete in storage.listar(apenas_ativos=True):
        try:
            scheduler.agendar(lembrete)
        except ValueError:
            #: um lembrete mal configurado (ex: janela a atravessar a meia-noite)
            #: nao pode impedir os restantes de arrancar.
            pass

    scheduler.agendar_intervalo(vigiar_paragem, INTERVALO_VIGIA)

    tray.arrancar(ao_sair=sair_tudo)  # bloqueia aqui


def arrancar_em_segundo_plano() -> None:
    """Lança arrancar() num processo à parte, desligado do terminal.

    Nao faz nada se ja houver um servico a correr - evita processos duplicados.
    """
    if servico_ativo():
        return

    if sys.platform == "win32":
        _arrancar_windows()
    else:
        _arrancar_posix()


def _comando_relancar() -> list[str]:
    """O exe empacotado nao percebe "-m": relanca-se a si proprio com "--start"."""
    if getattr(sys, "frozen", False):
        return [sys.executable, "--start"]
    return [sys.executable, "-m", "rememberme", "start", "--debug"]


def _arrancar_windows() -> None:
    """Arranca o programa em Windows."""
    subprocess.Popen(
        _comando_relancar(),
        creationflags=subprocess.CREATE_NO_WINDOW,
        #: sem isto, o exe --onefile relancado herda a pasta temporaria (_MEI) do
        #: pai e perde-a quando o pai fecha; a variavel pede uma extracao propria.
        env={**os.environ, "PYINSTALLER_RESET_ENVIRONMENT": "1"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )


def _arrancar_posix() -> None:
    """Arranca o programa em Linux e MacOS."""
    subprocess.Popen(
        _comando_relancar(),
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )


def pedir_paragem() -> None:
    """O `rememberme stop`. Corre noutro processo: so' escreve o pedido."""
    storage.guardar_estado(PARAGEM, "1")


def parar_e_aguardar(limite_s: float = 15) -> bool:
    """O `--stop` do exe: pede a paragem e espera que o servico encerre.

    Usado pelo instalador/desinstalador. A vigia corre de `INTERVALO_VIGIA` em
    `INTERVALO_VIGIA` segundos, por isso o limite tem de ser bem maior.
    Devolve False se o servico nao encerrou a tempo (o instalador usa taskkill).
    """
    if not servico_ativo():
        return True
    pedir_paragem()

    import time

    fim = time.monotonic() + limite_s
    while time.monotonic() < fim:
        if not servico_ativo():
            time.sleep(1)  #: o lock e' apagado antes de o processo terminar
            return True
        time.sleep(0.5)
    return False


if __name__ == "__main__":
    #: entrada do executavel do PyInstaller.
    #: "--gui" abre so' a janela; "--start" arranca o servico (tray+agendador);
    #: sem argumentos (duplo-clique no exe) arranca o servico, se ainda nao
    #: houver um, e abre a GUI. "--stop" pede a paragem e espera (instalador).
    if "--stop" in sys.argv:
        sys.exit(0 if parar_e_aguardar() else 1)
    elif "--start" in sys.argv:
        arrancar()
    elif "--gui" in sys.argv:
        from rememberme import gui

        gui.arrancar()
    elif getattr(sys, "frozen", False):
        #: duplo clique no exe portatil: nao ha' atalho com "--start", por isso
        #: garante o tray e abre a janela. arrancar_em_segundo_plano() ja' evita
        #: duplicar o servico (ver servico_ativo()).
        arrancar_em_segundo_plano()
        from rememberme import gui

        gui.arrancar()
    else:
        arrancar()
