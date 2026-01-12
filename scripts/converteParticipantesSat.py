import os
import sys

SEPARADOR_ENTRADA = ";"
SEPARADOR_SAIDA = ","

# Campos da saída que DEVEM ter aspas (1-based)
CAMPOS_COM_ASPAS = {
    3, 5, 6, 7, 8, 9,
    11, 12, 13, 14, 15, 16,
    17, 18, 19, 20, 24, 25, 26
}

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def limpar(valor):
    return valor.replace('"', '').strip()

def campo(campos, posicao):
    try:
        return limpar(campos[posicao - 1])
    except IndexError:
        return ""

def formatar_saida(valores):
    resultado = []
    for i, valor in enumerate(valores, start=1):
        if i in CAMPOS_COM_ASPAS:
            resultado.append(f'"{valor}"')
        else:
            resultado.append(valor)
    return SEPARADOR_SAIDA.join(resultado)

# ==============================
# FUNÇÃO PRINCIPAL (Importar no _GUI)
# ==============================

def processar_arquivo(arquivo_entrada):
    if not os.path.isfile(arquivo_entrada):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_entrada}")

    with open(arquivo_entrada, "r", encoding="latin-1", errors="replace") as f:
        linhas = f.readlines()

    registros_saida = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        campos = linha.split(SEPARADOR_ENTRADA)

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
            "0",                                    # 21
            campo(campos, 27),                      # 22
            "",                                     # 23
            "",                                     # 24
            "S",                                    # 25
            "",                                     # 26
            "1"                                     # 27
        ]

        registros_saida.append(formatar_saida(saida))

    nome_base, _ = os.path.splitext(arquivo_entrada)
    arquivo_saida = f"{nome_base}_SCI.txt"

    with open(arquivo_saida, "w", encoding="utf-8", newline="\r\n") as f:
        for linha in registros_saida:
            f.write(linha + "\n")

    return arquivo_saida

# ==============================
# EXECUÇÃO VIA LINHA DE COMANDO
# ==============================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso correto:")
        print("python converteParticipantes.py <arquivo_entrada.txt>")
        sys.exit(1)

    try:
        saida = processar_arquivo(sys.argv[1])
        print("Conversão concluída com sucesso!")
        print(f"Arquivo gerado: {saida}")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
