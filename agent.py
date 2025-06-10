import openai
from langchain_community.llms import OpenAI
from prompt_builder import build_automat_prompt
from utils import clean_input


def ask_agent(user_input, csv_data: dict, csv_meta: dict, api_key: str):
    clean_question = clean_input(user_input)

    prompt = build_automat_prompt(clean_question, csv_data)
    print(f"Prompt: {prompt}")

    try:
        openai.api_key = api_key
        model = OpenAI(temperature=0, openai_api_key=api_key)
        return model.invoke(prompt)
    except Exception as e:
        print(f"Error in ask_agent: {e}")
        return "Try again later"


def get_all_headers(csv_data: dict):
    return [col for df in csv_data.values() for col in df.columns]
