# ------------------------
# importações
# ------------------------

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import time

from converteParticipantes import processar_arquivo

VERSAO = "1.2"

# ==============================
# TEMA CORPORATIVO
# ==============================

COR_FUNDO = "#f2f2f2"
COR_BOTAO = "#1f6aa5"
COR_BOTAO_ATIVO = "#155a8a"
COR_TEXTO = "#000000"

FONTE_PADRAO = ("Segoe UI", 11)
FONTE_TITULO = ("Segoe UI", 11, "bold")
FONTE_RODAPE = ("Segoe UI", 9)

# ==============================
# SPLASH SCREEN
# ==============================

def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg=COR_FUNDO)

    largura = 360
    altura = 160
    x = (splash.winfo_screenwidth() // 2) - (largura // 2)
    y = (splash.winfo_screenheight() // 2) - (altura // 2)
    splash.geometry(f"{largura}x{altura}+{x}+{y}")

    tk.Label(
        splash,
        text="Conversor Participantes → SCI",
        font=("Segoe UI", 12, "bold"),
        bg=COR_FUNDO
        ).pack(pady=(30, 5))

    tk.Label(
        splash,
        text=f"Versão {VERSAO}",
        font=("Segoe UI", 9),
        fg="gray",
        bg=COR_FUNDO
        ).pack(pady=(0, 15))

    tk.Label(
        splash,
        text="Inicializando aplicação...",
        font=("Segoe UI", 10),
        bg=COR_FUNDO
        ).pack()


    splash.update()
    time.sleep(2)
    splash.destroy()

# ==============================
# PROCESSAMENTO EM THREAD
# ==============================

def executar_conversao(caminho):
    try:
        arquivo_saida = processar_arquivo(caminho)

        nome_arquivo = os.path.basename(arquivo_saida)

        resposta = messagebox.askyesno(
            "Conversão concluída",
            f"Arquivo processado com sucesso!\n\n"
            f"Arquivo gerado:\n{nome_arquivo}\n\n"
            f"Deseja converter outro arquivo?"
        )

        if resposta:
            selecionar_arquivo()
        else:
            janela.quit()

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# ==============================
# SELEÇÃO DE ARQUIVO
# ==============================

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        initialdir=os.path.expanduser("~"),
        filetypes=[
            ("Arquivos TXT", "*.txt"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if not arquivo:
        return

    thread = threading.Thread(
        target=executar_conversao,
        args=(arquivo,),
        daemon=True
    )
    thread.start()

# ==============================
# JANELA PRINCIPAL
# ==============================

splash_screen()

janela = tk.Tk()
janela.title("Conversor Participantes → SCI")
janela.geometry("460x260")
janela.resizable(False, False)
janela.configure(bg=COR_FUNDO)

label = tk.Label(
    janela,
    text="Conversão Participantes → SCI\n\n"
         "Selecione o arquivo .txt de origem",
    font=FONTE_PADRAO,
    justify="center",
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
label.pack(pady=25)

btn = tk.Button(
    janela,
    text="Selecionar arquivo TXT",
    command=selecionar_arquivo,
    font=FONTE_TITULO,
    width=30,
    height=2,
    bg=COR_BOTAO,
    fg="white",
    activebackground=COR_BOTAO_ATIVO,
    relief="flat",
    cursor="hand2"
)
btn.pack(pady=20)

# -----------------------------
# Rodapé
# -----------------------------
rodape_frame = tk.Frame(janela, bg=COR_FUNDO)
rodape_frame.pack(side="bottom", fill="x")

rodape = tk.Label(
    rodape_frame,
    text=f"Versão {VERSAO}",
    font=FONTE_RODAPE,
    fg="gray",
    bg=COR_FUNDO
)
rodape.pack(pady=6)
rodape.pack(anchor="e", padx=10)

janela.mainloop()
