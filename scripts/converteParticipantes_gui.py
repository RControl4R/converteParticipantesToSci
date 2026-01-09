# ------------------------
# importações
# ------------------------

import tkinter as tk
from tkinter import filedialog, messagebox
import os

# importa o script já existente
from converteParticipantes import processar_arquivo

VERSAO = "1.0"

def selecionar_arquivo():
    while True:
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

        try:
            processar_arquivo(arquivo)

            resposta = messagebox.askyesno(
                "Conversão concluída",
                "Arquivo processado com sucesso!\n\nDeseja converter outro arquivo?"
            )

            if not resposta:
                return

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao processar o arquivo:\n\n{str(e)}"
            )
            return

# -----------------------------
# Janela principal
# -----------------------------
janela = tk.Tk()
janela.title("Conversor Participantes → SCI")
janela.geometry("460x200")
janela.resizable(False, False)

label = tk.Label(
    janela,
    text="Conversão Participantes → SCI\n\n"
         "Selecione o arquivo TXT de origem",
    font=("Arial", 11),
    justify="center"
)
label.pack(pady=25)

btn = tk.Button(
    janela,
    text="Selecionar arquivo TXT",
    command=selecionar_arquivo,
    font=("Arial", 11),
    width=30,
    height=2
)
btn.pack(expand=True)

rodape = tk.Label(
    janela,
    text=f"Versão {VERSAO}",
    font=("Arial", 9),
    fg="gray"
)
rodape.pack(side="bottom", pady=8)

janela.mainloop()
