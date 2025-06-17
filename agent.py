from langchain_openai import ChatOpenAI
from prompt_builder import build_automat_prompt, build_role_task_input
from utils import clean_input
import tiktoken
from pydantic import SecretStr
import os


class CsvAgent:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-nano",
        temperature: float = 0,
        timeout: int = 30,
    ):
        self.model_name = model or os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
        self.temperature = temperature
        self.api_key = api_key
        self.timeout = timeout
        self.llm = ChatOpenAI(
            temperature=self.temperature,
            api_key=SecretStr(self.api_key),
            model=self.model_name,
            timeout=self.timeout,
        )

    def count_tokens(self, prompt: str, model: str = "o200k_base") -> int:
        enc = tiktoken.get_encoding(model)
        return len(enc.encode(prompt))

    def ask(self, user_input: str, docs: list, csv_meta: dict) -> str:
        clean_question = clean_input(user_input)
        meta_text = "METADATA:\n"
        if csv_meta:
            if "head_fields_with_type" in csv_meta:
                meta_text += (
                    "- Header fields: "
                    + ", ".join(
                        f"{k} ({v})" for k, v in csv_meta["head_fields_with_type"]
                    )
                    + "\n"
                )
            if "item_fields_with_type" in csv_meta:
                meta_text += (
                    "- Item fields: "
                    + ", ".join(
                        f"{k} ({v})" for k, v in csv_meta["item_fields_with_type"]
                    )
                    + "\n"
                )
            if "num_nfes" in csv_meta:
                meta_text += f"- Number of invoices: {csv_meta['num_nfes']}\n"
            if "avg_items_per_nfe" in csv_meta:
                meta_text += f"- Average items per invoice: {csv_meta['avg_items_per_nfe']:.2f}\n"
            if "date_range" in csv_meta:
                meta_text += f"- Date range: {csv_meta['date_range'][0]} to {csv_meta['date_range'][1]}\n"
            if "max_invoice_value" in csv_meta and "max_invoice_chave" in csv_meta:
                meta_text += f"- Max invoice value: {csv_meta['max_invoice_value']} (Access Key: {csv_meta['max_invoice_chave']})\n"

        sample = "\n\nRELEVANT DATA SAMPLE:\n"
        for doc in docs:
            meta = doc.metadata
            if meta.get("type") == "head":
                sample += f"Invoice Access Key: {meta.get('chave')} | Type: Header\n"
            elif meta.get("type") == "item":
                sample += f"Invoice Access Key: {meta.get('chave')} | Type: Item | Item Index: {meta.get('item_idx')}\n"
            else:
                sample += f"Metadata: {meta}\n"
            sample += doc.page_content + "\n\n"

        prompt = build_automat_prompt(
            clean_question, context=f"{meta_text}\n\n{sample}"
        )
        token_count = self.count_tokens(prompt, model="o200k_base")
        print(f"Token count for prompt: {token_count}")

        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, "content") else response
            if isinstance(content, str):
                return content
            else:
                return str(content)
        except Exception as e:
            print("Error in ask_agent:", e)
            return "Try again later"

    def format_summary(self, summary: dict, lang: str = "pt", query: str = "") -> str:
        prompt = build_role_task_input(summary, lang=lang, query=query)
        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, "content") else response
            if isinstance(content, str):
                return content
            else:
                return str(content)
        except Exception as e:
            print("Error in format_summary:", e)
            return "Try again later"
