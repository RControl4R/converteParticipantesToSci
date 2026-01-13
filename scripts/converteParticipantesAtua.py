import pandas as pd
import os
import csv

# ================================
# Pastas
# ================================
INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

# ================================
# Funções auxiliares  
# ================================
def formatar_data(valor):
    if valor is None or str(valor).strip() == "":
        return ""
    valor = str(valor).strip()
    
    # yyyy-mm-dd ou yyyy-mm-dd hh:mm:ss
    if "-" in valor and len(valor.split("-")[0]) == 4:
        try:
            data = valor.split(" ")[0]  # remove hora
            ano, mes, dia = data.split("-")
            return f"{ano}{mes}{dia}"
        except:
            pass

    # dd/mm/yyyy
    if "/" in valor:
        try:
            dia, mes, ano = valor.split("/")
            return f"{ano}{mes}{dia}"
        except:
            pass

    # número serial do Excel
    try:
        numero = float(valor)
        data = pd.to_datetime(numero, unit="D", origin="1899-12-30")
        return data.strftime("%Y%m%d")
    except:
        pass

    return valor

CAMPOS_COM_ASPAS = {
    3, 5, 6, 7, 8, 9,
    11, 12, 13, 14, 15, 16,
    17, 18, 19, 20, 24, 25, 26
}

# ================================
def colocar_aspas(valor):
    if valor is None or str(valor) == "":
        return "\"\""
    return f"\"{valor}\""


# ================================
# Normalização de texto
# ================================
def normalizar(texto):
    if texto is None:
        return ""
    return (
        str(texto)
        .strip()
        .upper()
        .replace("Á","A")
        .replace("É","E")
        .replace("Í","I")
        .replace("Ó","O")
        .replace("Ú","U")
        .replace("Ã","A")
        .replace("Õ","O")
        .replace("Â","A")
        .replace("Ê","E")
        .replace("Ô","O")
        .replace("Ç","C")
    )

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

    df_ibge = pd.read_csv("../input/ibge_municipios.csv", dtype=str, sep=";", encoding="latin-1")

    # Normaliza cidade e UF vindos do Excel
    df["CIDADE_NORM"] = df[12].apply(normalizar)  
    df["UF_NORM"] = df[13].apply(normalizar)      

    # Normaliza tabela IBGE
    df_ibge["CIDADE_NORM"] = df_ibge["MUNICIPIO_IBGE"].apply(normalizar)
    df_ibge["UF_NORM"] = df_ibge["UF"].apply(normalizar)

    mapa_ibge = (
        df_ibge
        .drop_duplicates(subset=["CIDADE_NORM", "UF_NORM"])
        .set_index(["CIDADE_NORM", "UF_NORM"])["CODIGO_MUNICIPIO_IBGE"]
        .to_dict()
    )


    # ================================
    # Mapeamento de campos
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

    # Campo 11 → coluna 22
    col11 = df[21].astype(str)

    # Campo 12 → coluna 23
    col12 = df[22].astype(str)

    # Campo 10 → código IBGE (usando cidade + UF da SAÍDA)
    cidade_norm = col11.apply(normalizar)
    uf_norm = col12.apply(normalizar)

    col10 = [
        mapa_ibge.get((c, u), "")
        for c, u in zip(cidade_norm, uf_norm)
    ]
    col10 = pd.Series(col10)


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

    # Campo 18 → coluna 12
    col18 = df[11].apply(formatar_data)

    # Campo 19 → vazio
    col19 = pd.Series([""] * len(df))

    # Campo 20 → vazio
    col20 = pd.Series([""] * len(df))

    # Campo 21 → fixo "0"
    col21 = pd.Series(["0"] * len(df))

    # Campo 22 → fixo "2"
    col22 = pd.Series(["2"] * len(df))

    # Campo 23 → vazio
    col23 = pd.Series([""] * len(df))

    # Campo 24 → fixo "S"
    col24 = pd.Series(["S"] * len(df))

    # Campo 25 → vazio
    col25 = pd.Series([""] * len(df))

    # Campo 26 → fixo "1"
    col26 = pd.Series(["1"] * len(df))


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
        18: col18,
        19: col19,
        20: col20,
        21: col21,
        22: col22,
        23: col23,
        24: col24,
        25: col25,
        26: col26,
        #**extras
    })

    # ----------------------------
    # Aplicação de aspas
    # ----------------------------
    for campo in CAMPOS_COM_ASPAS:
        df_final[campo] = df_final[campo].apply(colocar_aspas)

    # Nome do arquivo de saída
    pasta_saida = os.path.dirname(arquivo_excel)
    nome_base = os.path.splitext(os.path.basename(arquivo_excel))[0]
    output_path = os.path.join(pasta_saida, f"{nome_base}_SCI.txt")


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
