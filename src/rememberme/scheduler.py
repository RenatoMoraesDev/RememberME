"""Motor de agendamento.

    Lembrete (models.py)  ->  CronTrigger (APScheduler)

    hora = "08:30"                   -> CronTrigger(hour=8, minute=30)
    janela 08:00-14:00, a cada 60min -> CronTrigger(hour="8-14", minute=0)

"""

from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from rememberme.models import Lembrete


#: Traducao pt-en para os do APScheduler.
DIAS_APS = {"seg": "mon", "ter": "tue", "qua": "wed", "qui": "thu",
            "sex": "fri", "sab": "sat", "dom": "sun"}

_scheduler = None
_ao_disparar = None

def iniciar(ao_disparar: Callable[[Lembrete], None]) -> None:
    """Arranca o agendador em segundo plano.

    `ao_disparar` é chamada com o lembrete sempre que chega a hora. Quem chama
    decide o que fazer - normalmente notificar.
    """
    global _scheduler
    _ao_disparar = ao_disparar
    _scheduler = BackgroundScheduler()
    _scheduler.start()

def agendar(lembrete: Lembrete) -> None:
    """Põe um lembrete a disparar. Se já lá estava, substitui."""
    if lembrete.e_hora_fixa:
        hora, minuto = int(lembrete.hora.split(":")[0]), int(lembrete.hora.split(":")[1])
        trigger = CronTrigger(hour=hora, minute=minuto)
        _scheduler.add_job(_disparar, trigger, id=str(lembrete.id), args=(lembrete,),replace_existing=True)
    else:
        inicio, fim = int(lembrete.janela_inicio.split(":")[0]), int(lembrete.janela_fim.split(":")[0])
        if lembrete.intervalo_min == 60:
            minuto = "0"
        else:
            minuto = f"*/{lembrete.intervalo_min}"
        trigger = CronTrigger(hour=f"{inicio}-{fim}", minute=minuto)
        _scheduler.add_job(_disparar, trigger, id=str(lembrete.id), args=(lembrete,),replace_existing=True)


def remover(id: int) -> None:
    """Tira um lembrete do agendador. Não apaga da base de dados."""
    _scheduler.remove_job(str(id))


def parar() -> None:
    """Desliga o agendador. Chamado pelo `encerrar()` do app.py."""
    _scheduler.shutdown(wait=False)

def _disparar(lembrete):
    _ao_disparar(lembrete)