"""Wave 0 tests for aitaro console entrypoint stubs (D-01/D-05/D-06)."""

from __future__ import annotations

from pathlib import Path

import aitaro_api
import aitaro_setup


def test_aitaro_api_main_is_callable() -> None:
    assert callable(aitaro_api.main)


def test_aitaro_setup_main_is_callable() -> None:
    assert callable(aitaro_setup.main)


def test_ensure_backend_on_path_returns_repo_root_with_backend() -> None:
    root = aitaro_api.ensure_backend_on_path()
    assert isinstance(root, Path)
    assert (root / "src" / "backend").is_dir()
    assert (root / "pyproject.toml").is_file()


def test_ensure_backend_on_path_allows_server_import() -> None:
    aitaro_api.ensure_backend_on_path()
    from server.required_env import REQUIRED_ENV_KEYS

    assert REQUIRED_ENV_KEYS == ("STREAM_API_KEY", "OPENAI_API_KEY", "ZEP_API")
