"""O que o `python -m rememberme` executa.

Existe para o programa poder correr sem estar instalado - util em aula e para
depurar. Quando esta' instalado, o comando `rememberme` faz o mesmo por outro
caminho (ver [project.scripts] no pyproject.toml).
"""

from rememberme.cli import app

app()
