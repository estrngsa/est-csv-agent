# 📊 CSV Assistant Agent (RAG)

[🇧🇷 Versão em Português](README.pt.md)

A Streamlit-based assistant for analyzing and querying CSV files, with a focus on Brazilian "Notas Fiscais" (invoices). Uses Retrieval-Augmented Generation (RAG) with OpenAI models and vector search for accurate, context-aware answers.

## Features

- Upload and analyze multiple CSV files.
- Extracts and summarizes metadata and statistics from your data.
- Natural language Q&A about your CSVs, including:
  - "Which item had the highest delivered volume?"
  - "Which supplier received the highest amount?"
- Uses OpenAI LLMs (configurable) for advanced summarization and explanations.
- Retrieval-Augmented Generation (RAG): finds relevant CSV chunks before answering.
- Multilingual support (Portuguese 🇧🇷 and English 🇺🇸).
- Interactive chat interface with conversation history.
- Persistent vector database for fast retrieval.

## How it works

1. **CSV Loading:** Reads all CSVs from the `data/` folder.
2. **Metadata Extraction:** Builds metadata and statistics for each file.
3. **Vector Indexing:** Converts CSV rows into embeddings and stores them in a Chroma vector database.
4. **Question Answering:** User asks a question; the system retrieves relevant CSV chunks and builds a prompt for the LLM.
5. **LLM Response:** The LLM answers using only the provided data sample.
6. **Chat History:** All questions and answers are stored and displayed in a chat-like interface.

## Requirements

- Python 3.9+
- OpenAI API key (set in `.env` as `OPENAI_API_KEY`)
- See `requirements.txt` for dependencies.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd est-csv-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your CSV files:**
   - Place your CSV files in the `data/` folder.

4. **Set your OpenAI API key:**
   - Create a `.env` file with:
     ```
     OPENAI_API_KEY=sk-...
     ```

5. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## Usage

- Use the chat input or click the common question buttons.
- Switch language using the toggle (🇧🇷/🇺🇸).
- View and clear your question/answer history.

## Project Structure

```
est-csv-agent/
├── actions.py
├── agent.py
├── csv_handler.py
├── main.py
├── prompt_builder.py
├── requirements.txt
├── utils.py
├── vector_store.py
├── data/
└── ...
```

## Customization

- **Prompt Engineering:** See `prompt_builder.py` to adjust how prompts are built for the LLM.
- **Model Selection:** Change the model in `agent.py` as needed (e.g., `gpt-3.5-turbo`, `gpt-4.1-nano`).
- **Translation:** Edit `utils.py` to add or modify translations.

## License

MIT License

---

**Developed with ❤️ using Streamlit, LangChain, and OpenAI.**