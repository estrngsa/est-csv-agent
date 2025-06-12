# Use uma imagem oficial leve de Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie e instale dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código
COPY . .

# Exponha a porta padrão do Streamlit
EXPOSE 8501

# Ao iniciar, rode o Streamlit apontando pro main.py
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
