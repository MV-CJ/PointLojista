FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /backend

# Instalar dependências necessárias para o Python
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar as dependências do Python
COPY requirements.txt requirements.txt


# Instalar dependências do Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código para o contêiner
COPY . .

# Expor as portas usadas pelo backend
EXPOSE 5999

# Iniciar o aplicativo Python
CMD python run.py
