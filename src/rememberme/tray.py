"""O icone na bandeja do sistema e o seu menu (RF03).

- `arrancar()` BLOQUEIA a thread que a chama, até chamar `parar()`.
- `parar()` pode ser chamada de outra thread - e' assim que o `stop` funciona.
- O texto de um item do menu tem de ser uma FUNCAO, nao uma string, se quiser
  refletir estado que muda.
"""

from typing import Callable

import pystray
from PIL import Image, ImageDraw
from pystray import Menu, MenuItem

_icone = None

def _criar_icone():
    """Desenha um icone simples em memoria, sem precisar de ficheiro PNG."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 4, 60, 60], fill="#2d7ff9")
    d.line([32, 18, 32, 34], fill="white", width=5)
    d.line([32, 34, 44, 40], fill="white", width=5)
    return img

def arrancar(ao_sair: Callable[[], None]) -> None:
    """Mostra o icone e BLOQUEIA até o programa encerrar.

    `ao_sair` é o que se chama quando o utilizador escolhe "Sair" no menu.
    """
    global _icone

    def _sair(icon, item):
        icon.stop()
        ao_sair()

    menu = Menu(MenuItem("Sair", _sair))
    _icone = pystray.Icon("rememberme", _criar_icone(), "RememberME", menu)
    _icone.run()


def parar() -> None:
    """Tira o icone da bandeja e desbloqueia o `arrancar()`."""
    _icone.stop()
