from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


def build_vector_index(csv_data: dict, persist_directory: str = "db"):
    """
    Lê todos os CSVs (cada linha vira um documento), gera embeddings e
    constrói um índice Chroma persistido em disco.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    texts, metadatas, ids = [], [], []
    for filename, df in csv_data.items():
        for idx, row in df.iterrows():
            text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
            texts.append(text)
            metadatas.append({"filename": filename, "row": idx})
            ids.append(f"{filename}-{idx}")

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        ids=ids,
        persist_directory=persist_directory,
        collection_name="csv_collection",
    )
    vectordb.persist()
    return vectordb


def query_vector_index(vectordb, question: str, k: int = 5):
    """
    Recebe o objeto Chroma e uma pergunta, retorna os k docs mais similares.
    Cada doc é um objeto com .page_content e .metadata.
    """
    results = vectordb.similarity_search(question, k=k)

    return results
