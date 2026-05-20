# Dia 2 — Upload e Persistencia Local

## Visao geral

O Dia 2 transformou a base criada no Dia 1 em algo útil de verdade: o sistema passou a aceitar upload de PDF, validar o arquivo, salvar o binário localmente e registrar metadados no banco.

Em termos de arquitetura, o Dia 2 foi a transição de:

- aplicação de infraestrutura

para:

- aplicação com primeiro fluxo de negócio completo

O fluxo implementado foi:

1. frontend seleciona um PDF
2. frontend envia `multipart/form-data`
3. backend valida o arquivo
4. backend gera nome interno com UUID
5. backend salva o PDF em storage local
6. backend grava metadados na tabela `documents`
7. backend responde com payload público
8. frontend mostra loading, erro ou sucesso

## O que foi feito

### Refatoracao estrutural do backend

O backend deixou de ser um único `main.py` simples e passou a ter uma divisão mínima por responsabilidade:

- `backend/app/api/`
- `backend/app/core/`
- `backend/app/db/`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/services/`

Arquivos principais criados:

- `backend/app/api/documents.py`
- `backend/app/core/config.py`
- `backend/app/db/database.py`
- `backend/app/models/document.py`
- `backend/app/schemas/document.py`
- `backend/app/services/file_service.py`

Essa mudança foi importante porque o Dia 2 introduziu persistência, validação e regras de upload. Manter tudo em `main.py` tornaria o crescimento do projeto desorganizado muito cedo.

### App factory e bootstrap da aplicacao

`backend/app/main.py` foi reescrito para usar `create_app()`.

Por que isso foi feito:

- facilita testes com ambientes isolados
- permite recriar a app com variáveis de ambiente diferentes
- reduz acoplamento entre startup global e execução local

Durante o startup, o backend faz duas coisas:

- garante a existência de `LOCAL_STORAGE_PATH`
- executa `Base.metadata.create_all(bind=engine)`

### Configuracao central

Foi criado `backend/app/core/config.py` com `Settings`.

Variáveis relevantes:

- `APP_ENV`
- `DATABASE_URL`
- `FRONTEND_ORIGIN`
- `STORAGE_TYPE`
- `LOCAL_STORAGE_PATH`
- `MAX_UPLOAD_SIZE_MB`

Por que centralizar:

- evita espalhar `os.getenv()` pelo código
- padroniza defaults
- simplifica testes e evolução futura

### Banco e modelo de dados

Foi criado `backend/app/db/database.py` com:

- `engine`
- `SessionLocal`
- `Base`
- `get_db()`

Foi criado `backend/app/models/document.py` com:

- enum `StorageType`
- enum `DocumentStatus`
- modelo `Document`

Campos persistidos:

- `id`
- `original_filename`
- `stored_filename`
- `content_type`
- `size_bytes`
- `storage_type`
- `local_path`
- `status`
- `created_at`
- `updated_at`

### Endpoint de upload

Foi criado:

- `POST /documents/upload`

Arquivo:

- `backend/app/api/documents.py`

Esse endpoint:

- recebe `UploadFile`
- lê o conteúdo em memória
- valida o arquivo
- cria o caminho local
- salva o arquivo
- persiste metadados no banco
- retorna um `DocumentResponse`

### Validacao de PDF

A validação foi implementada em `backend/app/services/file_service.py`.

Regras aplicadas:

- arquivo obrigatório
- extensão `.pdf`
- `content_type` compatível
- payload não vazio
- tamanho máximo de `10 MB`
- assinatura inicial `%PDF`

Por que validar assim:

- não confiar só no nome do arquivo
- evitar arquivos vazios ou arbitrários
- limitar risco de upload exagerado
- manter a primeira versão simples, sem parser pesado

### Salvar arquivo localmente

O arquivo é salvo usando:

- nome físico interno com `UUID`
- mesma extensão do arquivo original
- diretório vindo de `LOCAL_STORAGE_PATH`

Por que usar UUID:

- evita colisão de nomes
- desacopla nome original do nome físico
- melhora segurança operacional

### Tratamento de falha de persistencia

Em `backend/app/api/documents.py`, se o banco falhar depois do arquivo já ter sido salvo:

- faz `rollback`
- remove o arquivo do disco

Por que isso importa:

- evita lixo órfão no storage
- mantém coerência entre banco e filesystem

## Frontend implementado no Dia 2

### Mudanca de foco da UI

`frontend/src/App.vue` deixou de ser uma landing de status e passou a ser uma tela de upload.

Foram implementados:

- seleção de arquivo com `v-file-input`
- envio via `axios`
- mensagem de erro
- estado de loading
- mensagem de sucesso
- exibição dos metadados retornados pela API

### Cliente HTTP dedicado

Foi criado:

- `frontend/src/services/api.ts`

Ele encapsula a `baseURL` usando `VITE_API_URL`.

Por que isso foi feito:

- evita URL hardcoded no componente
- prepara o terreno para endpoints futuros
- reduz repetição

### Estados de interface

O componente passou a trabalhar com:

- `idle`
- `loading`
- `success`
- `error`

Por que explicitar estados:

- torna o fluxo previsível
- melhora UX
- evita lógica ambígua no template

### Dependencia nova

Foi adicionada a dependência:

- `axios`

em:

- `frontend/package.json`
- `frontend/package-lock.json`

## Arquivos criados no Dia 2

### Backend

- `backend/app/api/__init__.py`
- `backend/app/api/documents.py`
- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/db/__init__.py`
- `backend/app/db/database.py`
- `backend/app/models/__init__.py`
- `backend/app/models/document.py`
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/document.py`
- `backend/app/services/__init__.py`
- `backend/app/services/file_service.py`

### Frontend

- `frontend/src/services/api.ts`

### Testes

- `tests/backend/test_documents_upload.py`

## Arquivos modificados no Dia 2

- `.env.example`
- `.gitignore`
- `README.md`
- `backend/app/main.py`
- `backend/requirements.txt`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/src/App.vue`
- `tests/conftest.py`
- `tests/backend/test_health.py`

## Arquivos apagados no Dia 2

Do ponto de vista de Git e arquitetura, nao houve remoções funcionais relevantes já consolidadas no histórico. Houve substituição de conteúdo em arquivos existentes, especialmente:

- `backend/app/main.py`
- `frontend/src/App.vue`

Mas isso ocorreu como modificação estrutural, não como remoção de arquivo seguida de abandono.

## Decisoes arquiteturais do Dia 2

### 1. `create_all` em vez de Alembic

Escolha:

- usar `Base.metadata.create_all()`

Por que:

- mais rápido para colocar o fluxo de upload em produção local
- menos atrito no segundo dia
- suficiente para um schema inicial único

Tradeoff:

- não há versionamento formal de migrations ainda
- isso provavelmente mudará quando o schema crescer

### 2. Storage local em vez de S3

Escolha:

- persistência local em filesystem

Por que:

- o Dia 2 explicitamente pede persistência local
- reduz custo e superfície de erro
- mantém o projeto alinhado com a prioridade “rodar localmente”

Tradeoff:

- não resolve distribuição, durabilidade externa nem acesso remoto

### 3. Persistir `local_path` no banco, mas nao expor na API

Escolha:

- guardar caminho local em `documents.local_path`
- omitir esse campo em `DocumentResponse`

Por que:

- o backend precisa saber onde o arquivo está
- o cliente não deve conhecer caminho interno do servidor

Tradeoff:

- exige schema de resposta separado do modelo ORM, o que foi corretamente introduzido com `DocumentResponse`

### 4. Validacao por assinatura `%PDF`

Escolha:

- verificar bytes iniciais do arquivo

Por que:

- é um meio barato de confirmar o tipo real
- é mais forte que confiar apenas em extensão e content type

Tradeoff:

- não substitui validação semântica completa do PDF
- PDFs extremamente malformados podem passar da assinatura inicial

### 5. Tela unica no frontend

Escolha:

- não adicionar router nem múltiplas views ainda

Por que:

- mantém o escopo do Dia 2 focado no fluxo de upload
- evita antecipar a navegação do Dia 3

Tradeoff:

- o componente `App.vue` ficou mais pesado
- no futuro ele provavelmente será quebrado em componentes e views

### 6. Testes com SQLite temporário

Escolha:

- não depender do PostgreSQL do Compose para testes

Por que:

- testes precisam ser rápidos, isolados e repetíveis
- elimina dependência de infraestrutura externa

Tradeoff:

- SQLite não reproduz 100% do comportamento do PostgreSQL
- mas é suficiente para validar o fluxo básico deste dia

## Testes adicionados

### `tests/conftest.py`

Foi criado um helper de teste que:

- injeta `PYTHONPATH`
- redefine `DATABASE_URL`
- redefine `LOCAL_STORAGE_PATH`
- redefine `MAX_UPLOAD_SIZE_MB`
- recria os módulos relevantes
- gera `TestClient` isolado

### `tests/backend/test_health.py`

O teste de health foi adaptado para:

- usar ambiente de teste isolado
- garantir que a app factory funciona

### `tests/backend/test_documents_upload.py`

Cobre:

- upload válido
- persistência do arquivo
- persistência de metadados
- rejeição por extensão errada
- rejeição por assinatura inválida
- rejeição por tamanho acima do limite

## Atualizacoes auxiliares

### `.env.example`

Passou a incluir:

- `STORAGE_TYPE=LOCAL`
- `LOCAL_STORAGE_PATH=/app/storage`
- `MAX_UPLOAD_SIZE_MB=10`

### `.gitignore`

Passou a ignorar:

- `backend/storage/`

Por que:

- PDFs enviados não devem entrar no Git

### `README.md`

Foi atualizado para refletir:

- endpoint de upload
- existência do fluxo do Dia 2
- nova checklist de validação

## Estado atual do Dia 2

Importante: no momento desta documentação, o Dia 2 está implementado no working tree local, mas ainda não aparece como commit separado no histórico exibido por `git log`.

Ou seja:

- Dia 1 e hardening Docker já estão em commits
- Dia 2 está implementado no código local atual
- a documentação abaixo descreve esse estado real do working tree

## Resumo tecnico

O Dia 2 consolidou quatro pilares fundamentais do produto:

- primeiro endpoint de negócio
- primeiro modelo persistido
- primeiro fluxo real de UI para API
- primeira estratégia de teste de integração local

Foi o ponto em que o projeto deixou de ser apenas “estrutura que sobe” e passou a ser “aplicação que executa um caso de uso de verdade”.
