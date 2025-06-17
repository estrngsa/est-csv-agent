from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def build_vector_index(csv_data: dict, persist_directory: str = "db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    texts, metadatas, ids = [], [], []
    for chave, nfe in csv_data.items():
        head = nfe.get("head", {})

        if head:
            text = " | ".join(f"{k}: {v}" for k, v in head.items())
            texts.append(text)
            metadatas.append({"chave": chave, "type": "head"})
            ids.append(f"{chave}-head")

        for idx, item in enumerate(nfe.get("items", [])):
            item_text = " | ".join(f"{k}: {v}" for k, v in item.items())
            texts.append(item_text)
            metadatas.append({"chave": chave, "type": "item", "item_idx": idx})
            ids.append(f"{chave}-item-{idx}")

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        ids=ids,
        persist_directory=persist_directory,
        collection_name="csv_collection",
    )

    return vectordb


def query_vector_index(vectordb, question: str, k: int = 5):
    results = vectordb.similarity_search(question, k=k)

    return results
