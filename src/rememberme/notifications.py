"""Mostrar uma notificacao no ambiente de trabalho.

"""

TITULO = "RememberME"


from plyer import notification

def notificar(mensagem: str, titulo: str = TITULO) -> None:
    try:
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=10
        )
    except Exception:
        pass

