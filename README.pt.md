# 📊 Agente Assistente de CSV (RAG)

[🇺🇸 English version](README.md)

Um assistente baseado em Streamlit para análise e consulta de arquivos CSV, com foco em "Notas Fiscais" brasileiras. Utiliza Geração Aumentada por Recuperação (RAG) com modelos OpenAI e busca vetorial para respostas precisas e contextualizadas.

## Funcionalidades

- Carregue e analise múltiplos arquivos CSV.
- Extrai e resume metadados e estatísticas dos seus dados.
- Perguntas e respostas em linguagem natural sobre seus CSVs, incluindo:
  - "Qual item teve maior volume entregue?"
  - "Qual fornecedor recebeu o maior montante?"
- Usa LLMs da OpenAI (configurável) para sumarização e explicações avançadas.
- Geração Aumentada por Recuperação (RAG): encontra trechos relevantes do CSV antes de responder.
- Suporte multilíngue (Português 🇧🇷 e Inglês 🇺🇸).
- Interface de chat interativa com histórico de conversas.
- Banco vetorial persistente para buscas rápidas.

## Como funciona

1. **Carregamento dos CSVs:** Lê todos os arquivos CSV de um arquivo ZIP ou TAR com os 202401_NFs_Itens.csv, 202401_NFs_Cabecalho.csv
2. **Extração de Metadados:** Gera metadados e estatísticas para cada arquivo.
3. **Indexação Vetorial:** Converte linhas dos CSVs em embeddings e armazena em um banco vetorial Chroma.
4. **Perguntas e Respostas:** O usuário faz uma pergunta; o sistema recupera trechos relevantes do CSV e monta um prompt para a LLM.
5. **Resposta da LLM:** O modelo responde usando apenas a amostra de dados fornecida.
6. **Histórico de Chat:** Todas as perguntas e respostas são armazenadas e exibidas em formato de chat.

## Requisitos

- Python 3.9+
- Chave da API OpenAI (defina no `.env` como `OPENAI_API_KEY`)
- Veja `requirements.txt` para dependências.

## Como começar

1. **Clone o repositório:**
   ```bash
   git clone <repo-url>
   cd est-csv-agent
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Adicione seus arquivos CSV:**
   - Coloque seus arquivos CSV na pasta `data/`.

4. **Defina sua chave da API OpenAI:**
   - Crie um arquivo `.env` com:
     ```
     OPENAI_API_KEY=sk-...
     USE_OPENAI=
     CHROMA_K=
     OPENAI_MODEL=
     OPENAI_TEMPERATURE=
     ```

5. **Execute o app:**
   ```bash
   streamlit run main.py
   ```

## Uso

- Use o campo de chat ou clique nos botões de perguntas comuns.
- Altere o idioma usando o seletor (🇧🇷/🇺🇸).
- Veja e limpe o histórico de perguntas e respostas.

## Estrutura do Projeto

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
└── ...
```
Disponivel apenas para o Curso de Agentes Autonomos do Instituto I2A2

---

**Desenvolvido usando Streamlit, LangChain e OpenAI.**
