import pandas as pd
import os
import csv

# ================================
# Pastas
# ================================
INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

# ================================
# Processamento do arquivo
# ================================
def processar_arquivo(caminho_excel=None):

    # Define arquivo de entrada
    if caminho_excel:
        arquivo_excel = caminho_excel
    else:
        if not os.path.isdir(INPUT_FOLDER):
            print(f"Pasta de input não encontrada: {INPUT_FOLDER}")
            return

        arquivo_excel = None
        for file in os.listdir(INPUT_FOLDER):
            if file.lower().endswith((".xls", ".xlsx")):
                arquivo_excel = os.path.join(INPUT_FOLDER, file)
                break

        if not arquivo_excel:
            print("Nenhum arquivo XLS/XLSX encontrado na pasta input/")
            return

    # Leitura do Excel
    df = pd.read_excel(
        arquivo_excel,
        dtype=str,
        header=None,
        keep_default_na=False,
        skiprows=2
    )

    # ================================
    # Mapeamento parcial
    # ================================

    # Campo 01 → vazio
    col1 = pd.Series([""] * len(df))

    # Campo 02 → vazio
    col2 = pd.Series([""] * len(df))

    # Campo 03 → campo 18
    col3 = df[17].astype(str)

    # Campo 04 → vazio
    col4 = pd.Series([""] * len(df))

    # Campo 05 → campo02
    col5 = df[1].astype(str)

    # Campo 06 → fixo "RUA"
    col6 = pd.Series(["RUA"] * len(df))

    # Campo 07 → coluna 24 + espaço + coluna 25
    col7 = (
        df[23].astype(str).str.strip()
        + " "
        + df[24].astype(str).str.strip()
    ).str.strip()

    # Campo 08 → coluna 27
    col8 = df[26].astype(str)

    # Campo 09 → coluna 28
    col9 = df[27].astype(str)

    # Campo 10 → vazio
    col10 = pd.Series([""] * len(df))

    # Campo 11 → coluna 22
    col11 = df[21].astype(str)

    # Campo 12 → coluna 23
    col12 = df[22].astype(str)

    # Campo 13 → vazio
    col13 = pd.Series([""] * len(df))

    # Campo 14 → vazio
    col14 = pd.Series([""] * len(df))

    # Campo 15 → coluna 03
    col15 = df[2].astype(str)

    # Campo 16 → vazio
    col16 = pd.Series([""] * len(df))

    # Campo 17 → fixo "N"
    col17 = pd.Series(["N"] * len(df))



    # DataFrame final com 31 colunas
    df_final = pd.DataFrame({
        1: col1,
        2: col2,
        3: col3,
        4: col4,
        5: col5,
        6: col6,
        7: col7,
        8: col8,
        9: col9,
        10: col10,
        11: col11,
        12: col12,
        13: col13,
        14: col14,
        15: col15,
        16: col16,
        17: col17,
        #**extras
    })

    # Nome do arquivo de saída
    pasta_saida = os.path.dirname(arquivo_excel)
    nome_base = os.path.splitext(os.path.basename(arquivo_excel))[0]
    output_path = os.path.join(pasta_saida, f"{nome_base}_SCI.txt")

    print(df_final[[10, 11]].head())


    # Geração do TXT
    df_final.to_csv(
        output_path,
        sep=",",
        index=False,
        header=False,
        quoting=csv.QUOTE_NONE,
        escapechar="\\"
    )

    print(f"Arquivo gerado com sucesso: {output_path}")


if __name__ == "__main__":
    processar_arquivo()
