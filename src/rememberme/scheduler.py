"""Motor de agendamento.

    Lembrete (models.py)  ->  CronTrigger (APScheduler)

    hora = "08:30"                   -> CronTrigger(hour=8, minute=30)
    janela 08:00-14:00, a cada 60min -> CronTrigger(hour="8-14", minute=0)

"""

from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler

from rememberme.models import Lembrete


#: Traducao pt-en para os do APScheduler.
DIAS_APS = {"seg": "mon", "ter": "tue", "qua": "wed", "qui": "thu",
            "sex": "fri", "sab": "sat", "dom": "sun"}

_scheduler = None

def iniciar(ao_disparar: Callable[[Lembrete], None]) -> None:
    """Arranca o agendador em segundo plano.

    `ao_disparar` é chamada com o lembrete sempre que chega a hora. Quem chama
    decide o que fazer - normalmente notificar.
    """
    # TODO (Renato): BackgroundScheduler().start()
    global _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.start()

def agendar(lembrete: Lembrete) -> None:
    """Põe um lembrete a disparar. Se já lá estava, substitui."""
    raise NotImplementedError


def remover(id: int) -> None:
    """Tira um lembrete do agendador. Não apaga da base de dados."""
    raise NotImplementedError


def parar() -> None:
    """Desliga o agendador. Chamado pelo `encerrar()` do app.py."""
    _scheduler.shutdown(wait=False)
