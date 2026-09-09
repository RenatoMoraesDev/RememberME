"""Mostrar uma notificacao no ambiente de trabalho.

"""

TITULO = "RememberME"


def notificar(mensagem: str, titulo: str = TITULO) -> None:
    """Mostra uma notificacao.

    Nao levanta exceção se falhar: um lembrete que nao aparece nao pode deitar
    abaixo o programa todo.
    """
    # TODO (Niley): plyer.notification.notify(title=..., message=..., timeout=10)
    try:
        print (f"NOTIFICACAO: {titulo}: {mensagem}")
    except Exception as e:
        print(f"Erro ao notificar: {e}")
        # raise NotImplementedError("Niley: preencher com o plyer")
