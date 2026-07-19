"""Tests for aitaro console entrypoints (packaging + aitaro-setup D-02/D-10–D-15)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import aitaro_api
import aitaro_setup
import server.required_env as required_env_mod
from server.required_env import REQUIRED_ENV_KEYS

_SECRET_VALUE = "super-secret-value-never-in-message"


@pytest.fixture(autouse=True)
def _disable_dotenv_load(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent repo .env from restoring keys after monkeypatch.delenv."""
    monkeypatch.setattr(required_env_mod, "_load_dotenv_from_repo", lambda: None)


def _set_all_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STREAM_API_KEY", _SECRET_VALUE)
    monkeypatch.setenv("OPENAI_API_KEY", _SECRET_VALUE)
    monkeypatch.setenv("ZEP_API", _SECRET_VALUE)


def test_aitaro_api_main_is_callable() -> None:
    assert callable(aitaro_api.main)


def test_aitaro_setup_main_is_callable() -> None:
    assert callable(aitaro_setup.main)


def test_find_repo_root_returns_pyproject_and_backend() -> None:
    root = aitaro_api.find_repo_root()
    assert isinstance(root, Path)
    assert (root / "pyproject.toml").is_file()
    assert (root / "src" / "backend").is_dir()


def test_ensure_backend_on_path_returns_repo_root_with_backend() -> None:
    root = aitaro_api.ensure_backend_on_path()
    assert isinstance(root, Path)
    assert (root / "src" / "backend").is_dir()
    assert (root / "pyproject.toml").is_file()


def test_ensure_backend_on_path_allows_server_import() -> None:
    aitaro_api.ensure_backend_on_path()
    from server.required_env import REQUIRED_ENV_KEYS as keys

    assert keys == ("STREAM_API_KEY", "OPENAI_API_KEY", "ZEP_API")


def test_aitaro_api_main_only_ensures_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(aitaro_api.uvicorn, "run", lambda *args, **kwargs: None)
    aitaro_api.main()
    from server.required_env import REQUIRED_ENV_KEYS as keys

    assert "STREAM_API_KEY" in keys


def test_build_tarot_mcp_missing_dir_raises(tmp_path: Path) -> None:
    missing_root = tmp_path / "empty-repo"
    missing_root.mkdir()
    with pytest.raises(FileNotFoundError, match="tarot"):
        aitaro_setup.build_tarot_mcp(missing_root)


def test_build_tarot_mcp_runs_fixed_npm_argv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = tmp_path / "repo"
    tarotmcp = repo_root / "src" / "tarotmcp"
    tarotmcp.mkdir(parents=True)
    calls: list[dict[str, Any]] = []

    def fake_run(
        args: list[str],
        cwd: Path | str | None = None,
        check: bool = False,
        **kwargs: object,
    ) -> object:
        calls.append({"args": list(args), "cwd": Path(cwd) if cwd is not None else None, "check": check, "kwargs": kwargs})
        return object()

    monkeypatch.setattr(aitaro_setup.subprocess, "run", fake_run)
    aitaro_setup.build_tarot_mcp(repo_root)

    assert len(calls) == 2
    assert calls[0]["args"] == ["npm", "install"]
    assert calls[1]["args"] == ["npm", "run", "build"]
    assert calls[0]["cwd"] == tarotmcp
    assert calls[1]["cwd"] == tarotmcp
    assert calls[0]["check"] is True
    assert calls[1]["check"] is True
    for call in calls:
        assert call["kwargs"].get("shell") is not True


def test_main_checks_env_before_npm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    order: list[str] = []

    def fake_require() -> None:
        order.append("env")

    def fake_build(repo_root: Path) -> None:
        order.append("npm")
        assert isinstance(repo_root, Path)

    aitaro_api.ensure_backend_on_path()
    monkeypatch.setattr(required_env_mod, "require_env_or_exit", fake_require)
    monkeypatch.setattr(aitaro_setup, "build_tarot_mcp", fake_build)
    aitaro_setup.main()
    assert order == ["env", "npm"]


def test_main_prints_checklist_with_login_menu_and_postgres(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _set_all_required(monkeypatch)
    monkeypatch.setattr(aitaro_setup, "build_tarot_mcp", lambda repo_root: None)
    aitaro_setup.main()
    out = capsys.readouterr().out
    assert "login_menu.py" in out
    assert "POSTGRESQL_" in out
    assert "uv run aitaro-api" in out
    assert "STREAM_API_KEY" in out
    assert "OPENAI_API_KEY" in out
    assert "ZEP_API" in out
    assert "uv sync" not in out.lower()
    assert _SECRET_VALUE not in out
    for key in REQUIRED_ENV_KEYS:
        assert key in out


def test_main_source_has_no_uv_sync() -> None:
    source = Path(aitaro_setup.__file__).read_text(encoding="utf-8")
    assert "uv sync" not in source
    assert "shell=True" not in source
