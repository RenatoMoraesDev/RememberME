"""Contrato de dados entre todos os modulos."""

from dataclasses import dataclass
from typing import Optional

#: A posicao no tuplo e' o que se guarda na base de dados.
DIAS = ("seg", "ter", "qua", "qui", "sex", "sab", "dom")

#: A janela de tempo é FECHADA nos dois extremos: `08:00-14:00` inclui as 14:00.
JANELA_FIM_INCLUSIVO = True


@dataclass
class Lembrete:
    """Um lembrete.

    Há dois tipos, e distinguem-se por um campo estar preenchido ou não:

    - **hora fixa (RF01)** - `hora` preenchida, tudo o resto da janela a None.
      Dispara uma vez por dia, aquela hora.
    - **recorrente numa janela (RF02)** - `hora` a None, e `janela_inicio`,
      `janela_fim` e `intervalo_min` preenchidos. Dispara de `intervalo_min` em
      `intervalo_min` minutos, dentro da janela.

    Nao há campo `tipo`: o tipo lê-se do que está preenchido.
    """

    texto: str
    hora: Optional[str] = None
    janela_inicio: Optional[str] = None
    janela_fim: Optional[str] = None
    intervalo_min: Optional[int] = None
    dias_semana: str = ",".join(DIAS)
    ativo: bool = True
    id: Optional[int] = None  # None enquanto nao foi gravado

    @property
    def e_hora_fixa(self) -> bool:
        return self.hora is not None

    def dias(self) -> list[str]:
        return [d for d in self.dias_semana.split(",") if d]
