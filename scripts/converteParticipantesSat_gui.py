# ------------------------
# importações
# ------------------------

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import time
import sys

from converteParticipantes import processar_arquivo

VERSAO = "1.2"

# ==============================
# FUNÇÃO PARA RECURSOS (EXE)
# ==============================

def caminho_recurso(relativo):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relativo)

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

        # Atualiza rodapé
        rodape_var.set(f"Versão {VERSAO} | Último arquivo: {nome_arquivo}")

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

# -----------------------------
# Conteúdo principal
# -----------------------------
conteudo_frame = tk.Frame(janela, bg=COR_FUNDO)
conteudo_frame.pack(fill="both", expand=True)

label = tk.Label(
    conteudo_frame,
    text="Conversão Participantes → SCI\n\n"
         "Selecione o arquivo .txt de origem",
    font=FONTE_PADRAO,
    justify="center",
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
label.pack(pady=20)

btn = tk.Button(
    conteudo_frame,
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
btn.pack(pady=10)

# -----------------------------
# Rodapé
# -----------------------------
rodape_frame = tk.Frame(janela, bg=COR_FUNDO)
rodape_frame.pack(side="bottom", fill="x")

rodape_var = tk.StringVar()
rodape_var.set(f"Versão {VERSAO}")

rodape = tk.Label(
    rodape_frame,
    textvariable=rodape_var,
    font=FONTE_RODAPE,
    fg="gray",
    bg=COR_FUNDO,
    anchor="e"
)
rodape.pack(pady=6, padx=10, fill="x")


print(caminho_recurso("logo.png"))

janela.mainloop()
