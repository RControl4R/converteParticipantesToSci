import os
import sys

# ==============================
# VALIDAÇÃO DE PARÂMETRO
# ==============================

if len(sys.argv) < 2:
    print("Uso correto:")
    print("python converteParticipantes.py <arquivo_entrada.txt>")
    sys.exit(1)

ARQUIVO_ENTRADA = sys.argv[1]

if not os.path.isfile(ARQUIVO_ENTRADA):
    print(f"Erro: arquivo não encontrado -> {ARQUIVO_ENTRADA}")
    sys.exit(1)

SEPARADOR = ","

# ==============================
# FUNÇÕES
# ==============================

def limpar(valor):
    return valor.replace('"', '').strip()

def campo(campos, posicao):
    try:
        return limpar(campos[posicao - 1])
    except IndexError:
        return ""

# ==============================
# LEITURA DO ARQUIVO
# ==============================

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
    linhas = f.readlines()

# ==============================
# PROCESSAMENTO
# ==============================

registros_saida = []

for linha in linhas:
    linha = linha.strip()

    if not linha:
        continue

    campos = linha.split(SEPARADOR)

    # Garante 31 colunas
    if len(campos) < 31:
        campos.extend([""] * (31 - len(campos)))

    saida = [
        "",                                     # 01
        "",                                     # 02
        campo(campos, 3),                       # 03
        "",                                     # 04
        campo(campos, 2),                       # 05
        campo(campos, 14),                      # 06
        f"{campo(campos,15)} {campo(campos,16)}",  # 07
        f"Bairro {campo(campos,18)}",           # 08
        campo(campos, 19),                      # 09
        campo(campos, 31),                      # 10
        campo(campos, 10),                      # 11
        campo(campos, 5),                       # 12
        "",                                     # 13
        "",                                     # 14
        campo(campos, 4),                       # 15
        "",                                     # 16
        "N",                                    # 17
        "20000101",                             # 18
        "",                                     # 19
        "",                                     # 20
        campo(campos, 28),                      # 21
        campo(campos, 27),                      # 22
        "",                                     # 23
        "",                                     # 24
        "S",                                    # 25
        "",                                     # 26
        "1"                                     # 27
    ]

    registros_saida.append(SEPARADOR.join(saida))

# ==============================
# GRAVAÇÃO DO ARQUIVO DE SAÍDA
# ==============================

nome_base, _ = os.path.splitext(ARQUIVO_ENTRADA)
arquivo_saida = f"{nome_base}_SCI.txt"

with open(arquivo_saida, "w", encoding="utf-8", newline="\r\n") as f:
    for linha in registros_saida:
        f.write(linha + "\n")

print("Conversão concluída com sucesso!")
print(f"Arquivo gerado: {arquivo_saida}")
