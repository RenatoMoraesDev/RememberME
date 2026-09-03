"""Leitura e escrita na base de dados SQLite.

A base de dados NAO vai para o repositorio: fica na pasta de dados do
utilizador, que o `typer.get_app_dir` devolve em Windows, macOS e Linux.
"""

import sqlite3
from pathlib import Path
from typing import Optional

import typer

from rememberme.models import Lembrete

ESQUEMA = """
CREATE TABLE IF NOT EXISTS lembrete (
    id            INTEGER PRIMARY KEY,
    texto         TEXT    NOT NULL,
    hora          TEXT,
    janela_inicio TEXT,
    janela_fim    TEXT,
    intervalo_min INTEGER,
    dias_semana   TEXT    NOT NULL,
    ativo         INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS estado (
    chave TEXT PRIMARY KEY,
    valor TEXT
);
"""

CAMPOS = (
    "id", "texto", "hora", "janela_inicio", "janela_fim",
    "intervalo_min", "dias_semana", "ativo",
)


def caminho_bd() -> Path:
    pasta = Path(typer.get_app_dir("RememberME"))
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta / "rememberme.db"


def ligar() -> sqlite3.Connection:
    """Abre a ligacao e garante que as tabelas existam."""
    con = sqlite3.connect(caminho_bd())
    con.row_factory = sqlite3.Row  # permite aceder as colunas pelo nome
    con.executescript(ESQUEMA)
    return con


def _para_lembrete(linha: sqlite3.Row) -> Lembrete:
    return Lembrete(
        id=linha["id"],
        texto=linha["texto"],
        hora=linha["hora"],
        janela_inicio=linha["janela_inicio"],
        janela_fim=linha["janela_fim"],
        intervalo_min=linha["intervalo_min"],
        dias_semana=linha["dias_semana"],
        ativo=bool(linha["ativo"]),
    )


# lembretes

def criar(lembrete: Lembrete) -> Lembrete:
    """Grava um lembrete novo e devolve-o com o `id` preenchido."""
    con = ligar()
    with con:
        cur = con.execute(
            "INSERT INTO lembrete (texto, hora, janela_inicio, janela_fim,"
            " intervalo_min, dias_semana, ativo) VALUES (?,?,?,?,?,?,?)",
            (lembrete.texto, lembrete.hora, lembrete.janela_inicio,
             lembrete.janela_fim, lembrete.intervalo_min,
             lembrete.dias_semana, int(lembrete.ativo)),
        )
    lembrete.id = cur.lastrowid
    return lembrete


def listar(apenas_ativos: bool = False) -> list[Lembrete]:
    sql = "SELECT * FROM lembrete"
    if apenas_ativos:
        sql += " WHERE ativo = 1"
    return [_para_lembrete(l) for l in ligar().execute(sql + " ORDER BY id")]


def obter(id: int) -> Optional[Lembrete]:
    linha = ligar().execute("SELECT * FROM lembrete WHERE id = ?", (id,)).fetchone()
    return _para_lembrete(linha) if linha else None


def atualizar(lembrete: Lembrete) -> None:
    con = ligar()
    with con:
        con.execute(
            "UPDATE lembrete SET texto=?, hora=?, janela_inicio=?, janela_fim=?,"
            " intervalo_min=?, dias_semana=?, ativo=? WHERE id=?",
            (lembrete.texto, lembrete.hora, lembrete.janela_inicio,
             lembrete.janela_fim, lembrete.intervalo_min,
             lembrete.dias_semana, int(lembrete.ativo), lembrete.id),
        )


def apagar(id: int) -> bool:
    """Devolve True se apagou alguma coisa."""
    con = ligar()
    with con:
        return con.execute("DELETE FROM lembrete WHERE id = ?", (id,)).rowcount > 0


# estado da aplicacao 

def guardar_estado(chave: str, valor: str) -> None:
    con = ligar()
    with con:
        con.execute(
            "INSERT INTO estado (chave, valor) VALUES (?,?)"
            " ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor",
            (chave, valor),
        )


def ler_estado(chave: str) -> Optional[str]:
    linha = ligar().execute(
        "SELECT valor FROM estado WHERE chave = ?", (chave,)
    ).fetchone()
    return linha["valor"] if linha else None
