from unidecode import unidecode
import zipfile
import tarfile
import tempfile
import os


def clean_input(text: str) -> str:
    return unidecode(text.strip())


def t(key, lang="pt") -> str:
    translations = {
        "title": {"pt": "📊 Agente Assistente de CSV", "en": "📊 CSV Assistant Agent"},
        "input_label": {
            "pt": "Pergunte algo sobre seus arquivos CSV...",
            "en": "Ask something about your CSV files...",
        },
        "error_csv": {
            "pt": "Não foi possível ler os arquivos CSV. Tente novamente mais tarde.",
            "en": "Could not read CSVs. Try again later.",
        },
        "error_key": {
            "pt": "Chave de API da OpenAI não encontrada. Verifique seu arquivo .env.",
            "en": "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.",
        },
        "response_label": {"pt": "Resposta:", "en": "Answer:"},
        "error_generic": {
            "pt": "Tente novamente mais tarde.",
            "en": "Try again later.",
        },
        "common_question_quantity": {
            "pt": "Qual item teve maior volume entregue (em quantidade)?",
            "en": "Which item had the highest delivered volume (in quantity)?",
        },
        "common_question_supplier": {
            "pt": "Qual é o fornecedor que teve maior montante recebido?",
            "en": "Which supplier received the highest amount?",
        },
        "loading_vectordb": {
            "pt": "Carregando banco de dados vetorial...",
            "en": "Loading vector database...",
        },
        "vectordb_ready": {
            "pt": "Banco de dados vetorial pronto!",
            "en": "Vector database ready!",
        },
        "quantity": {"pt": "maior volume", "en": "highest volume"},
        "amount": {"pt": "maior montante", "en": "highest amount"},
        "clear_history": {
            "pt": "Limpar histórico",
            "en": "Clear history",
        },
        "language": {
            "pt": "Escolha o idioma:",
            "en": "Choose language:",
        },
        "upload_label": {
            "pt": "📂 ZIP ou TAR com os arquivos 202401_NFs_Itens.csv, 202401_NFs_Cabecalho.csv",
            "en": "📂 ZIP or TAR with the files 202401_NFs_Itens.csv, 202401_NFs_Cabecalho.csv",
        },
        "common": {
            "pt": "Perguntas comuns",
            "en": "Common questions",
        },
        "loading_embeddings": {
            "pt": "Criando embeddings, aguarde...",
            "en": "Creating embeddings, please wait...",
        },
    }

    return translations[key][lang]


def save_to_temp(uploaded_file):
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def extract_archive(path):
    dest = os.path.dirname(path)
    if path.endswith(".zip"):
        with zipfile.ZipFile(path, "r") as z:
            z.extractall(dest)
    else:
        with tarfile.open(path, "r:*") as t:
            t.extractall(dest)
    return dest
