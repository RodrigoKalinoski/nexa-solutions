# Sistema de Chamados — Nexa Solutions

Projeto desenvolvido para a disciplina de **Manutenção e Evolução de Software**, com o objetivo de realizar manutenção corretiva e evolutiva em um sistema de gerenciamento de chamados.

A solução disponibiliza uma API REST para criação, consulta e atualização de chamados, incluindo filtro por status e indicadores, utilizando Django, Django REST Framework, PostgreSQL e Docker.

## Tecnologias utilizadas

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL 16
- Docker
- Docker Compose
- Git
- GitHub

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── chamados/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── docs/
│   ├── README.md
│   └── issues.md
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Funcionalidades

O sistema disponibiliza as seguintes funcionalidades:

- Cadastro de chamados.
- Validação obrigatória do título.
- Listagem de chamados.
- Consulta individual de chamados.
- Atualização de chamados.
- Filtro de chamados por status.
- Indicadores de quantidade de chamados.
- Persistência dos dados em PostgreSQL.
- Testes automatizados da API.

## Pré-requisitos

Para executar o projeto é necessário possuir:

- Docker
- Docker Compose

Não é necessário instalar Python ou PostgreSQL diretamente na máquina, pois os serviços são executados através de containers Docker.

## Configuração do ambiente

O projeto utiliza variáveis de ambiente para configurações do Django e do PostgreSQL.

Primeiro, crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Configure as variáveis conforme necessário.

Exemplo:

```env
DJANGO_SECRET_KEY=django-insecure-local-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=nexa
POSTGRES_USER=nexa
POSTGRES_PASSWORD=nexa_local_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

O arquivo `.env` contém configurações locais e **não deve ser versionado**.

O arquivo `.env.example` é mantido no repositório apenas como referência das variáveis necessárias para execução.

## Executando o projeto

Na raiz do repositório, execute:

```bash
docker compose up --build
```

O Docker Compose irá:

1. Criar o container PostgreSQL.
2. Inicializar o banco de dados.
3. Aguardar o banco atingir o estado saudável.
4. Criar o container da API.
5. Instalar as dependências Python durante o build.
6. Executar as migrations do Django.
7. Iniciar o servidor da aplicação.

A API estará disponível em:

```text
http://localhost:8000/api/
```

Para executar os containers em segundo plano:

```bash
docker compose up --build -d
```

Para encerrar os containers:

```bash
docker compose down
```

## Banco de dados

O projeto utiliza **PostgreSQL 16** executado em um container Docker.

O serviço da API se conecta ao PostgreSQL através da rede interna do Docker Compose utilizando o hostname:

```text
db
```

Os dados são armazenados em um volume Docker:

```text
postgres_data
```

Dessa forma, os dados permanecem disponíveis mesmo após a remoção dos containers com:

```bash
docker compose down
```

Para remover também os dados armazenados no volume:

```bash
docker compose down -v
```

## Migrations

As migrations são executadas automaticamente durante a inicialização da API.

O comando configurado no Docker Compose executa:

```bash
python manage.py migrate
```

antes de iniciar o servidor Django.

Para consultar as migrations manualmente:

```bash
docker compose exec api python manage.py showmigrations
```

## Endpoints da API

### Listar chamados

```http
GET /api/chamados/
```

Retorna todos os chamados cadastrados.

### Criar chamado

```http
POST /api/chamados/
```

Exemplo de requisição:

```json
{
  "titulo": "Erro ao acessar sistema",
  "descricao": "Usuário não consegue realizar login"
}
```

Quando válido, o endpoint retorna:

```text
201 Created
```

O status inicial do chamado é:

```text
ABERTO
```

### Validação de título

O campo `titulo` é obrigatório.

Uma requisição sem título:

```json
{
  "descricao": "Chamado sem título"
}
```

retorna:

```text
400 Bad Request
```

Da mesma forma, um título vazio também é rejeitado:

```json
{
  "titulo": "",
  "descricao": "Chamado com título vazio"
}
```

### Consultar chamado

```http
GET /api/chamados/{id}/
```

Exemplo:

```http
GET /api/chamados/1/
```

### Atualizar chamado

Atualização completa:

```http
PUT /api/chamados/{id}/
```

Atualização parcial:

```http
PATCH /api/chamados/{id}/
```

Exemplo para atualizar o status:

```json
{
  "status": "EM_ANDAMENTO"
}
```

## Filtro por status

A listagem de chamados permite filtrar registros através do parâmetro `status`.

Status disponíveis:

- `ABERTO`
- `EM_ANDAMENTO`
- `CONCLUIDO`

### Chamados abertos

```http
GET /api/chamados/?status=ABERTO
```

### Chamados em andamento

```http
GET /api/chamados/?status=EM_ANDAMENTO
```

### Chamados concluídos

```http
GET /api/chamados/?status=CONCLUIDO
```

Quando nenhum parâmetro é informado:

```http
GET /api/chamados/
```

todos os chamados são retornados.

Um status inválido, por exemplo:

```http
GET /api/chamados/?status=INVALIDO
```

retorna:

```text
400 Bad Request
```

## Indicadores

A API disponibiliza um endpoint com indicadores dos chamados:

```http
GET /api/indicadores/
```

Exemplo de resposta:

```json
{
  "total": 4,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 1
}
```

Os indicadores representam:

- `total`: quantidade total de chamados.
- `abertos`: quantidade com status `ABERTO`.
- `em_andamento`: quantidade com status `EM_ANDAMENTO`.
- `concluidos`: quantidade com status `CONCLUIDO`.

## Testes automatizados

Os testes automatizados podem ser executados dentro do container da API:

```bash
docker compose exec api python manage.py test chamados
```

A suíte possui testes para:

- Criação válida de chamado.
- Rejeição de chamado sem título.
- Rejeição de título vazio.
- Filtro pelo status `ABERTO`.
- Filtro pelo status `EM_ANDAMENTO`.
- Filtro pelo status `CONCLUIDO`.
- Tratamento de status inválido.
- Listagem de chamados sem filtro.
- Indicadores dos chamados.
- Indicadores sem registros cadastrados.

Atualmente a suíte possui **10 testes automatizados**.

Resultado esperado:

```text
Found 10 test(s).
System check identified no issues (0 silenced).

Ran 10 tests

OK
```

Também é possível executar a validação do projeto Django:

```bash
docker compose exec api python manage.py check
```

Resultado esperado:

```text
System check identified no issues (0 silenced).
```

## Decisões técnicas

### PostgreSQL em container

O SQLite utilizado inicialmente foi substituído pelo PostgreSQL para disponibilizar um ambiente de banco de dados mais próximo de uma aplicação real e permitir execução reproduzível através do Docker Compose.

### Persistência dos dados

Foi utilizado um volume Docker para que os dados do PostgreSQL não sejam perdidos quando os containers forem encerrados.

### Healthcheck do banco

O PostgreSQL possui um `healthcheck`, e a API somente é iniciada depois que o serviço do banco está saudável.

Isso evita tentativas de conexão enquanto o PostgreSQL ainda está inicializando.

### Variáveis de ambiente

Configurações sensíveis e específicas do ambiente foram removidas do código-fonte e externalizadas através de variáveis de ambiente.

Entre elas:

- chave secreta do Django;
- configurações de debug;
- hosts permitidos;
- banco de dados;
- usuário do PostgreSQL;
- senha do PostgreSQL;
- host e porta do banco.

O arquivo `.env` não é versionado.

### Migrations automáticas

As migrations são executadas automaticamente antes da inicialização do servidor Django, permitindo que uma instalação nova configure o banco de dados sem intervenção manual.

### Validação da API

As regras de validação são tratadas pelo Django REST Framework.

Tentativas de criação com dados inválidos retornam erros HTTP adequados, como:

```text
400 Bad Request
```

em vez de erros internos da aplicação.

## Validação em ambiente limpo

Para validar a aplicação como uma nova instalação, removendo containers e volumes existentes:

```bash
docker compose down -v
```

Em seguida:

```bash
docker compose up --build
```

A aplicação deve:

- construir a imagem da API;
- criar o PostgreSQL;
- criar o volume persistente;
- aguardar o banco ficar saudável;
- executar todas as migrations;
- iniciar o Django;
- disponibilizar a API na porta `8000`.

Após a inicialização, os testes podem ser executados com:

```bash
docker compose exec api python manage.py test chamados
```

## Fluxo de desenvolvimento

O desenvolvimento da atividade foi organizado utilizando:

- Issues para registrar as demandas.
- Branches específicas para cada alteração.
- Commits descritivos.
- Pull Requests para integração das alterações na branch `main`.
- Testes automatizados para validar as correções e evoluções realizadas.

## Documentação complementar

As demandas originais da atividade estão disponíveis em:

```text
docs/issues.md
```

O documento original de contextualização encontra-se em:

```text
docs/README.md
```