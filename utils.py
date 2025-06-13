from unidecode import unidecode


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
    }

    return translations[key][lang]
