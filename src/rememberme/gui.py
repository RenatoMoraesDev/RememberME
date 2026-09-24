"""GUI minima em Tkinter para gerir lembretes.

Nao substitui a CLI nem o tray: e' so' uma janela simples para criar, ver,
ativar/desativar e apagar lembretes, usando o mesmo `storage`.
"""

import tkinter as tk
import ctypes
from tkinter import messagebox, ttk

from rememberme import app as aplicacao
from rememberme import storage
from rememberme.models import DIAS, Lembrete


_mutex = None


def _gui_ja_aberta() -> bool:
    global _mutex

    _mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "RememberME-GUI")
    return ctypes.windll.kernel32.GetLastError() == 183


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RememberME")
        self.geometry("560x520")
        self.minsize(560, 480)

        self.id_em_edicao = None

        self._construir_formulario()
        self._construir_controlo()
        self._construir_lista()
        self.atualizar_lista()

    # formulario para criar lembretes

    def _construir_formulario(self):
        moldura = ttk.Frame(self, padding=10)
        moldura.pack(fill="x")

        ttk.Label(moldura, text="Texto:").grid(row=0, column=0, sticky="w")
        self.campo_texto = ttk.Entry(moldura, width=30)
        self.campo_texto.grid(row=0, column=1, columnspan=3, sticky="we", padx=5)

        ttk.Label(moldura, text="Hora fixa (HH:MM):").grid(row=1, column=0, sticky="w")
        self.campo_hora = ttk.Entry(moldura, width=10)
        self.campo_hora.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(moldura, text="Entre: inicio").grid(row=2, column=0, sticky="w")
        self.campo_janela_inicio = ttk.Entry(moldura, width=10)
        self.campo_janela_inicio.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(moldura, text="fim").grid(row=2, column=2, sticky="w")
        self.campo_janela_fim = ttk.Entry(moldura, width=10)
        self.campo_janela_fim.grid(row=2, column=3, sticky="w", padx=5)

        ttk.Label(moldura, text="a cada (min)").grid(row=3, column=0, sticky="w")
        self.campo_intervalo = ttk.Entry(moldura, width=10)
        self.campo_intervalo.grid(row=3, column=1, sticky="w", padx=5)

        ttk.Label(moldura, text="Tipo de aviso:").grid(row=4, column=0, sticky="w")
        self.campo_accao = ttk.Combobox(
            moldura,
            values=["Popup (janela visivel)"],
            state="readonly",
            width=25,
        )
        self.campo_accao.current(0)
        self.campo_accao.grid(row=4, column=1, columnspan=2, sticky="w", padx=5)

        self.botao_guardar = ttk.Button(moldura, text="Adicionar", command=self.guardar)
        self.botao_guardar.grid(row=5, column=0, columnspan=13, pady=8, sticky="we")
        self.botao_cancelar = ttk.Button(
            moldura, text="Cancelar edicao", command=self.cancelar_edicao
        )

        moldura.columnconfigure(1, weight=1)

    # iniciar/parar o agendador em segundo plano

    def _construir_controlo(self):
        moldura = ttk.Frame(self, padding=(10, 0, 10, 10))
        moldura.pack(fill="x")

        ttk.Button(moldura, text="Iniciar", command=self.iniciar).pack(side="left")
        ttk.Button(moldura, text="Parar", command=self.parar).pack(side="left", padx=5)

    # lista de lembretes existentes

    def _construir_lista(self):
        # botoes primeiro e fixos em baixo, para nao ficarem cortados quando a lista cresce
        botoes = ttk.Frame(self, padding=(10, 0, 10, 10))
        botoes.pack(side="bottom", fill="x")
        ttk.Button(botoes, text="Editar", command=self.carregar_para_edicao).pack(side="left")
        ttk.Button(botoes, text="Ativar/Desativar", command=self.alternar_ativo).pack(
            side="left", padx=5
        )
        ttk.Button(botoes, text="Apagar", command=self.apagar).pack(side="left")
        ttk.Button(botoes, text="Atualizar lista", command=self.atualizar_lista).pack(
            side="left", padx=5
        )

        moldura = ttk.Frame(self, padding=10)
        moldura.pack(fill="both", expand=True)

        colunas = ("id", "texto", "agenda", "ativo")
        self.tabela = ttk.Treeview(moldura, columns=colunas, show="headings")
        for coluna, titulo in zip(colunas, ("ID", "Texto", "Agenda", "Ativo")):
            self.tabela.heading(coluna, text=titulo)
        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("ativo", width=60, anchor="center")
        self.tabela.pack(fill="both", expand=True)

    # acoes

    def guardar(self):
        texto = self.campo_texto.get().strip()
        hora = self.campo_hora.get().strip() or None
        janela_inicio = self.campo_janela_inicio.get().strip() or None
        janela_fim = self.campo_janela_fim.get().strip() or None
        intervalo = self.campo_intervalo.get().strip() or None

        if not texto:
            messagebox.showerror("Erro", "Indique o texto do lembrete.")
            return

        if hora and (janela_inicio or janela_fim):
            messagebox.showerror("Erro", "Use hora fixa OU janela, nao os dois.")
            return

        if not hora and not (janela_inicio and janela_fim and intervalo):
            messagebox.showerror(
                "Erro", "Indique uma hora fixa, ou janela completa com intervalo."
            )
            return

        #: o agendador nao suporta uma janela que atravesse a meia-noite (ex: 23:00-01:00)
        if janela_inicio and janela_fim and janela_inicio >= janela_fim:
            messagebox.showerror(
                "Erro", "A janela nao pode atravessar a meia-noite: o inicio tem de ser antes do fim."
            )
            return

        accao = "popup" if self.campo_accao.get().startswith("Popup") else "notificacao"

        if self.id_em_edicao is None:
            lembrete = Lembrete(
                texto=texto,
                hora=hora,
                janela_inicio=janela_inicio,
                janela_fim=janela_fim,
                intervalo_min=int(intervalo) if intervalo else None,
                dias_semana=",".join(DIAS),
                accao=accao,
                accao_param=texto,
            )
            storage.criar(lembrete)
        else:
            lembrete = storage.obter(self.id_em_edicao)
            lembrete.texto = texto
            lembrete.hora = hora
            lembrete.janela_inicio = janela_inicio
            lembrete.janela_fim = janela_fim
            lembrete.intervalo_min = int(intervalo) if intervalo else None
            lembrete.accao = accao
            lembrete.accao_param = texto
            storage.atualizar(lembrete)
            self.cancelar_edicao()

        self.campo_texto.delete(0, "end")
        self.campo_hora.delete(0, "end")
        self.campo_janela_inicio.delete(0, "end")
        self.campo_janela_fim.delete(0, "end")
        self.campo_intervalo.delete(0, "end")
        self.campo_accao.current(0)

        self.atualizar_lista()

    def carregar_para_edicao(self):
        id_ = self._id_selecionado()
        if id_ is None:
            return
        lembrete = storage.obter(id_)
        if lembrete is None:
            return

        self.campo_texto.delete(0, "end")
        self.campo_texto.insert(0, lembrete.texto)
        self.campo_hora.delete(0, "end")
        self.campo_hora.insert(0, lembrete.hora or "")
        self.campo_janela_inicio.delete(0, "end")
        self.campo_janela_inicio.insert(0, lembrete.janela_inicio or "")
        self.campo_janela_fim.delete(0, "end")
        self.campo_janela_fim.insert(0, lembrete.janela_fim or "")
        self.campo_intervalo.delete(0, "end")
        self.campo_intervalo.insert(0, str(lembrete.intervalo_min or ""))
        self.campo_accao.current(1 if lembrete.accao == "popup" else 0)

        self.id_em_edicao = id_
        self.botao_guardar.config(text=f"Guardar edicao (ID {id_})")
        self.botao_cancelar.grid(row=6, column=0, columnspan=4, sticky="we")

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.botao_guardar.config(text="Adicionar")
        self.botao_cancelar.grid_forget()

    def atualizar_lista(self):
        self.tabela.delete(*self.tabela.get_children())
        for lembrete in storage.listar():
            if lembrete.e_hora_fixa:
                agenda = lembrete.hora
            else:
                agenda = (
                    f"{lembrete.janela_inicio}-{lembrete.janela_fim}"
                    f" ({lembrete.intervalo_min} min)"
                )
            self.tabela.insert(
                "",
                "end",
                iid=str(lembrete.id),
                values=(lembrete.id, lembrete.texto, agenda, "sim" if lembrete.ativo else "nao"),
            )

    def _id_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showinfo("Aviso", "Selecione um lembrete na lista.")
            return None
        return int(selecao[0])

    def alternar_ativo(self):
        id_ = self._id_selecionado()
        if id_ is None:
            return
        lembrete = storage.obter(id_)
        if lembrete is None:
            return
        lembrete.ativo = not lembrete.ativo
        storage.atualizar(lembrete)
        self.atualizar_lista()

    def apagar(self):
        id_ = self._id_selecionado()
        if id_ is None:
            return
        if messagebox.askyesno("Confirmar", f"Apagar o lembrete {id_}?"):
            storage.apagar(id_)
            if self.id_em_edicao == id_:
                self.cancelar_edicao()
            self.atualizar_lista()

    def iniciar(self):
        if aplicacao.servico_ativo():
            messagebox.showinfo("RememberME", "O agendador ja esta a correr.")
            return
        aplicacao.arrancar_em_segundo_plano()
        messagebox.showinfo("RememberME", "Agendador iniciado em segundo plano.")

    def parar(self):
        if not aplicacao.servico_ativo():
            messagebox.showinfo("RememberME", "O agendador nao esta a correr.")
            return
        aplicacao.pedir_paragem()
        messagebox.showinfo("RememberME", "Pedido de paragem enviado.")


def arrancar() -> None:
    """Ponto de entrada da GUI."""
    if _gui_ja_aberta():
        return
    JanelaPrincipal().mainloop()


if __name__ == "__main__":
    arrancar()
