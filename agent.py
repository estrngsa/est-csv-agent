from langchain_openai import ChatOpenAI  # Change from OpenAI to ChatOpenAI
from prompt_builder import build_automat_prompt
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

    # 1) Prefácio com metadados resumidos
    meta_text = "METADADOS:\n"
    for fname, md in csv_meta.items():
        meta_text += f"- {fname}: {md['rows']} linhas × {md['cols']} colunas\n"

    # 2) Amostra dos docs recuperados
    sample = "\n\nAMOSTRA DE DADOS RELEVANTES:\n"
    for doc in docs:
        sample += (
            f"Arquivo: {doc.metadata['filename']} | Linha: {doc.metadata['row']}\n"
        )
        sample += doc.page_content + "\n\n"

    # 3) Monta prompt final
    prompt = build_automat_prompt(clean_question, context=f"{meta_text}\n\n{sample}")

    # Calculate and print token count
    token_count = count_tokens(prompt, model="o200k_base")
    print(f"Token count for prompt: {token_count}")

    # 4) Chama o LLM
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
    import json
    from pydantic import SecretStr

    prompt = f"""
You are a professional technical copywriter.

## Task
Rewrite the following summary in clear, concise, and engaging English prose, suitable for a business or technical audience. Focus on accuracy, readability, and informativeness.

## Guidelines
- Use natural, fluent English.
- Present the information in a logical and well-structured way.
- Do not invent or omit any details.
- If the summary contains numbers, units, or names, preserve them accurately.
- Avoid unnecessary repetition.
- Answer in the same language as the input (English or Portuguese) {lang}.
- Don't be overwhelming in the amount of information, keep it concise.

## User Input
{query}

## Data to summarize
{json.dumps(summary, ensure_ascii=False, indent=2)}   
"""
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
