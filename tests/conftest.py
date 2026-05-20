import importlib
import os
import sys
from contextlib import contextmanager
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@contextmanager
def create_test_client(tmp_path: Path):
    database_path = tmp_path / "test.db"
    storage_path = tmp_path / "storage"

    os.environ["DATABASE_URL"] = f"sqlite:///{database_path}"
    os.environ["LOCAL_STORAGE_PATH"] = str(storage_path)
    os.environ["MAX_UPLOAD_SIZE_MB"] = "10"
    os.environ["APP_ENV"] = "test"

    for module_name in [
        "app.main",
        "app.api.documents",
        "app.services.file_service",
        "app.schemas.document",
        "app.models.document",
        "app.db.database",
        "app.core.config",
    ]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    main = importlib.import_module("app.main")
    with TestClient(main.create_app()) as client:
        yield client
