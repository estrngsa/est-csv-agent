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
    }
    return translations[key][lang]
