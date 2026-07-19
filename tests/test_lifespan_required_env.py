"""Lifespan require_env_or_raise ordering and aitaro-api uvicorn kwargs (Plan 10-03)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI

import aitaro_api
import server.app as app_mod
import server.required_env as required_env_mod


@pytest.fixture(autouse=True)
def _disable_dotenv_load(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(required_env_mod, "_load_dotenv_from_repo", lambda: None)


@pytest.mark.asyncio
async def test_lifespan_skips_setup_when_require_env_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    setup = AsyncMock()
    monkeypatch.setattr(app_mod, "setup_workflow", setup)
    monkeypatch.setattr(
        app_mod,
        "require_env_or_raise",
        MagicMock(side_effect=RuntimeError("Missing required environment variables:\n  - STREAM_API_KEY")),
    )

    fake_app = FastAPI()
    with pytest.raises(RuntimeError, match="STREAM_API_KEY"):
        async with app_mod.lifespan(fake_app):
            pass

    setup.assert_not_awaited()
    setup.assert_not_called()


@pytest.mark.asyncio
async def test_lifespan_calls_setup_after_require_env_passes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    setup = AsyncMock(return_value=object())
    require = MagicMock()
    monkeypatch.setattr(app_mod, "setup_workflow", setup)
    monkeypatch.setattr(app_mod, "require_env_or_raise", require)

    fake_app = FastAPI()
    async with app_mod.lifespan(fake_app):
        require.assert_called_once_with()
        setup.assert_awaited_once()


def test_aitaro_api_main_uvicorn_kwargs(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[dict[str, Any]] = []

    def fake_run(*args: object, **kwargs: object) -> None:
        captured.append({"args": args, "kwargs": kwargs})

    monkeypatch.setattr(aitaro_api.uvicorn, "run", fake_run)
    aitaro_api.main()

    assert len(captured) == 1
    call = captured[0]
    assert call["args"][0] == "server.app:app"
    assert call["kwargs"]["host"] == "127.0.0.1"
    assert call["kwargs"]["port"] == 8000
    assert call["kwargs"]["reload"] is True
