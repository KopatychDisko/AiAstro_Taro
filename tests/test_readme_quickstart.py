"""README Quick start must document aitaro scripts without PYTHONPATH uvicorn (D-08/D-16)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"


def test_readme_documents_aitaro_setup_and_api() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "uv run aitaro-setup" in text
    assert "uv run aitaro-api" in text


def test_readme_has_no_pythonpath_uvicorn() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "PYTHONPATH=" in line and "uvicorn" in line:
            raise AssertionError(
                f"README must not document PYTHONPATH uvicorn (D-08): {line!r}"
            )


def test_readme_quick_start_mentions_env_sync_and_ui() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "cp .env.example .env" in text
    assert "uv sync" in text
    assert "login_menu.py" in text
