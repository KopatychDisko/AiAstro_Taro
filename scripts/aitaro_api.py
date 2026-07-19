"""Console entrypoint wrapper for aitaro-api (path + uvicorn defaults)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


def find_repo_root() -> Path:
    start = Path.cwd().resolve()
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "src" / "backend"
        ).is_dir():
            return candidate
    raise RuntimeError(
        "Could not find AiTaro repo root (pyproject.toml + src/backend). "
        "Run uv run aitaro-api from the repository."
    )


def ensure_backend_on_path() -> Path:
    root = find_repo_root()
    backend = root / "src" / "backend"
    backend_str = str(backend)
    if backend_str not in sys.path:
        sys.path.insert(0, backend_str)
    existing = os.environ.get("PYTHONPATH", "")
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_str not in parts:
        if not parts:
            os.environ["PYTHONPATH"] = backend_str
        else:
            os.environ["PYTHONPATH"] = backend_str + os.pathsep + existing
    return root


def main() -> None:
    ensure_backend_on_path()
    uvicorn.run(
        "server.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
