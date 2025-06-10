import pandas as pd
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
                df = pd.read_csv(path)
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
        print(f"Processing {name} with shape {df.shape}")
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


def filter_rows_by_keywords(question: str, csv_data: dict, max_rows: int = 5) -> dict:
    """
    Para cada DataFrame, encontra linhas que contenham qualquer uma das keywords
    extraídas de `question`. Se não achar nenhuma, retorna as primeiras `max_rows`.
    """
    # Extrai palavras de mais de 2 caracteres
    keywords = [w.strip() for w in question.lower().split() if len(w) > 2]
    filtered = {}

    for name, df in csv_data.items():
        # máscara booleana: True para linhas que contenham qualquer keyword
        mask = df.apply(
            lambda row: any(
                kw in str(val).lower() for val in row.values for kw in keywords
            ),
            axis=1,
        )
        subset = df[mask]
        # se vazio, pega head; senão head do subset
        if subset.empty:
            filtered[name] = df.head(max_rows).copy()
        else:
            filtered[name] = subset.head(max_rows).copy()

    return filtered
