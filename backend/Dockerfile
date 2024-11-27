FROM python:3.9-slim

# Instalar dependências do PostgreSQL e ferramentas de compilação
RUN apt-get update && apt-get install -y libpq-dev gcc

# Definindo o diretório de trabalho no container
WORKDIR /backend

# Copiando os arquivos do backend para o diretório de trabalho
COPY . .

# Atualizando o pip
RUN pip install --upgrade pip

# Instalando as dependências
RUN pip install -r requirements.txt

# Comando para rodar a aplicação usando Uvicorn (FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5999"]
