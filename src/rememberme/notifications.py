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


def popup_canto(mensagem: str, titulo: str = TITULO, duracao_ms: int = 8000) -> None:
    """Janelinha sem moldura no canto inferior direito do ecra, tipo balao.

    Fecha sozinha ao fim de `duracao_ms`, ou ao clicar nela.
    """
    import tkinter as tk

    janela = tk.Tk()
    janela.withdraw()  # evita um instante da janela por defeito antes de posicionar
    janela.overrideredirect(True)
    janela.attributes("-topmost", True)

    largura, altura = 300, 110
    x = janela.winfo_screenwidth() - largura - 20
    y = janela.winfo_screenheight() - altura - 60
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

    fundo = tk.Frame(janela, bg="#2d7ff9", padx=12, pady=10)
    fundo.pack(fill="both", expand=True)
    tk.Label(
        fundo, text=titulo, bg="#2d7ff9", fg="white", font=("Segoe UI", 10, "bold"), anchor="w"
    ).pack(fill="x")
    tk.Label(
        fundo, text=mensagem, bg="#2d7ff9", fg="white", wraplength=270, justify="left", anchor="w"
    ).pack(fill="x", pady=(6, 0))

    janela.bind("<Button-1>", lambda _evento: janela.destroy())
    janela.after(duracao_ms, janela.destroy)
    janela.deiconify()
    janela.mainloop()

