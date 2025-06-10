import pandas
import os


def load_csvs_from_folder(folder_path="data"):
    """
    Carrega todos os CSVs de uma pasta e retorna um dict {filename: DataFrame}.
    Se algo der errado, retorna a string "ERROR".
    """
    csv_data = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                path = os.path.join(folder_path, filename)
                df = pandas.read_csv(path)
                csv_data[filename] = df
        return csv_data
    except Exception as e:
        print("Erro ao carregar CSVs:", e)
        return "ERROR"


def build_metadata(csv_data: dict) -> dict:
    """
    Gera um dicionário de metadados para cada CSV:
      - número de linhas e colunas
      - tipos de cada coluna
      - estatísticas descritivas
      - top-5 valores mais frequentes em colunas categóricas
    """
    meta = {}
    for name, df in csv_data.items():
        meta[name] = {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "dtypes": df.dtypes.apply(lambda dt: dt.name).to_dict(),
            "stats": df.describe(include="all").to_dict(),
            "top_values": {
                col: df[col].value_counts().head(5).to_dict()
                for col in df.select_dtypes(include=["object", "category"]).columns
            },
        }
    return meta


def mount_nfe(csv_data: dict) -> dict:
    """
    Monta a estrutura final da NFe a partir dos dados CSV.
    """
    nfes = {}
    heads = None
    items = None

    # Preencher as informações da NFe
    for name, df in csv_data.items():
        if name == "202401_NFs_Cabecalho.csv":
            heads = df
        if name == "202401_NFs_Itens.csv":
            items = df

    if heads is not None:
        head_records = heads.to_dict(orient="records")[:5]  # Limit to 2 heads
        for record in head_records:
            chave = record.get("CHAVE DE ACESSO")
            if chave is not None:
                nfes[chave] = {
                    "head": record,
                    "items": [],
                }

    if items is not None:
        from collections import defaultdict

        items_by_chave = defaultdict(list)

        for record in items.to_dict(orient="records"):
            chave = record.get("CHAVE DE ACESSO")
            if chave in nfes:
                items_by_chave[chave].append(record)

        for chave, item_list in items_by_chave.items():
            nfes[chave]["items"] = item_list[:5]

    return nfes
