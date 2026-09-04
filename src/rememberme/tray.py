"""O icone na bandeja do sistema e o seu menu (RF03).

- `arrancar()` BLOQUEIA a thread que a chama, até chamar `parar()`.
- `parar()` pode ser chamada de outra thread - e' assim que o `stop` funciona.
- O texto de um item do menu tem de ser uma FUNCAO, nao uma string, se quiser
  refletir estado que muda.
"""

from typing import Callable


def arrancar(ao_sair: Callable[[], None]) -> None:
    """Mostra o icone e BLOQUEIA até o programa encerrar.

    `ao_sair` é o que se chama quando o utilizador escolhe "Sair" no menu.
    """
    # TODO (Renato): pystray.Icon(...).run()
    raise NotImplementedError


def parar() -> None:
    """Tira o icone da bandeja e desbloqueia o `arrancar()`."""
    raise NotImplementedError
