# DocuAI Viewer

Base setup for Day 1 of the DocuAI Viewer project. This repository now includes a Vue 3 + Vuetify frontend, a FastAPI backend, and PostgreSQL orchestrated with Docker Compose.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Vuetify
- Backend: FastAPI, Uvicorn
- Database: PostgreSQL 16
- Dev tooling: Docker Compose, `npm`, `venv` + `pip`

## Project Structure

- `frontend/` Vue application
- `backend/` FastAPI application
- `tests/backend/` backend tests
- `docker-compose.yml` local stack orchestration
- `.env.example` required environment variables

## Prerequisites

- Docker Engine with Compose plugin available as `docker compose`
- Node.js 20+
- Python 3.12+

## Local Setup

1. Copy the environment file:

```bash
cp .env.example .env
```

2. Start the full stack:

```bash
docker compose up --build
```

3. Access the services:

- Frontend: `http://localhost:5173`
- Backend health check: `http://localhost:8000/health`
- Backend upload endpoint: `http://localhost:8000/documents/upload`
- PostgreSQL: `localhost:5432`

## Day 2 Flow

The application now supports local PDF upload with metadata persistence.

- The frontend sends the selected PDF as `multipart/form-data`
- The backend validates extension, content type, file size, and PDF signature
- The file is stored in the local storage directory configured by `LOCAL_STORAGE_PATH`
- Document metadata is stored in PostgreSQL

## Running Without Docker

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Validation Checklist

- `docker compose up --build` completes successfully
- `GET /health` returns HTTP `200`
- Frontend loads and shows the upload screen
- Uploading a valid PDF returns success and persists metadata
- PostgreSQL container starts with the configured credentials
