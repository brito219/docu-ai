# DocuAI Viewer

DocuAI Viewer is a full-stack application for uploading, validating, storing, and later viewing PDF documents. The current implementation focuses on local-first development: PDFs are stored on disk, document metadata is stored in PostgreSQL, the API is built with FastAPI, and the UI is built with Vue 3 and Vuetify.

## What the project does

- Uploads PDF files from the browser
- Validates file extension, content type, file size, and PDF signature
- Stores PDFs locally on the backend host
- Persists document metadata in PostgreSQL
- Exposes a documented FastAPI API with Swagger UI
- Provides a simple upload interface with loading, success, and error states

## Stack

- Frontend: Vue 3, TypeScript, Vite, Vuetify, Axios
- Backend: FastAPI, SQLAlchemy, Uvicorn
- Database: PostgreSQL 16
- Dev environment: Docker Compose

## Project structure

- `frontend/` Vue application
- `backend/` FastAPI application
- `tests/backend/` backend tests
- `jorney/` implementation notes and development history
- `docker-compose.yml` local orchestration
- `.env.example` environment template

## Prerequisites

- Docker Engine with the Compose plugin available as `docker compose`
- Node.js 20+ if you want to run the frontend outside Docker
- Python 3.12+ if you want to run the backend outside Docker

## Quick start

1. Copy the environment file:

```bash
cp .env.example .env
```

2. Start the stack:

```bash
docker compose up --build
```

3. Open the application:

- Frontend: `http://localhost:5173`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## API overview

### `GET /health`

Returns a basic health payload for the running API.

### `POST /documents/upload`

Accepts `multipart/form-data` with a `file` field, validates the PDF, stores it locally, and saves metadata in PostgreSQL.

## Environment variables

Key variables used by the application:

- `APP_ENV`: application environment label
- `DATABASE_URL`: backend database connection string
- `STORAGE_TYPE`: current storage mode, set to `LOCAL`
- `LOCAL_STORAGE_PATH`: backend directory for uploaded PDFs
- `MAX_UPLOAD_SIZE_MB`: maximum accepted upload size
- `FRONTEND_ORIGIN`: allowed CORS origin
- `VITE_API_URL`: frontend API base URL

See `.env.example` for the current defaults.

## Run without Docker

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Validation checklist

- `docker compose up --build` completes successfully
- `GET /health` returns HTTP `200`
- `POST /documents/upload` accepts a valid PDF
- Uploaded PDFs are stored under the configured local storage path
- Document metadata is written to PostgreSQL
- The frontend displays loading, success, and error states correctly

## Current scope

The repository currently covers the first functional milestone:

- local PDF upload
- local file persistence
- metadata persistence
- basic UI for upload feedback

Future milestones such as document listing, inline viewing, HTTP range streaming, text extraction, and semantic workflows are tracked separately in the project planning and journey notes.
