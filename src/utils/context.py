import json
import os
from pathlib import Path

def load_test_context():
    path = os.getenv("TEST_CONTEXT_PATH")
    if not path:
        raise RuntimeError("TEST_CONTEXT_PATH env var not set")
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"testContext.json not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))
