"""Mostrar uma notificacao no ambiente de trabalho.

"""

TITULO = "RememberME"


from plyer import notification

def notificar(mensagem: str, titulo: str = TITULO) -> None:
    """Mostra uma notificacao.

    Nao levanta exceção se falhar: um lembrete que nao aparece nao pode deitar
    abaixo o programa todo.
    """
    try:
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=10
        )
    except Exception:
        pass