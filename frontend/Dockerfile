# Use a imagem mais recente do Node.js
FROM node:latest

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de dependência
COPY package*.json ./

# Instale as dependências
RUN npm install

# Copie o restante do código do front-end
COPY . .

# Exponha a porta que o Next.js usará
EXPOSE 3000

# Comando para rodar a aplicação Next.js em modo de desenvolvimento
CMD ["npm", "run", "dev"]
