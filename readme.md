# API Dados Embrapa

Esta API coleta dados do Site da Embrapa, em formato CSV, devido a constante indisponibilidade do site, armazena-os em um banco de dados e disponibiliza as informações através de endpoints, relacionados abaixo.

- **Link Embrapa:** `http://vitibrasil.cnpuv.embrapa.br/`

Atividade feita como parte da avaliação do Curso de Pós Graduação em Mechine Learning Engineering da Insituição FIAP, no ano de 2024.


## Exemplo de Uso - Flasgger

#### Criação de Usuário e Senha
 ![Criação de Usário e Senha](/documents/images/criar_user.png)

#### Fazendo Login na API
![Fazendo Login na API](/documents/images/autenticação.png)

#### Encontrando o Token de Acesso para Requisição 
Faça a Cópia do Seu Token
![Encontrando o Toke de Acesso](/documents/images/token_acesso.png)

#### Realizando Requisição GET pela API usando o Token
No campo Authorization escreva "Bearer + Token"
![Realizando Requisição Get](/documents/images/gets.png)

#### Resultado - Retorno da API
![Resultado - Retorno da API](/documents/images/resultado.png)

## Endpoints

### Autenticação

#### Login

- **URL:** `/login`
- **Método:** `POST`
- **Descrição:** Realiza o login do usuário.
- **Parâmetros:**
  - `username` (string, obrigatório): O nome de usuário.
  - `password` (string, obrigatório): A senha do usuário.
- **Respostas:**
  - `200 OK`: Login bem-sucedido.
    ```json
    {
      "access_token": "string"
    }
    ```
  - `401 Unauthorized`: Credenciais inválidas.
    ```json
    {
      "error": "Credenciais inválidas"
    }
    ```

#### Registro

- **URL:** `/register`
- **Método:** `POST`
- **Descrição:** Registra um novo usuário.
- **Parâmetros:**
  - `username` (string, obrigatório): O nome de usuário.
  - `password` (string, obrigatório): A senha do usuário.
- **Respostas:**
  - `201 Created`: Usuário registrado com sucesso.
    ```json
    {
      "msg": "Usuário cadastrado com sucesso"
    }
    ```
  - `400 Bad Request`: Username e senha são obrigatórios.
    ```json
    {
      "error": "Username e senha são obrigatórios"
    }
    ```
  - `409 Conflict`: Usuário já existe.
    ```json
    {
      "error": "Usuário já existe"
    }
    ```

### Comércio

#### Obter Dados de Comércio

- **URL:** `/comercio`
- **Método:** `GET`
- **Descrição:** Obtém dados de comércio por ano.
- **Parâmetros:**
  - `ano` (integer, opcional): O ano para filtrar os dados de comércio.
- **Respostas:**
  - `200 OK`: Dados de comércio recuperados com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `500 Internal Server Error`: Erro interno do servidor.

### Data Log

#### Obter Log de Dados

- **URL:** `/data_info/<uuid>`
- **Método:** `GET`
- **Descrição:** Obtém o log de dados pelo UUID.
- **Parâmetros:**
  - `uuid` (string, obrigatório): O UUID do log de dados.
- **Respostas:**
  - `200 OK`: Log de dados recuperado com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `404 Not Found`: Log de dados não encontrado.
  - `500 Internal Server Error`: Erro interno do servidor.

### Exportação

#### Obter Dados de Exportação

- **URL:** `/exportacao/<objeto>`
- **Método:** `GET`
- **Descrição:** Obtém dados de exportação por ano.
- **Parâmetros:**
  - `objeto` (string, obrigatório): Objeto/Tipo de uva de exportação.
  - `ano` (integer, opcional): Ano da exportação.
- **Respostas:**
  - `200 OK`: Dados de exportação recuperados com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `500 Internal Server Error`: Erro interno do servidor.

### Importação

#### Obter Dados de Importação

- **URL:** `/importacao/<objeto>`
- **Método:** `GET`
- **Descrição:** Obtém dados de importação por ano.
- **Parâmetros:**
  - `objeto` (string, obrigatório): Objeto de importação.
  - `ano` (integer, opcional): Ano da importação.
- **Respostas:**
  - `200 OK`: Dados de importação recuperados com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `500 Internal Server Error`: Erro interno do servidor.

### Processamento

#### Obter Dados de Processamento

- **URL:** `/processamento/<objeto>`
- **Método:** `GET`
- **Descrição:** Obtém dados de processamento por ano.
- **Parâmetros:**
  - `objeto` (string, obrigatório): O objeto/Tipo de uva para o qual os dados de processamento são recuperados.
  - `ano` (integer, opcional): O ano para filtrar os dados de processamento.
- **Respostas:**
  - `200 OK`: Dados de processamento recuperados com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `500 Internal Server Error`: Erro interno do servidor.

### Produção

#### Obter Dados de Produção

- **URL:** `/producao`
- **Método:** `GET`
- **Descrição:** Obtém dados de produção por ano.
- **Parâmetros:**
  - `ano` (integer, opcional): O ano para filtrar os dados de produção.
- **Respostas:**
  - `200 OK`: Dados de produção recuperados com sucesso.
  - `401 Unauthorized`: Acesso não autorizado.
  - `500 Internal Server Error`: Erro interno do servidor.

## Requisitos

- Flask-SQLAlchemy==3.1.1
- python-dotenv==1.0.1
- PyMySQL==1.1.1
- cryptography==43.0.1
- requests==2.32.3
- pytest==8.3.2
- pandas==2.2.2
- APScheduler==3.10.4
- Flask-JWT-Extended==4.6.0
- psycopg2-binary==2.9.10
- flasgger==0.9.7.1

## Estrutura do Banco de Dados

Este documento descreve a estrutura do banco de dados utilizado para armazenar informações de captura de arquivos e dados relacionados a produção, comércio, exportação, importação e processamento.

### Tabelas

#### 1. `data_log`
Armazena informações sobre a captura dos arquivos.

- **uuid**: `VARCHAR(36)` - Identificador único para cada registro de captura.
- **object**: `VARCHAR(255)` - Nome do objeto capturado.
- **record_date**: `DATETIME` - Data e hora da captura do arquivo (padrão: `CURRENT_TIMESTAMP`).
- **object_modified_date**: `DATETIME` - Data e hora da modificação do arquivo.

#### 2. `producao`
Armazena informações da captura do arquivo `Producao.csv`.

- **uuid**: `VARCHAR(36)` - Identificador único da captura.
- **id**: `INT` - Identificador do registro.
- **control**: `VARCHAR(50)` - Controle do registro.
- **produto**: `VARCHAR(255)` - Nome do produto.
- **ano**: `INT` - Ano do registro.
- **quantidade**: `DECIMAL(15, 2)` - Quantidade do produto.
- **tipo**: `VARCHAR(50)` - Tipo do item (item ou pai).
- **totalizador**: `VARCHAR(255)` - Identificador do item pai.
- **PRIMARY KEY**: (`uuid`, `id`, `ano`)

#### 3. `comercio`
Armazena informações da captura do arquivo `Comercio.csv`.

- **uuid**: `VARCHAR(36)` - Identificador único da captura.
- **id**: `INT` - Identificador do registro.
- **control**: `VARCHAR(50)` - Controle do registro.
- **produto**: `VARCHAR(255)` - Nome do produto.
- **ano**: `INT` - Ano do registro.
- **quantidade**: `DECIMAL(15, 2)` - Quantidade do produto.
- **tipo**: `VARCHAR(50)` - Tipo do item (item ou pai).
- **totalizador**: `VARCHAR(255)` - Identificador do item pai.
- **PRIMARY KEY**: (`uuid`, `id`, `ano`)

#### 4. `exportacao`
Armazena informações da captura do arquivo `Exp<objeto>.csv`.

- **uuid**: `VARCHAR(36)` - Identificador único da captura.
- **id**: `INT` - Identificador do registro.
- **object**: `VARCHAR(255)` - Nome do objeto exportado.
- **pais**: `VARCHAR(255)` - País de destino.
- **ano**: `INT` - Ano do registro.
- **quantidade**: `DECIMAL(15, 2)` - Quantidade exportada.
- **valor**: `DECIMAL(15, 2)` - Valor da exportação.
- **PRIMARY KEY**: (`uuid`, `id`, `ano`)

#### 5. `importacao`
Armazena informações da captura do arquivo `Imp<objeto>.csv`.

- **uuid**: `VARCHAR(36)` - Identificador único da captura.
- **id**: `INT` - Identificador do registro.
- **object**: `VARCHAR(255)` - Nome do objeto importado.
- **pais**: `VARCHAR(255)` - País de origem.
- **ano**: `INT` - Ano do registro.
- **quantidade**: `DECIMAL(15, 2)` - Quantidade importada.
- **valor**: `DECIMAL(15, 2)` - Valor da importação.
- **PRIMARY KEY**: (`uuid`, `id`, `ano`)

#### 6. `processamento`
Armazena informações da captura de dados de processamento.

- **uuid**: `VARCHAR(36)` - Identificador único da captura.
- **id**: `INT` - Identificador do registro.
- **control**: `VARCHAR(50)` - Controle do registro.
- **object**: `VARCHAR(255)` - Nome do objeto processado.
- **cultivar**: `VARCHAR(255)` - Nome da cultivar.
- **ano**: `INT` - Ano do registro.
- **quantidade**: `DECIMAL(15, 2)` - Quantidade processada.
- **tipo**: `VARCHAR(50)` - Tipo do item (item ou pai).
- **totalizador**: `VARCHAR(255)` - Identificador do item pai.
- **PRIMARY KEY**: (`uuid`, `id`, `control`, `ano`)

#### 7. `usuarios`
Armazena informações dos usuários do sistema.

- **id**: `CHAR(36)` - Identificador único do usuário.
- **usuario**: `VARCHAR(80)` - Nome de usuário (único).
- **senha**: `VARCHAR(200)` - Senha do usuário.

## Contato

### André Torres
- **Wpp:** +55 11 98560-3464

### Victor H.
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/victor-hugo-teles-de-santana-359ba260/)

### Nathan Lobato
- **Wpp:** +55 42 99824-7049

---
