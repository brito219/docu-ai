# Day 1 — Project Setup

## Overview

Day 1 moved the repository from a documentation-first state to an executable full-stack baseline. Before that point, the project mostly contained `descricao.md` and very little operational structure. The goal was to create a predictable local development foundation with a frontend, backend, and database that could run together in a standardized way.

The practical output of Day 1 was:

- a reachable Vue 3 frontend
- a FastAPI backend responding to `GET /health`
- PostgreSQL running through Docker
- a minimal set of environment variables and project documentation

## What was implemented

### Initial backend

A minimal FastAPI backend was created with:

- `backend/app/main.py`
- `backend/requirements.txt`
- `backend/Dockerfile`
- `backend/app/__init__.py`

This backend exposed a single endpoint:

- `GET /health`

That endpoint existed to prove that:

- the Python application started correctly
- the backend container worked
- the frontend already had a stable API URL to target

### Initial frontend

A Vue 3 frontend was created with Vite, TypeScript, and Vuetify:

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

The first frontend intentionally had no router, store, or API integration. It was a static status screen designed to validate the stack and make the running services visible.

### Local orchestration

`docker-compose.yml` was added at the repository root with three services:

- `db`
- `backend`
- `frontend`

The Compose file handled:

- PostgreSQL startup with a persistent volume
- backend image build and runtime
- frontend image build and runtime
- port exposure for `5432`, `8000`, and `5173`
- basic startup ordering with `depends_on`

### Configuration and documentation

The following files were created or filled in:

- `.env.example`
- `.gitignore`
- `README.md`
- `tests/conftest.py`
- `tests/backend/test_health.py`

The README documented:

- prerequisites
- local startup with Docker Compose
- optional startup without Docker
- a minimal validation checklist

## Files created on Day 1

Based on commit `20e6eeb chore: setup inicial`, these were the main files introduced:

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

## Architectural decisions on Day 1

### 1. Full stack through Docker Compose

Decision:

- run frontend, backend, and database through Compose

Why:

- reduces environment drift
- forces integration from the beginning
- documents the runtime architecture on day one

Tradeoff:

- introduces Docker-related troubleshooting earlier in the project

### 2. Single-screen frontend

Decision:

- keep the UI inside `App.vue`

Why:

- Day 1 was about infrastructure, not navigation
- avoids premature structure in the UI layer

Tradeoff:

- the initial screen was always expected to be replaced once upload functionality arrived

### 3. Minimal backend with health check only

Decision:

- implement only `GET /health`

Why:

- it is the smallest useful surface for stack validation
- it isolates the first milestone from storage, database schema, and business rules

Tradeoff:

- the backend structure was enough to start, but intentionally shallow

### 4. Vuetify from the start

Decision:

- install Vuetify as part of the initial setup

Why:

- `descricao.md` already established it as part of the intended stack
- avoids reworking the UI foundation later

Tradeoff:

- adds dependency weight before real application behavior exists

## Later improvements still related to Day 1

After the initial setup, commit `7adcf09` added operational hardening:

- `backend/.dockerignore`
- `frontend/.dockerignore`
- `.gitignore` updates

This was done to:

- shrink the Docker build context
- avoid sending `node_modules`, build outputs, caches, and local environments to images
- make the Docker workflow leaner and more predictable

Even though this happened later, it still belongs to the Day 1 consolidation work.

## What Day 1 intentionally did not include

These items were deliberately deferred:

- file upload
- domain tables
- document persistence
- PDF reading and streaming
- feature-level Vue components
- Alembic migrations

The goal was to keep the first day focused on an environment that starts and can be verified quickly.

## Day 1 acceptance criteria

The expected validation for Day 1 was:

- `docker compose up --build`
- `http://localhost:5173`
- `http://localhost:8000/health`
- PostgreSQL marked as healthy in Compose

Architecturally, Day 1 was about infrastructure and runtime contracts, not yet about business functionality.
