from langchain_openai import ChatOpenAI  # Change from OpenAI to ChatOpenAI
from prompt_builder import build_automat_prompt, build_role_task_input
from utils import clean_input
import tiktoken
from pydantic import SecretStr


def count_tokens(prompt: str, model: str = "o200k_base") -> int:
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(prompt))


def ask_agent(user_input: str, docs: list, csv_meta: dict, api_key: str) -> str:
    """
    docs: lista de Document(page_content, metadata) retornada pelo Chroma.
    csv_meta: dicionário de metadados (linhas, colunas, stats).
    """
    clean_question = clean_input(user_input)

    meta_text = "METADADOS:\n"
    for fname, md in csv_meta.items():
        meta_text += f"- {fname}: {md['rows']} linhas × {md['cols']} colunas\n"

    sample = "\n\nAMOSTRA DE DADOS RELEVANTES:\n"
    for doc in docs:
        sample += (
            f"Arquivo: {doc.metadata['filename']} | Linha: {doc.metadata['row']}\n"
        )
        sample += doc.page_content + "\n\n"

    prompt = build_automat_prompt(clean_question, context=f"{meta_text}\n\n{sample}")

    token_count = count_tokens(prompt, model="o200k_base")
    print(f"Token count for prompt: {token_count}")

    try:
        model = ChatOpenAI(
            temperature=0, api_key=SecretStr(api_key), model="gpt-4.1-nano"
        )
        response = model.invoke(prompt)
        print("Response from LLM:", response)
        content = response.content if hasattr(response, "content") else response
        if isinstance(content, str):
            return content
        else:
            return str(content)
    except Exception as e:
        print("Error in ask_agent:", e)
        return "Try again later"


def format_summary(
    summary: dict, api_key: str, lang: str = "pt", query: str = ""
) -> str:
    """
    Usa a LLM para gerar um texto mais bonito a partir do resumo já calculado.
    summary: dicionário com os dados exatos (ex: descrição, quantidade ou fornecedor e valor).
    lang: 'pt' ou 'en'.
    """
    from langchain_openai import ChatOpenAI
    from pydantic import SecretStr

    prompt = build_role_task_input(summary, lang=lang, query=query)

    try:
        model = ChatOpenAI(
            temperature=0.7, api_key=SecretStr(api_key), model="gpt-4.1-nano"
        )
        response = model.invoke(prompt)
        content = response.content if hasattr(response, "content") else response
        if isinstance(content, str):
            return content
        else:
            return str(content)
    except Exception as e:
        print("Error in format_summary:", e)
        return "Try again later"
