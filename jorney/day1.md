# Dia 1 — Setup do Projeto

## Visao geral

O Dia 1 saiu de um repositório praticamente documental para uma base fullstack executável. Antes dele, o projeto tinha essencialmente `descricao.md` e quase nenhuma estrutura operacional. O objetivo foi criar uma espinha dorsal previsível para desenvolvimento local, com frontend, backend e banco subindo de forma padronizada.

O resultado prático do Dia 1 foi:

- frontend Vue 3 acessível
- backend FastAPI respondendo `GET /health`
- PostgreSQL via Docker
- documentação mínima e variáveis de ambiente definidas

## O que foi feito

### Backend inicial

Foi criado um backend mínimo em FastAPI com:

- `backend/app/main.py`
- `backend/requirements.txt`
- `backend/Dockerfile`
- `backend/app/__init__.py`

Esse backend tinha um único endpoint:

- `GET /health`

Ele existia para provar que:

- a aplicação Python subia corretamente
- o container do backend funcionava
- o frontend já tinha uma URL de API conhecida

### Frontend inicial

Foi criado um frontend Vue 3 com Vite, TypeScript e Vuetify:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/vite.config.ts`
- `frontend/index.html`
- `frontend/src/main.ts`
- `frontend/src/env.d.ts`
- `frontend/src/plugins/vuetify.ts`
- `frontend/src/styles/main.css`
- `frontend/src/App.vue`
- `frontend/Dockerfile`

Esse frontend não tinha navegação, store, router nem comunicação real com API. A intenção foi deliberadamente simples: uma tela estática apresentando o estado do setup e as portas do sistema.

### Orquestracao local

Foi criado `docker-compose.yml` na raiz com tres serviços:

- `db`
- `backend`
- `frontend`

O Compose fazia o seguinte:

- subia PostgreSQL com volume persistente
- construía a imagem do backend
- construía a imagem do frontend
- publicava `5432`, `8000` e `5173`
- garantia ordem mínima de subida com `depends_on`

### Configuracao e documentacao

Foram criados ou preenchidos:

- `.env.example`
- `.gitignore`
- `README.md`
- `tests/conftest.py`
- `tests/backend/test_health.py`

O `README.md` passou a documentar:

- pré-requisitos
- comando de subida com Compose
- execução sem Docker
- checklist básico de validação

## Arquivos criados no Dia 1

Com base no commit `20e6eeb chore: setup inicial`, estes foram os principais arquivos adicionados:

- `.env.example`
- `.gitignore`
- `README.md`
- `docker-compose.yml`
- `backend/Dockerfile`
- `backend/requirements.txt`
- `backend/app/__init__.py`
- `backend/app/main.py`
- `frontend/Dockerfile`
- `frontend/index.html`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/vite.config.ts`
- `frontend/src/App.vue`
- `frontend/src/env.d.ts`
- `frontend/src/main.ts`
- `frontend/src/plugins/vuetify.ts`
- `frontend/src/styles/main.css`
- `tests/conftest.py`
- `tests/backend/test_health.py`

## Decisoes arquiteturais do Dia 1

### 1. Stack inteira em Docker Compose

Escolha:

- subir frontend, backend e banco via Compose

Por que:

- reduz divergência entre ambientes
- força integração desde o início
- documenta a arquitetura operacional já no Dia 1

Tradeoff:

- aumenta o tempo de build e troubleshooting logo no começo

### 2. Frontend sem router e sem views

Escolha:

- uma tela única em `App.vue`

Por que:

- o objetivo do Dia 1 era provar infraestrutura, não navegação
- reduz esforço prematuro em estrutura de UI

Tradeoff:

- essa tela seria inevitavelmente substituída quando surgisse o upload no Dia 2

### 3. Backend mínimo com health check

Escolha:

- apenas `GET /health`

Por que:

- health check é a menor superfície útil para validar stack
- desacopla o primeiro passo de banco, storage e regras de negócio

Tradeoff:

- a estrutura do backend ficou boa para começar, mas ainda rasa para evoluir

### 4. Vuetify desde o começo

Escolha:

- já instalar Vuetify no setup inicial

Por que:

- `descricao.md` já definia essa stack
- evita migrar visual e componentes no meio da implementação

Tradeoff:

- adiciona peso de dependência antes de existir funcionalidade real

## Ajustes posteriores ainda ligados ao Dia 1

Depois do setup inicial, houve um hardening operacional no commit `7adcf09`:

- `backend/.dockerignore`
- `frontend/.dockerignore`
- atualização de `.gitignore`

Isso foi feito para:

- reduzir build context
- impedir envio de `node_modules`, `dist`, caches e ambientes locais para a imagem
- deixar o fluxo Docker mais enxuto

Embora tenha vindo depois, esse ajuste ainda pertence à consolidação do Dia 1.

## O que nao foi feito no Dia 1

Deliberadamente ficaram de fora:

- upload de arquivos
- banco com tabela de domínio
- persistência de documentos
- leitura e streaming de PDFs
- componentes Vue organizados por feature
- migrations com Alembic

Essa limitação foi intencional para preservar foco no objetivo do dia: ambiente funcionando.

## Validacao esperada do Dia 1

O critério de aceite do Dia 1 era:

- `docker compose up --build`
- `http://localhost:5173`
- `http://localhost:8000/health`
- Postgres saudável no Compose

Em termos arquiteturais, o Dia 1 foi um dia de infraestrutura e contrato operacional, não de regra de negócio.
