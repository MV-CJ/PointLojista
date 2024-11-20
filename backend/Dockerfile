FROM python:3.9-slim

# Definindo o diretório de trabalho no container
WORKDIR /backend

# Copiando o arquivo de requisitos para o diretório de trabalho no container
COPY . .

# Instalando as dependências
RUN pip install -r requirements.txt

# Comando para rodar a aplicação
CMD ["gunicorn", "-b", "0.0.0.0:5999", "app.app:app"]