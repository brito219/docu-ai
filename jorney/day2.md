# Day 2 — Upload and Local Persistence

## Overview

Day 2 turned the Day 1 baseline into a real product slice. The system moved from “the stack runs” to “the application completes a real use case”: uploading a PDF, validating it, storing it on disk, and recording metadata in PostgreSQL.

The implemented flow was:

1. the frontend selects a PDF
2. the frontend sends `multipart/form-data`
3. the backend validates the file
4. the backend generates an internal UUID-based filename
5. the backend saves the PDF to local storage
6. the backend writes a row to `documents`
7. the backend returns a public metadata payload
8. the frontend shows loading, success, or error feedback

## What was implemented

### Backend refactor

The backend moved from a single-purpose `main.py` to a minimal layered structure:

- `backend/app/api/`
- `backend/app/core/`
- `backend/app/db/`
- `backend/app/models/`
- `backend/app/schemas/`
- `backend/app/services/`

Main files introduced:

- `backend/app/api/documents.py`
- `backend/app/core/config.py`
- `backend/app/db/database.py`
- `backend/app/models/document.py`
- `backend/app/schemas/document.py`
- `backend/app/services/file_service.py`

This refactor was necessary because Day 2 introduced validation, persistence, and business logic. Keeping all of that inside `main.py` would have made the project harder to evolve immediately.

### App factory and startup behavior

`backend/app/main.py` was rewritten around `create_app()`.

Why:

- makes test setup easier
- allows the app to be recreated with different environment settings
- reduces coupling between module import and runtime startup

On startup, the backend now:

- ensures `LOCAL_STORAGE_PATH` exists
- runs `Base.metadata.create_all(bind=engine)`

### Centralized configuration

`backend/app/core/config.py` introduced a `Settings` object.

Relevant variables:

- `APP_ENV`
- `DATABASE_URL`
- `FRONTEND_ORIGIN`
- `STORAGE_TYPE`
- `LOCAL_STORAGE_PATH`
- `MAX_UPLOAD_SIZE_MB`

Why centralize configuration:

- avoids scattered `os.getenv()` calls
- creates a single source of truth for defaults
- simplifies testing and later expansion

### Database and domain model

`backend/app/db/database.py` introduced:

- `engine`
- `SessionLocal`
- `Base`
- `get_db()`

`backend/app/models/document.py` introduced:

- `StorageType`
- `DocumentStatus`
- `Document`

Persisted fields:

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

### Upload endpoint

The following endpoint was created:

- `POST /documents/upload`

File:

- `backend/app/api/documents.py`

This endpoint:

- receives `UploadFile`
- reads the file payload
- validates the upload
- generates a local storage path
- saves the file
- writes metadata to the database
- returns a `DocumentResponse`

### PDF validation

Validation logic was implemented in `backend/app/services/file_service.py`.

Rules enforced:

- file is required
- extension must be `.pdf`
- `content_type` must be one of the allowed PDF-like values
- payload must not be empty
- file size must be at most `10 MB`
- payload must start with `%PDF`

Why validate this way:

- the filename alone is not trustworthy
- empty or arbitrary files must be rejected early
- upload size must be controlled
- the first version should stay lightweight and deterministic

### Local file persistence

Uploaded files are stored using:

- an internal UUID-based filename
- the original file extension
- a directory derived from `LOCAL_STORAGE_PATH`

Why UUIDs are used:

- avoids filename collisions
- decouples the original filename from the physical storage name
- improves operational safety

### Failure handling

If the database write fails after the PDF was already saved:

- the session is rolled back
- the saved file is deleted

Why this matters:

- avoids orphaned files on disk
- keeps the database and filesystem in sync

## Frontend changes

### New UI goal

`frontend/src/App.vue` stopped being a static setup screen and became a working upload screen.

Implemented behavior:

- file selection via `v-file-input`
- upload through `axios`
- loading state
- error state
- success state
- metadata display after a successful upload

### Dedicated API client

New file:

- `frontend/src/services/api.ts`

Why:

- keeps the API base URL out of the component
- prepares the codebase for future endpoints
- avoids repeated configuration

### Explicit UI states

The component now uses:

- `idle`
- `loading`
- `success`
- `error`

Why explicit states matter:

- the behavior becomes predictable
- the UI becomes easier to reason about
- the template avoids ambiguous conditional logic

### New frontend dependency

Added:

- `axios`

Files affected:

- `frontend/package.json`
- `frontend/package-lock.json`

## Files created on Day 2

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

### Tests

- `tests/backend/test_documents_upload.py`

## Files modified on Day 2

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

## Files effectively replaced

There were no important feature files removed and abandoned. The main changes were structural replacements inside existing files, especially:

- `backend/app/main.py`
- `frontend/src/App.vue`

## Architectural decisions on Day 2

### 1. `create_all` instead of Alembic

Decision:

- use `Base.metadata.create_all()`

Why:

- faster path to a working upload flow
- lower friction for the second development day
- sufficient for a single initial table

Tradeoff:

- no formal migration history yet
- schema evolution will eventually need Alembic

### 2. Local storage instead of S3

Decision:

- store uploaded PDFs on the local filesystem

Why:

- Day 2 explicitly targets local persistence
- keeps costs at zero
- reduces infrastructure complexity

Tradeoff:

- no remote durability or distribution yet

### 3. Persist `local_path` but hide it from the API

Decision:

- keep `local_path` in the database
- exclude it from `DocumentResponse`

Why:

- the backend needs an internal pointer to the file
- clients should not see server filesystem paths

Tradeoff:

- requires a proper response schema instead of returning ORM objects directly

### 4. Signature check with `%PDF`

Decision:

- verify the initial bytes of the upload

Why:

- cheap and useful validation
- stronger than checking extension and content type alone

Tradeoff:

- not a full semantic PDF validation

### 5. Single-screen upload UI

Decision:

- keep the frontend on one screen without router or view structure yet

Why:

- keeps Day 2 focused on the upload flow
- avoids prematurely solving Day 3 navigation

Tradeoff:

- `App.vue` became heavier than it should be long term

### 6. SQLite-based isolated tests

Decision:

- avoid depending on the Docker PostgreSQL instance for tests

Why:

- tests should be fast and reproducible
- contributors should not need live infrastructure to validate the flow

Tradeoff:

- SQLite does not perfectly mirror PostgreSQL behavior
- it is still sufficient for this milestone

## Tests introduced or updated

### `tests/conftest.py`

This helper now:

- injects `PYTHONPATH`
- overrides `DATABASE_URL`
- overrides `LOCAL_STORAGE_PATH`
- overrides `MAX_UPLOAD_SIZE_MB`
- recreates relevant modules
- yields an isolated `TestClient`

### `tests/backend/test_health.py`

The health test was updated to:

- run against an isolated app instance
- validate the test environment wiring

### `tests/backend/test_documents_upload.py`

This file covers:

- successful upload
- file persistence
- metadata persistence
- rejection by invalid extension
- rejection by invalid PDF signature
- rejection by file size limit

## Supporting changes

### `.env.example`

New variables added:

- `STORAGE_TYPE=LOCAL`
- `LOCAL_STORAGE_PATH=/app/storage`
- `MAX_UPLOAD_SIZE_MB=10`

### `.gitignore`

New ignore entry:

- `backend/storage/`

Why:

- uploaded PDFs should never be committed

### `README.md`

The main README was updated to describe:

- the upload endpoint
- the Day 2 local upload flow
- the new runtime validation checklist

## Current repository state

At the time this document was written:

- Day 1 and Docker hardening were already present in Git history
- Day 2 existed in the current working tree
- the documentation reflects the actual code state rather than a future plan

## Technical summary

Day 2 established four foundational capabilities:

- the first real business endpoint
- the first persisted domain model
- the first full UI-to-API workflow
- the first isolated backend integration tests

This was the point where the project stopped being only “a stack that starts” and became “an application that executes a real use case”.
