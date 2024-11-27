# Documentação da API - FastAPI

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
PointLojista/ 
├── backend/ 
│ ├── app/ 
│ │ ├── init.py 
│ │ ├── crud.py 
│ │ ├── database.py 
│ │ ├── main.py 
│ │ ├── models.py 
│ │ ├── routes.py 
│ │ ├── schemas.py 
│ │ └── init.py 
│ ├── Dockerfile 
│ ├── requirements.txt 
└── docker-compose.yml
```

## Requisitos

O arquivo `requirements.txt` deve conter as dependências necessárias para a aplicação:

```txt
fastapi==0.115.5
uvicorn==0.32.1
psycopg2-binary==2.9.10
sqlalchemy==1.4.41
pydantic==2.0
```

## Endpoints da API

1. **Criar Usuário:**
   - **Endpoint**: `POST /users/`
   - **Descrição**: Cria um novo usuário.

**Exemplo de uso**:

```json
    {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "securepassword"
    }
```

2. **Ler Usuário**:
   - **Endpoint**: `GET /users/{user_id}`
   - **Descrição**: Retorna os dados de um usuário específico.
   - **Exemplo de uso**: `GET /users/123e4567-e89b-12d3-a456-426614174000`

3. **Atualizar Usuário**:
    - **Endpoint**: `PUT /users/{user_id}`
    - **Descrição**: Atualiza os dados de um usuário específico.
    - **Exemplo de uso**:

```json
{
    "username": "john_doe_updated",
    "email": "john_doe_updated@example.com"
}
```

4. **Deletar Usuário:**
    - **Endpoint**: DELETE /users/{user_id}
    - **Descrição**: Deleta um usuário específico.
    - **Exemplo de uso**: 
```json
DELETE /users/123e4567-e89b-12d3-a456-426614174000
```

5. **Listar Usuários:**
    - **Endpoint**: GET /users/
    - **Descrição**:Retorna uma lista de usuários.
    - **Parâmetros de Query:**

        **skip:** Número de registros a serem pulados (opcional).
        
        **limit:** Limite de registros a serem retornados (opcional).


**Exemplo de uso:**
```json
GET /users/?skip=0&limit=10
```

## Como rodar a aplicação
```bash
docker-compose up --build
```
Por default a aplicação será acessível em: http://localhost:5999

### Notas
> Este projeto foi criado uma instancia no SUPABASE, caso queira utilizar outro banco de dados, basta alterar a variável de ambiente DATABASE_URL dentro do docker-compose.yml.

>Se necessario substituir a porta 5999 para outra basta realizar a alteração no Dockerfile.

Essa documentação cobre os principais pontos da API de maneira simples. 