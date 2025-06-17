import pandas
import os


def load_csvs_from_folder(folder_path="data"):
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


def build_metadata2(csv_data: dict) -> dict:
    meta = {}
    first_nfe = next(iter(csv_data.values()), None)

    if first_nfe:
        head = first_nfe.get("head", {})
        items = first_nfe.get("items", [])
        head_fields_with_type = [(k, type(v).__name__) for k, v in head.items()]
        if items:
            item_fields_with_type = [(k, type(v).__name__) for k, v in items[0].items()]
        else:
            item_fields_with_type = []
    else:
        head_fields_with_type = []
        item_fields_with_type = []

    num_nfes = len(csv_data)
    items_counts = [len(nfe.get("items", [])) for nfe in csv_data.values()]
    avg_items_per_nfe = sum(items_counts) / num_nfes if num_nfes > 0 else 0

    from datetime import datetime

    dates = []
    for nfe in csv_data.values():
        date_str = nfe.get("head", {}).get("DATA EMISSÃO")
        if date_str:
            for fmt in (
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%m/%d/%Y %I:%M:%S %p",
                "%m/%d/%Y %H:%M:%S",
                "%m/%d/%Y %I:%M:%S %p",
            ):
                try:
                    dates.append(datetime.strptime(date_str.strip(), fmt))
                    break
                except Exception:
                    continue
            else:
                try:
                    import pandas as pd

                    dt = pd.to_datetime(date_str, errors="coerce")
                    if pd.notnull(dt):
                        dates.append(dt.to_pydatetime())
                except Exception:
                    pass
    date_range = (
        (min(dates).strftime("%Y-%m-%d"), max(dates).strftime("%Y-%m-%d"))
        if dates
        else (None, None)
    )

    max_invoice_value = None
    max_invoice_chave = None

    for chave, nfe in csv_data.items():
        head = nfe.get("head", {})
        valor = head.get("VALOR NOTA FISCAL")

        if valor is not None:
            try:
                valor_num = float(valor)
            except Exception:
                continue
            if (max_invoice_value is None) or (valor_num > max_invoice_value):
                max_invoice_value = valor_num
                max_invoice_chave = chave

    meta["head_fields_with_type"] = head_fields_with_type
    meta["item_fields_with_type"] = item_fields_with_type
    meta["avg_items_per_nfe"] = avg_items_per_nfe
    meta["max_invoice_value"] = max_invoice_value
    meta["max_invoice_chave"] = max_invoice_chave
    meta["date_range"] = date_range
    meta["num_nfes"] = num_nfes

    return meta


def mount_nfe(csv_data: dict) -> dict:
    nfes = {}
    heads = None
    items = None

    for name, df in csv_data.items():
        if name == "202401_NFs_Cabecalho.csv":
            heads = df
        if name == "202401_NFs_Itens.csv":
            items = df

    if heads is not None:
        head_records = heads.to_dict(orient="records")
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
            nfes[chave]["items"] = item_list

    return nfes
