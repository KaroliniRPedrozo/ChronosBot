import sys
import os
from pathlib import Path

# Ensure the `backend` package is resolvable when tests run from the workspace
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# During tests we set a dummy Gemini key so importing modules that
# initialize the Gemini client doesn't raise at import-time.
os.environ.setdefault("GEMINI_API_KEY", "test")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_status_routes():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

    r2 = client.get("/health")
    assert r2.status_code == 200
    assert r2.json().get("status") == "healthy"
