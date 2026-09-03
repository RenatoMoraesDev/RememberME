"""Mostrar uma notificacao no ambiente de trabalho.

"""

TITULO = "RememberME"


def notificar(mensagem: str, titulo: str = TITULO) -> None:
    """Mostra uma notificacao.

    Nao levanta exceção se falhar: um lembrete que nao aparece nao pode deitar
    abaixo o programa todo.
    """
    # TODO (Niley): plyer.notification.notify(title=..., message=..., timeout=10)
    raise NotImplementedError("Niley: preencher com o plyer")
